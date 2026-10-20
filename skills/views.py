from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Skill, UserSkill, SkillTest, Question, Answer, TestAttempt, LEVEL_CHOICES
from accounts.models import UserStreak


@login_required
def skill_setup(request):
    CATEGORY_LABELS = [
        ('tech', 'Technology'), ('music', 'Music'), ('art', 'Art & Design'),
        ('language', 'Languages'), ('cooking', 'Cooking'), ('fitness', 'Fitness'),
        ('business', 'Business'), ('science', 'Science'), ('math', 'Mathematics'),
        ('writing', 'Writing'), ('photography', 'Photography'), ('craft', 'Crafts'),
        ('dance', 'Dance'), ('sports', 'Sports'), ('other', 'Other'),
    ]
    # Build list of (label, skills_queryset) only for categories that have skills
    categories_with_skills = []
    for cat_key, cat_label in CATEGORY_LABELS:
        skills = Skill.objects.filter(category=cat_key, is_active=True)
        if skills.exists():
            categories_with_skills.append((cat_label, skills))

    # Get currently selected skills for pre-population
    user_have = list(UserSkill.objects.filter(user=request.user, relation='have').values_list('skill_id', flat=True))
    user_want = list(UserSkill.objects.filter(user=request.user, relation='want').values_list('skill_id', flat=True))

    return render(request, 'skills/skill_setup.html', {
        'categories_with_skills': categories_with_skills,
        'user_have': user_have,
        'user_want': user_want,
    })


@login_required
def save_skills(request):
    if request.method == 'POST':
        have_skills = request.POST.getlist('have_skills')
        want_skills = request.POST.getlist('want_skills')
        UserSkill.objects.filter(user=request.user).delete()
        for skill_id in have_skills:
            skill = Skill.objects.filter(id=skill_id).first()
            if skill:
                UserSkill.objects.create(user=request.user, skill=skill, relation='have', level='beginner')
        for skill_id in want_skills:
            skill = Skill.objects.filter(id=skill_id).first()
            if skill:
                UserSkill.objects.create(user=request.user, skill=skill, relation='want')
        messages.success(request, 'Skills saved! Now take a quick test to verify your skill level.')
        return redirect('skill_tests')
    return redirect('skill_setup')


@login_required
def skill_tests(request):
    have_skills = UserSkill.objects.filter(user=request.user, relation='have').select_related('skill')
    tests_available = []
    for us in have_skills:
        for level, label in LEVEL_CHOICES:
            test = SkillTest.objects.filter(skill=us.skill, level=level).first()
            if test:
                completed = TestAttempt.objects.filter(user=request.user, test=test, passed=True).exists()
                tests_available.append({'user_skill': us, 'test': test, 'level': level, 'label': label, 'completed': completed})
    return render(request, 'skills/skill_tests.html', {'tests_available': tests_available})


@login_required
def take_test(request, test_id):
    test = get_object_or_404(SkillTest, id=test_id)
    questions = test.questions.prefetch_related('answers').all()
    if request.method == 'POST':
        correct = 0
        total = questions.count()
        for question in questions:
            selected = request.POST.get(f'q_{question.id}')
            if selected:
                answer = Answer.objects.filter(id=selected, is_correct=True).first()
                if answer:
                    correct += 1
        score = int((correct / total) * 100) if total > 0 else 0
        passed = score >= test.passing_score
        attempt = TestAttempt.objects.create(
            user=request.user, test=test, score=score,
            total_questions=total, passed=passed
        )
        if passed:
            us = UserSkill.objects.filter(user=request.user, skill=test.skill, relation='have').first()
            if us:
                us.level = test.level
                us.verified = True
                us.save()
            streak = getattr(request.user, 'streak', None)
            if streak:
                streak.add_xp(50)
        return render(request, 'skills/test_result.html', {
            'test': test, 'score': score, 'passed': passed,
            'correct': correct, 'total': total, 'attempt': attempt
        })
    return render(request, 'skills/take_test.html', {'test': test, 'questions': questions})


@login_required
def my_skills(request):
    have_skills = UserSkill.objects.filter(user=request.user, relation='have').select_related('skill')
    want_skills = UserSkill.objects.filter(user=request.user, relation='want').select_related('skill')
    return render(request, 'skills/my_skills.html', {
        'have_skills': have_skills,
        'want_skills': want_skills,
    })
 
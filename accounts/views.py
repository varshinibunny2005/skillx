from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import User, UserStreak, Notification
from .forms import SignupForm, LoginForm, ProfileUpdateForm
from skills.models import UserSkill, SkillTest
from matching.models import SkillMatch
from community.models import Community


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/home.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserStreak.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome to SkillX, {user.first_name}! 🎉')
            return redirect('skill_setup')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            streak = getattr(user, 'streak', None)
            if streak:
                streak.update_streak()
            messages.success(request, f'Welcome back, {user.first_name}! 👋')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    user = request.user
    streak = getattr(user, 'streak', None)
    user_skills = UserSkill.objects.filter(user=user).select_related('skill')
    matches = SkillMatch.objects.filter(user=user, status='pending').select_related('matched_user').order_by('-score')[:5]
    unread_count = Notification.objects.filter(user=user, is_read=False).count()
    notifications = Notification.objects.filter(user=user, is_read=False)[:5]
    communities = Community.objects.filter(members=user)[:3]

    # Leaderboard top 10
    top_users = UserStreak.objects.select_related('user').order_by('-total_xp')[:10]

    context = {
        'streak': streak,
        'user_skills': user_skills,
        'matches': matches,
        'notifications': notifications,
        'communities': communities,
        'top_users': top_users,
        'unread_count': unread_count,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user
    user_skills = UserSkill.objects.filter(user=profile_user).select_related('skill')
    streak = getattr(profile_user, 'streak', None)
    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'user_skills': user_skills,
        'streak': streak,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def leaderboard(request):
    top_users = UserStreak.objects.select_related('user').order_by('-total_xp')[:50]
    streak_leaders = UserStreak.objects.select_related('user').order_by('-current_streak')[:10]
    user_rank = None
    if hasattr(request.user, 'streak'):
        all_ranks = list(UserStreak.objects.order_by('-total_xp').values_list('user_id', flat=True))
        if request.user.id in all_ranks:
            user_rank = all_ranks.index(request.user.id) + 1
    return render(request, 'accounts/leaderboard.html', {
        'top_users': top_users,
        'streak_leaders': streak_leaders,
        'user_rank': user_rank,
    })


@login_required
def mark_notification_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect(notif.link or 'dashboard')

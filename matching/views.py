from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
import uuid
from .models import SkillMatch, ConnectionRequest, Message, VideoSession
from skills.models import UserSkill, Skill
from accounts.models import User, Notification, LANGUAGE_CHOICES


def compute_matches(user):
    """Find users who have skills this user wants, and want skills this user has."""
    want_skill_ids = set(UserSkill.objects.filter(user=user, relation='want').values_list('skill_id', flat=True))
    have_skill_ids = set(UserSkill.objects.filter(user=user, relation='have').values_list('skill_id', flat=True))
    candidates = User.objects.exclude(id=user.id)
    for candidate in candidates:
        cand_have = set(UserSkill.objects.filter(user=candidate, relation='have').values_list('skill_id', flat=True))
        cand_want = set(UserSkill.objects.filter(user=candidate, relation='want').values_list('skill_id', flat=True))
        shared_teach = cand_have.intersection(want_skill_ids)   # candidate can teach user
        shared_learn = cand_want.intersection(have_skill_ids)   # user can teach candidate
        if shared_teach or shared_learn:
            score = min(100, len(shared_teach) * 10 + len(shared_learn) * 10 +
                        (20 if user.preferred_language == candidate.preferred_language else 0))
            SkillMatch.objects.update_or_create(
                user=user, matched_user=candidate,
                defaults={'score': score}
            )
    return SkillMatch.objects.filter(user=user).select_related('matched_user').order_by('-score')


@login_required
def find_matches(request):
    matches = compute_matches(request.user)
    # Apply filters
    age_min = request.GET.get('age_min')
    age_max = request.GET.get('age_max')
    gender = request.GET.get('gender')
    language = request.GET.get('language')
    skill_filter = request.GET.get('skill')

    filtered = []
    for match in matches:
        mu = match.matched_user
        include = True
        if age_min and mu.age and mu.age < int(age_min):
            include = False
        if age_max and mu.age and mu.age > int(age_max):
            include = False
        if gender and gender != 'any' and mu.gender != gender:
            include = False
        if language and mu.preferred_language != language:
            include = False
        if include:
            filtered.append(match)

    return render(request, 'matching/find_matches.html', {
        'matches': filtered,
        'total': len(filtered),
        'language_choices': LANGUAGE_CHOICES,
        'skills': Skill.objects.filter(is_active=True),
        'filters': request.GET,
    })


@login_required
def send_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        message = request.POST.get('message', '')
        skill_id = request.POST.get('skill_id')
        skill = Skill.objects.filter(id=skill_id).first()
        req, created = ConnectionRequest.objects.get_or_create(
            sender=request.user, receiver=receiver,
            defaults={'message': message, 'skill_to_learn': skill}
        )
        if created:
            Notification.objects.create(
                user=receiver, notif_type='request',
                title=f'New connection request from {request.user.full_name}',
                message=f'{request.user.full_name} wants to connect with you to learn/share skills.',
                link=f'/matching/requests/'
            )
            messages.success(request, f'Request sent to {receiver.full_name}!')
        else:
            messages.info(request, 'Request already sent.')
    return redirect('find_matches')


@login_required
def manage_requests(request):
    received = ConnectionRequest.objects.filter(receiver=request.user, status='pending')
    sent = ConnectionRequest.objects.filter(sender=request.user)
    return render(request, 'matching/requests.html', {'received': received, 'sent': sent})


@login_required
def accept_request(request, req_id):
    req = get_object_or_404(ConnectionRequest, id=req_id, receiver=request.user)
    req.status = 'accepted'
    req.save()
    Notification.objects.create(
        user=req.sender, notif_type='accepted',
        title=f'{request.user.full_name} accepted your request!',
        message='You can now start messaging and scheduling sessions.',
        link=f'/matching/chat/{request.user.id}/'
    )
    messages.success(request, f'Connected with {req.sender.full_name}!')
    return redirect('manage_requests')


@login_required
def decline_request(request, req_id):
    req = get_object_or_404(ConnectionRequest, id=req_id, receiver=request.user)
    req.status = 'declined'
    req.save()
    return redirect('manage_requests')


@login_required
def connections(request):
    accepted_sent = ConnectionRequest.objects.filter(sender=request.user, status='accepted').select_related('receiver')
    accepted_recv = ConnectionRequest.objects.filter(receiver=request.user, status='accepted').select_related('sender')
    # Build list of partner users (not ConnectionRequest objects)
    partners = []
    seen = set()
    for conn in accepted_sent:
        if conn.receiver_id not in seen:
            partners.append(conn.receiver)
            seen.add(conn.receiver_id)
    for conn in accepted_recv:
        if conn.sender_id not in seen:
            partners.append(conn.sender)
            seen.add(conn.sender_id)
    return render(request, 'matching/connections.html', {'partners': partners})


@login_required
def chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    # Check they are connected
    is_connected = ConnectionRequest.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user),
        status='accepted'
    ).exists()
    if not is_connected:
        messages.error(request, 'You must be connected to chat.')
        return redirect('connections')
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
    messages_qs = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    sessions = VideoSession.objects.filter(
        Q(host=request.user, participant=other_user) | Q(host=other_user, participant=request.user)
    ).order_by('-created_at')[:5]
    return render(request, 'matching/chat.html', {
        'other_user': other_user,
        'messages': messages_qs,
        'sessions': sessions,
    })


@login_required
def start_video_session(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    room_id = str(uuid.uuid4())[:8].upper()
    session = VideoSession.objects.create(
        host=request.user, participant=other_user,
        room_id=room_id, status='active',
        started_at=timezone.now()
    )
    Notification.objects.create(
        user=other_user, notif_type='session',
        title=f'{request.user.full_name} started a video session!',
        message=f'Join room: {room_id}',
        link=f'/matching/video/{session.id}/'
    )
    return redirect('video_room', session_id=session.id)


@login_required
def video_room(request, session_id):
    session = get_object_or_404(VideoSession, id=session_id)
    if request.user not in [session.host, session.participant]:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    chat_partner = session.participant if request.user == session.host else session.host
    return render(request, 'matching/video_room.html', {
        'session': session,
        'chat_partner': chat_partner,
    })

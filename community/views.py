from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Community, Group, Post, Comment
from skills.models import Skill


@login_required
def community_list(request):
    my_communities = Community.objects.filter(members=request.user)
    discover = Community.objects.filter(is_public=True).exclude(members=request.user)[:12]
    return render(request, 'community/list.html', {
        'my_communities': my_communities,
        'discover': discover,
    })


@login_required
def create_community(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        skill_id = request.POST.get('skill')
        is_public = request.POST.get('is_public') == 'on'
        skill = Skill.objects.filter(id=skill_id).first()
        community = Community.objects.create(
            name=name, description=description, creator=request.user,
            skill=skill, is_public=is_public
        )
        community.members.add(request.user)
        messages.success(request, f'Community "{name}" created!')
        return redirect('community_detail', pk=community.pk)
    skills = Skill.objects.filter(is_active=True)
    return render(request, 'community/create.html', {'skills': skills})


@login_required
def community_detail(request, pk):
    community = get_object_or_404(Community, pk=pk)
    is_member = community.members.filter(id=request.user.id).exists()
    posts = community.posts.select_related('author').prefetch_related('comments', 'likes')[:20]
    groups = community.groups.all()[:6]
    if request.method == 'POST' and is_member:
        content = request.POST.get('content', '').strip()
        if content:
            Post.objects.create(community=community, author=request.user, content=content)
            return redirect('community_detail', pk=pk)
    return render(request, 'community/detail.html', {
        'community': community,
        'is_member': is_member,
        'posts': posts,
        'groups': groups,
    })


@login_required
def join_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    community.members.add(request.user)
    messages.success(request, f'Joined {community.name}!')
    return redirect('community_detail', pk=pk)


@login_required
def leave_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    community.members.remove(request.user)
    return redirect('community_list')


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'community_list'))


@login_required
def group_list(request):
    my_groups = Group.objects.filter(members=request.user)
    public_groups = Group.objects.filter(is_private=False).exclude(members=request.user)[:12]
    return render(request, 'community/groups.html', {
        'my_groups': my_groups,
        'public_groups': public_groups,
    })


@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_private = request.POST.get('is_private') == 'on'
        community_id = request.POST.get('community')
        community = Community.objects.filter(id=community_id).first()
        group = Group.objects.create(
            name=name, description=description, creator=request.user,
            is_private=is_private, community=community
        )
        group.members.add(request.user)
        messages.success(request, f'Group "{name}" created!')
        return redirect('group_detail', pk=group.pk)
    communities = Community.objects.filter(members=request.user)
    return render(request, 'community/create_group.html', {'communities': communities})


@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    is_member = group.members.filter(id=request.user.id).exists()
    posts = group.posts.select_related('author').prefetch_related('comments')[:20]
    if request.method == 'POST' and is_member:
        content = request.POST.get('content', '').strip()
        if content:
            Post.objects.create(group=group, author=request.user, content=content)
            return redirect('group_detail', pk=pk)
    return render(request, 'community/group_detail.html', {
        'group': group, 'is_member': is_member, 'posts': posts
    })


@login_required
def join_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if group.members.count() < group.max_members:
        group.members.add(request.user)
        messages.success(request, f'Joined group {group.name}!')
    else:
        messages.error(request, 'Group is full.')
    return redirect('group_detail', pk=pk)

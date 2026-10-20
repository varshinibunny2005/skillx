from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def learning_home(request):
    return redirect('dashboard')

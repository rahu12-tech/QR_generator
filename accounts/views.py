from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from qrapp.models import QRCode


# Create your views here.

def signup_view(request):
    if request.method == "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        return redirect('login')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(
            request,
            username=username,
            password=password,
        )
        if user is not None:
            if not user.is_active:
                return render(request, 'login.html', {'error': 'Your account has been blocked by the admin. Please contact support.'})
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def account_view(request):
    user = request.user
    total_qrs = QRCode.objects.filter(user=user).count()
    error = None
    success = None

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_info':
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            if User.objects.exclude(id=user.id).filter(username=username).exists():
                error = 'Username already taken.'
            else:
                user.username = username
                user.email = email
                user.save()
                success = 'Profile updated.'

        elif action == 'change_password':
            old = request.POST.get('old_password')
            new = request.POST.get('new_password')
            if not user.check_password(old):
                error = 'Old password is incorrect.'
            else:
                user.set_password(new)
                user.save()
                update_session_auth_hash(request, user)
                success = 'Password changed successfully.'

        elif action == 'delete_account':
            user.delete()
            return redirect('login')

    return render(request, 'accounts/account.html', {
        'total_qrs': total_qrs,
        'error': error,
        'success': success,
    })
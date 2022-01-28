from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    logout_then_login, LoginView,
)

from .decorators import logout_required
from django.http import HttpRequest
from django.shortcuts import render, redirect

# Create your views here.
from .form import JoinForm, ProfileForm

login = LoginView.as_view(template_name="accounts/login.html")


def logout(request: HttpRequest):
    messages.success(request, "로그아웃 되었습니다.")
    return logout_then_login(request)


@logout_required
def join(request: HttpRequest):
    if request.method == 'POST':
        form = JoinForm(request.POST, request.FILES)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입을 환영합니다.")
            # signed_user.send_welcome_email()
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = JoinForm()
    return render(request, 'accounts/join.html', {
        'form': form,
    })


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필을 저장했습니다.")
            return redirect("/index/")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile_edit_form.html", {
        "form": form,
    })

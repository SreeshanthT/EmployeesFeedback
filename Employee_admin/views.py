from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse

# Create your views here.
def login_view(request,*args,**kwargs):
    redirect_to = request.GET.get('next') or request.POST.get('next') or 'dashboard'
    if request.user.is_authenticated:
        return redirect(redirect_to)
    
    if request.method == "POST":
        user = authenticate(
                request,
                username = request.POST.get('username'),
                password = request.POST.get('password')
                )
        if user is not None:
            login(request,user)
            messages.success(request,'Login successfully completed')
            return redirect(redirect_to)
        
        messages.error(request,'invalid credentials')
        
    return render(request,'login_page.html',locals())

def logout_view(request,*args,**kwargs):
    logout(request)
    return redirect(request.GET.get('next', reverse('login-page')))


@login_required(login_url="login-page")
def dashboard(request,*args,**kwargs):
    print(request.user.has_perm("pygmalion_user.add_user"))
    return render(request,'dashboard.html',locals())

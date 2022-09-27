from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.db.models import Q

from Employee_admin.utils import get_object_or_none,ManageBaseView
from Employee_admin.mixins import LoggedInUser
from Employee_admin.forms import *
from .models import Review, User, Department

OOPS = 'Oops! Something went wrong try again later.'
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
    dashboard_active = True
    complete_users = User.objects.all()
    return render(request,'dashboard.html',locals())


class UserManagementView(LoggedInUser,ManageBaseView):

    def list_of_users(self,request,*args,**kwargs):
        table_data = User.objects.exclude(Q(is_staff = True)| Q(is_superuser = True))
        return render(request,'list_of_users.html',locals())

    def manage_user(self,request,*args,**kwargs):
        user_active = True
        cancel_url = reverse('list-users')
        user_ = get_object_or_none(User,slug=kwargs.get('user_slug'))
        if user_ is not None:
            form = UserUpdationForm(instance = user_)
        else:
            form = UserForm(instance = user_)

            
        if request.method == "POST":
            form = UserForm(request.POST,request.FILES,instance = user_)
            if user_ is not None:
                form = UserUpdationForm(request.POST,request.FILES,instance = user_)
            print(user_) 
            print(request.POST.get('department'))
            if form.is_valid():
                groups = form.cleaned_data.get('groups')
                form_object = form.save()
                if user_ is not None:
                    messages.success(request,f'user {form_object.username} is successfully updated')
                    request.user.log_change(request,form_object,form.changed_data)
                else:
                    messages.success(request,f'user {form_object.username} is successfully added')
                    request.user.log_addition(request,form_object)
                return redirect(reverse('list-users'))
            else:
                messages.error(request,OOPS)

                print(form.errors)
            
        return render(request,'manage_user.html',locals())
    
    def view_user_details(self,request,*args,**kwargs):
        user_active = True
        user_detail = get_object_or_404(User,slug=kwargs.get('user_slug'))
        change_password_form = UserChangePasswordForm(instance = user_detail)
        form = AssignForm(initial={
            'rated_for': user_detail.created_review_for(),
        })
        form.fields['rated_for'].queryset = form.fields['rated_for'].queryset.exclude(
            id__in = [user_detail.id,request.user.id]
        )
        
        
        return render(request,'user_details.html',locals())
    
    def change_password(self,request,*args,**kwargs):
        user_detail = get_object_or_404(User,slug=kwargs.get('user_slug'))
        if request.method == "POST":
            change_password_form = UserChangePasswordForm(request.POST,instance = user_detail)
            if change_password_form.is_valid():
                form_object = change_password_form.save()
                request.user.log_change(request,form_object,change_password_form.changed_data)
                messages.success(request,f'Password for {user_detail.capitalize} is updated')
            else:
                messages.error(request,OOPS) 
            print(change_password_form.errors)
        return redirect(request.META.get('HTTP_REFERER') or request.GET.get('next'))
    
    def assign_for_review(self,request,*args,**kwargs):
        review_by = get_object_or_404(User,slug = kwargs.get('user_slug'))
        print('hi')
        if request.method == "POST":
            for i in request.POST.getlist('rated_for'):
                rate = Review.objects.get_or_create(
                    rated_for_id = i,rated_by=review_by
                )[0]
                print(rate)
        return redirect(request.GET.get('next') or reverse('view-user',  args=[review_by.slug]))
    
class ReviewManagementView(LoggedInUser,ManageBaseView):
    def list_of_review(self,request,*args,**kwargs):
        table_data = Review.objects.filter(is_rated = True)
        return render(request,'list_of_reviews.html',locals())
    
    def manage_review(self,request,*args,**kwargs):
        review_active = True
        cancel_url = reverse('list-review')
        review = get_object_or_none(Review,id=kwargs.get('pk'))
            
        form = ReviewForm(instance = review)


            
        if request.method == "POST":
            form = ReviewForm(request.POST,request.FILES,instance = review)

            print(request.POST.get('department'))
            if form.is_valid():
                form_object = form.save()
                if review is not None:
                    messages.success(request,f'{form_object} is successfully updated')
                    request.user.log_change(request,form_object,form.changed_data)
                else:
                    messages.success(request,f'{form_object} is successfully added')
                    request.user.log_addition(request,form_object)
                return redirect(cancel_url)
            else:
                messages.error(request,OOPS)

                print(form.errors)
            
        return render(request,'manage_review.html',locals())
    
class DepartmentManagementView(LoggedInUser,ManageBaseView):
    def list_of_department(self,request,*args,**kwargs):
        table_data = Department.objects.all()
        return render(request,'list_of_department.html',locals())
    
    def manage_department(self,request,*args,**kwargs):
        department_active = True
        cancel_url = reverse('list-department')
        department = get_object_or_none(Department,id=kwargs.get('pk'))
        print(department)
        form = DepartmentForm(instance = department)


            
        if request.method == "POST":
            form = DepartmentForm(request.POST,instance = department)

            print(request.POST.get('department'))
            if form.is_valid():
                form_object = form.save()
                if department is not None:
                    messages.success(request,f'department {form_object} is successfully updated')
                    request.user.log_change(request,form_object,form.changed_data)
                else:
                    messages.success(request,f'department {form_object} is successfully added')
                    request.user.log_addition(request,form_object)
                return redirect(cancel_url)
            else:
                messages.error(request,OOPS)

                print(form.errors)
            
        return render(request,'manage_department.html',locals())
    
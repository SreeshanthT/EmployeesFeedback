from django.urls import path,include
from . import views

urlpatterns = [
    path('login',views.login_view,name='login-page' ), 
    path('logout',views.logout_view,name='logout-page' ),
     
    
    path('users/',include([
        path('',views.UserManagementView.as_view(method_name="list_of_users"),name='list-users'),
        path('manage-user-<str:user_slug>',views.UserManagementView.as_view(method_name="manage_user"),name='manage-user'),
        path('details-of-user-<str:user_slug>',views.UserManagementView.as_view(method_name="view_user_details"),name='view-user'),
        path('change-password-<str:user_slug>',views.UserManagementView.as_view(method_name="change_password"),name='change-password'),
        path('assign-review-<str:user_slug>',views.UserManagementView.as_view(method_name="assign_for_review"),name='assign_for_review'),
    ])),
    
    path('review/',include([
        path('',views.ReviewManagementView.as_view(method_name='list_of_review'),name='list-review'),
        path('add-review/',views.ReviewManagementView.as_view(method_name='manage_review'),name='add-review'),
        path('edit-review/<str:pk>/',views.ReviewManagementView.as_view(method_name='manage_review'),name='edit-review'),
    ])),
    path('department/',include([
        path('',views.DepartmentManagementView.as_view(method_name='list_of_department'),name='list-department'),
        path('add-department/',views.DepartmentManagementView.as_view(method_name='manage_department'),name='add-department'),
        path('edit-department/<str:pk>/',views.DepartmentManagementView.as_view(method_name='manage_department'),name='edit-department'),
    ]))
]
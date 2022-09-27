from django.urls import path,include
from . import views

urlpatterns = [
    path('',include([
        path('pending-feedback/',views.FeedbackView.as_view(method_name='list_pendings'),name='list-pending'),
        path('feedback/',views.FeedbackView.as_view(method_name='list_reviewed'),name='list-feedback'),
    ]))
]
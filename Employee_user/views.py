from django.shortcuts import render
from Employee_admin.utils import get_object_or_none,ManageBaseView
from Employee_admin.mixins import LoggedInUser

# Create your views here.


class FeedbackView(LoggedInUser,ManageBaseView):

    def list_pendings(self,request,*args,**kwargs):
        Pending_active=True
        pendings = request.user.pending_feedback()
        return render(request,'pending.html',locals())

    def list_reviewed(self,request,*args,**kwargs):
        Reviewed_active = True
        pendings = request.user.reviewed_feedback()
        return render(request,'reviewed.html',locals())
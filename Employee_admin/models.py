
from django.db import models
from django.contrib.auth.models import AbstractUser

from Employee.widgets import WEBPField

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)

class User(AbstractUser):
    cover_image = WEBPField(upload_to='user/cover_picture', blank=True, variations={
        'large': (600, 400),
        'thumbnail': (200, 200, True),
        'medium': (300, 200),
        'original': (None, None)
    })
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    
    def get_profile_pic(self):
        return(
            """
            https://ui-avatars.com/api/?background=0033C4&
            color=fff&size=256&name={}&rounded=true&bold=true
            """.format(self.username or self.email)
        )
        
class Review(models.Model):
    rate = models.PositiveIntegerField()
    discription = models.TextField()
    
    rated_for = models.ForeignKey(User,on_delete=models.CASCADE,related_name='my_feedback')
    rated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_feedback')
    
    is_rated = models.BooleanField(default=False)
     
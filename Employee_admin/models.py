
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    
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
     
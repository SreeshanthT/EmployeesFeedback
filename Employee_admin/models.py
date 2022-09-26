
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.admin.options import get_content_type_for_model
from django.utils.text import get_text_list
from django.core.files.storage import FileSystemStorage

from django_lifecycle import LifecycleModelMixin,hook,BEFORE_CREATE,BEFORE_UPDATE,BEFORE_SAVE

from Employee.widgets import WEBPField
from Employee_admin.utils import unique_slug_generator

import json
import re
import random

ADDITION = 1
CHANGE = 2
DELETION = 3
# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name

class User(LifecycleModelMixin,AbstractUser):
    random_images = [
                '/static/assets/img/others/cover_photo_1.jpg', '/static/assets/img/others/cover_photo_2.jpg',
                '/static/assets/img/others/cover_photo_3.jpg', '/static/assets/img/others/cover_photo_4.jpg',
                '/static/assets/img/others/cover_photo_5.jpg', '/static/assets/img/others/cover_photo_6.jpg',
                '/static/assets/img/others/cover_photo_7.jpg', '/static/assets/img/others/cover_photo_8.jpg',
                '/static/assets/img/others/cover_photo_9.jpg'
            ]
    cover_image = WEBPField(upload_to='cover_picture', blank=True, variations={
        'large': (600, 400),
        'thumbnail': (200, 200, True),
        'medium': (300, 200),
        'original': (None, None)
    },storage=FileSystemStorage())
    
    department = models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    
    slug = models.SlugField(blank=True,max_length=255)

    def get_status(self):
        if self.is_active:
            return 'Active'
        else:
            return 'Inactive'
        
    def get_profile_pic(self):
        return(
            """
            https://ui-avatars.com/api/?background=0033C4&
            color=fff&size=256&name={}&rounded=true&bold=true
            """.format(self.username or self.email)
        )
    
    def get_cover(self):
        return self.cover_image.url if self.cover_image else \
            random.choice(self.random_images) or "https://via.placeholder.com/340x120/FFB6C1/000000"
    
    def __str__(self) -> str:
        return self.username
    
    @hook(BEFORE_CREATE)
    def set_slug(self):
        self.slug = unique_slug_generator(self,self.username)
        
        
    def log_addition(self, request, object, messages = 	[{"added": {}}]):
        
        if isinstance(messages, list):
            messages = json.dumps(messages)
        
        return UserLogEntry.objects.create(
            user=request.user,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=str(object),
            action_flag=ADDITION,
            change_message = messages,
        )
    def log_change(self, request, object, changed_fields ):
        url = request.get_full_path()[1:] if bool(re.match("^/",request.get_full_path())) else request.get_full_path()
        print(request.build_absolute_uri('/'))
        messages = [{"changed": {"fields": changed_fields }}]
        if isinstance(messages, list):
            messages = json.dumps(messages)
        
        return UserLogEntry.objects.create(
            user=request.user,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=str(object),
            action_flag=CHANGE,
            change_message = messages,
            url = url
        )
    def log_deletion(self, request, object):
        return UserLogEntry.objects.create(
            user=request.user,
            content_type_id=get_content_type_for_model(object).pk,
            object_id=object.pk,
            object_repr=str(object),
            action_flag=DELETION,
        )
       
    def created_review_for(self):
        val =  self.__class__.objects.filter(
            my_feedback__in = self.created_feedback.all()
        )
        print(val)
        return val
    
    def pending_feedback(self):
        return self.created_feedback.filter(is_rated = False)
    
    def reviewed_feedback(self):
        return self.created_feedback.filter(is_rated = True)
     
class Review(models.Model):
    rate = models.PositiveIntegerField(null=True)
    discription = models.TextField(null=True)
    
    rated_for = models.ForeignKey(User,on_delete=models.CASCADE,related_name='my_feedback',null=True)
    rated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_feedback')
    
    is_rated = models.BooleanField(default=False)
    

    @hook(BEFORE_SAVE)
    def set_rated(self):
        if self.rate is not None and self.discription is not None:
            is_rated = True
        else:
            is_rated = False
            
    @hook(BEFORE_UPDATE, when='rate', has_changed=True)
    def set_rated(self):
        if self.rate is not None:
            is_rated = True
        else:
            is_rated = False
            
    
class UserLogEntry(models.Model):
    user = models.ForeignKey(
        User,
        models.CASCADE,
        verbose_name = _('user'),
    )
    content_type = models.ForeignKey(
        ContentType,
        models.SET_NULL,
        verbose_name=_('content type'),
        blank=True, null=True,
    )
    object_id = models.TextField(_('object id'), blank=True, null=True)
    object_repr = models.CharField(_('object repr'), max_length=200)
    change_message = models.TextField(_('change message'), blank=True,null=True)
    action_flag = models.PositiveSmallIntegerField(_('action flag'), choices=(
    (ADDITION, _('Addition')),
    (CHANGE, _('Change')),
    (DELETION, _('Deletion')),
    ))
    time = models.DateTimeField(auto_now_add=True,null=True)
    url = models.URLField(null=True)
    
    def __str__(self):
        if self.is_addition():
            return gettext('Added “%(object)s”.') % {'object': self.object_repr}
        elif self.is_change():
            return gettext('Changed “%(object)s” — %(changes)s') % {
                'object': self.object_repr,
                'changes': self.get_change_message(),
            }
        elif self.is_deletion():
            return gettext('Deleted “%(object)s.”') % {'object': self.object_repr}

        return gettext('UserLogEntry Object')
    
    def is_addition(self):
        return self.action_flag == ADDITION

    def is_change(self):
        return self.action_flag == CHANGE

    def is_deletion(self):
        return self.action_flag == DELETION
    
    def get_edited_object(self):
        """Return the edited object represented by this log entry."""
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def get_change_message(self):
        """
        If self.change_message is a JSON structure, interpret it as a change
        string, properly translated.
        """
        if self.change_message and self.change_message[0] == '[':
            try:
                change_message = json.loads(self.change_message)
            except json.JSONDecodeError:
                return self.change_message
            messages = []
            for sub_message in change_message:
                if 'added' in sub_message:
                    if sub_message['added']:
                        sub_message['added']['name'] = gettext(sub_message['added']['name'])
                        messages.append(gettext('Added {name} “{object}”.').format(**sub_message['added']))
                    else:
                        messages.append(gettext('Added.'))

                elif 'changed' in sub_message:
                    sub_message['changed']['fields'] = get_text_list(
                        [gettext(field_name) for field_name in sub_message['changed']['fields']], gettext('and')
                    )
                    if 'name' in sub_message['changed']:
                        sub_message['changed']['name'] = gettext(sub_message['changed']['name'])
                        messages.append(gettext('Changed {fields} for {name} “{object}”.').format(
                            **sub_message['changed']
                        ))
                    else:
                        messages.append(gettext('Changed {fields}.').format(**sub_message['changed']))

                elif 'deleted' in sub_message:
                    sub_message['deleted']['name'] = gettext(sub_message['deleted']['name'])
                    messages.append(gettext('Deleted {name} “{object}”.').format(**sub_message['deleted']))

            change_message = ' '.join(msg[0].upper() + msg[1:] for msg in messages)
            return change_message or gettext('No fields changed.')
        else:
            return self.change_message
        
    def get_message(self):
        
        if self.is_addition():
            return f"""
                <small>{self.user} added
                    <span class="fw-bold">{self.object_repr}</span>
                </small>
                """
        if self.is_change():
            return f"""
                <small>{self.user} changed {self.object_repr}
                    <span class="fw-bold">{self.get_change_message()}</span>
                </small>
                """
        if self.is_deletion():
            return f"""
                <small>{self.user} deleted
                    <span class="fw-bold">{self.object_repr}</span>
                </small>
                """
   
     
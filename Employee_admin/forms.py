from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm 
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Review, User,Department

from django_select2.forms import ModelSelect2MultipleWidget,ModelSelect2Widget

class ReviewForWidget(ModelSelect2MultipleWidget):
    search_fields = [
        "username__icontains",
    ]
    
class DepartmentWidget(ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]

class UserForm(UserCreationForm):

    # department = forms.ModelChoiceField(
    #     required=False, 
    #     queryset=Department.objects.all(),
    #     widget=DepartmentWidget
    # )
    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control form-control-sm',
            })

    class Meta:
        model = User
        fields = ['username','department','cover_image']
        
class UserUpdationForm(UserChangeForm):
    password = None
    # department = forms.ModelChoiceField(
    #     required=False, 
    #     queryset=Department.objects.all(),
    #     widget=DepartmentWidget
    # )
    
    def __init__(self, *args, **kwargs):
        super(UserUpdationForm,self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control form-control-sm',
            })
    class Meta:
        model = User
        fields = ['username','department','cover_image']
     
class UserChangePasswordForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    
    def __init__(self, *args, **kwargs):
        super(UserChangePasswordForm,self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control form-control-sm',
            })

    class Meta:
        model = User
        fields = ("password1","password2")


    def clean_password2(self):
        self.cleaned_data
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
 
 
class AssignForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignForm,self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control form-control-sm',
            })
    rated_for = forms.ModelMultipleChoiceField(
        required=False, 
        queryset=User.objects.filter(is_active = True),
        widget=ReviewForWidget
    )
    class Meta:
        model = Review
        fields = ['rated_for',]
        
class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm,self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class':'form-control form-control-sm',
            })

        self.fields['rate'].widget.attrs.update({'max':"5"})
    class Meta:
        model = Review
        fields = ['rated_for','rated_by','rate','discription']
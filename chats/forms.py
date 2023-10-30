from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User,Follower,Creator


from allauth.account.forms import SignupForm 
#newly added


#####################Django all auth #####################################


class FollowerSignUpForm(SignupForm):
    first_name = forms.CharField(required=True)
    # last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    
    

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')
    
    @transaction.atomic
    def save(self, request):
        user = super(FollowerSignUpForm, self).save(request)
        user.is_Follower = True
        user.is_staff = False
        user.is_superuser = False
        user.first_name = self.cleaned_data.get('first_name')
        # user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('username')
        user.save()
        follower = Follower.objects.create(user = user)
        
        follower.save()
        return user
   


class CreatorSignUpForm(SignupForm):
    
    first_name = forms.CharField(required=True)
    # last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)

    
    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        
        user = super().save(commit=False)
        user.is_Creator = True
        user.is_staff = False
        user.is_superuser = False
        user.is_Follower = False
        
        user.first_name = self.cleaned_data.get('first_name')
        # user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('username')
        if commit:
            user.save()
        creator = Creator.objects.create(user=user)
        
        if commit:
            user.save()

        return user
    



################ end of Django all auth ###########################################

# class FollowerSignUpForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     # last_name = forms.CharField(required=True)
#     username = forms.CharField(required=True)
    
    

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('username','email', 'password1', 'password2')
    
#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.is_Follower = True
#         user.is_staff = False
#         user.is_superuser = False
#         user.first_name = self.cleaned_data.get('first_name')
#         # user.last_name = self.cleaned_data.get('last_name')
#         user.username = self.cleaned_data.get('username')
#         user.save()
#         follower = Follower.objects.create(user = user)
        
#         follower.save()
#         return user
   


# class CreatorSignUpForm(UserCreationForm):
    
#     first_name = forms.CharField(required=True)
#     # last_name = forms.CharField(required=True)
#     username = forms.CharField(required=True)

    
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ('username','email', 'password1', 'password2')

#     @transaction.atomic
#     def save(self, commit=True):
        
#         user = super().save(commit=False)
#         user.is_Creator = True
#         user.is_staff = False
#         user.is_superuser = False
        
#         user.first_name = self.cleaned_data.get('first_name')
#         # user.last_name = self.cleaned_data.get('last_name')
#         user.username = self.cleaned_data.get('username')
#         if commit:
#             user.save()
#         creator = Creator.objects.create(user=user)
        
#         if commit:
#             user.save()

#         return user
    


    ##################################################
    ###############  password change #################
from django import forms

class UserSearchForm(forms.Form):
    search_query = forms.CharField(max_length=255)


# forms.py


class FileUploadForm(forms.Form):
    file = forms.FileField()



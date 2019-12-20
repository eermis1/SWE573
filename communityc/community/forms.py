from django import forms
from .models import (Community, Post, CommunityMembership)
from django.contrib.auth.models import User


class CommunityCreateForm(forms.ModelForm):
    class Meta : 
        model = Community
        fields = ["community_name", "community_description","community_tag"]

class PostTypeCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["post_title", "post_description", "post_tag"]
        
class  UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ["username", "email", "password"]

class CommunityMembershipForm (forms.ModelForm):
    class Meta:
        model = CommunityMembership
        fields = []
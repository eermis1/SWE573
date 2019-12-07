from django import forms
from .models import (Community, Post)


class CommunityCreateForm(forms.ModelForm):
    class Meta : 
        model = Community
        fields = ["community_name", "community_description","community_tag"]

class PostTypeCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["post_title", "post_description", "post_tag"]
        
    
    #model = Post
    #post_title = forms.CharField(max_length=100)
    #post_description = forms.CharField(max_length=200)
    #post_tag = forms.CharField(max_length=150)
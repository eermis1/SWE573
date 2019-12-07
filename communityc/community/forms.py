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
        
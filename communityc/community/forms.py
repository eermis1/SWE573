from django import forms
from .models import (Community, Post)


class CommunityCreateForm(forms.ModelForm):
    class Meta : 
        model = Community
        fields = ["community_name", "community_description","community_tag"]
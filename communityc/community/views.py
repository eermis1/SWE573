from django.views.generic import (CreateView, DetailView, ListView, UpdateView, DeleteView)
from django.http import Http404
from .models import Community
from. models import Post
from .forms import CommunityCreateForm

class CommunityListView(ListView): 

    context_object_name = "all_communities" 
    template_name = "index.html"
    
    def get_queryset(self):
        return Community.objects.all()

class CommunityDetailView(DetailView):
    model = Community #Primary Key of Lists --> Community. primary key olduğunu hep model ile belirtiyoruz
    template_name = "detail.html"
    
    def get_queryset(self):
        return Community.objects.all()

class CommunityCreate(CreateView):
    model = Community
    template_name = "community_form.html"
    form_class = CommunityCreateForm
    
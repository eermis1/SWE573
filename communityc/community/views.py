from django.views.generic import (CreateView, DetailView, ListView, UpdateView, DeleteView)
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Community
from. models import Post
from .forms import CommunityCreateForm, PostTypeCreateForm

class CommunityListView(ListView): 

    context_object_name = "all_communities" 
    template_name = "index.html"
    
    def get_queryset(self):
        return Community.objects.all()

class CommunityDetailView(DetailView):
    model = Community #Primary Key of Lists --> Community. primary key olduğunu hep model ile belirtiyoruz
    template_name = "community_detail.html"
    
    def get_queryset(self):
        return Community.objects.all()

class CommunityCreate(CreateView):
    model = Community
    template_name = "community_form.html"
    form_class = CommunityCreateForm
    
def PostTypeCreate(request, community_id):

    community = get_object_or_404(Community, pk=community_id)
    if request.method == "POST":
        form = PostTypeCreateForm(request.POST)
        if form.is_valid():
            Post = form.save(commit=False)
            Post.community = community #autofill labels
            Post.save()
            return HttpResponse("success")
        return render(request, 'posttype_form', {'form': form})
    else:
        form = PostTypeCreateForm()
   
    return render(request, "posttype_form.html", {"form" : form})


from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import Http404
from django.views import generic
from django.template import loader
from django.shortcuts import render
from .models import Community
from. models import Post
from django.urls import reverse

class ListView(generic.ListView): 

    template_name = "index.html"
    context_object_name = "all_communities" 
    #alttaki get_query her zaman object_list olarak return verdiğimizden index.html'deki all_communities kısmına
    # ya object_list diyecektik ya da bu şekilde object_list --> all_communities dönüşümü yapacaktık. 
    
    def get_queryset(self):
        return Community.objects.all()

class DetailView(generic.DetailView):
    model = Community #Primary Key of Lists --> Community. primary key olduğunu hep model ile belirtiyoruz
    template_name = "detail.html"

class CommunityCreate(CreateView):
    model = Community
    #template_name = "community_form.html"
    fields = ["community_name", "community_description","community_tag"]
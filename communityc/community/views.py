from django.views.generic import (CreateView, DetailView, ListView, UpdateView, DeleteView)
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Community
from. models import Post
from .forms import CommunityCreateForm, PostTypeCreateForm
from django.http import JsonResponse
import uuid
import requests

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

            # fields = {}
            # fields.setdefault("field_name", []) #Set Field Name as Key, Values As Python List
            # fields.setdefault("field_type", []) #Set Field Name as Key, Values As Python List
            # fields.setdefault("field_required", []) #Set Field Name as Key, Values As Python List
            
            # #Get Values From The Form 
            # fields["field_name"] = request.POST.get("dt_fieldlabel_v1", "")
            # fields["field_name"] = request.POST.get("dt_fieldlabel_v2", "")
            # fields["field_name"] = request.POST.get("dt_fieldlabel_v3", "")
            # fields["field_name"] = request.POST.get("dt_fieldlabel_v4", "")
            # fields["field_name"] = request.POST.get("dt_fieldlabel_v5", "")
            # Post.formfield = fields
            # Post.save()

            return HttpResponse("success")
        return render(request, 'posttype_form', {'form': form})
    else:
        form = PostTypeCreateForm()
   
    return render(request, "posttype_form.html", {"form" : form})


def AddSemanticTag(request):
    tag = [] #Create Empty List
    if request.method == "POST":   

        input_for_tag = request.POST.get("input_box", "Hatali Giris")
        #-----------000-------------------000------------------- 
        #Wikidata Query
        API_ENDPOINT = "https://www.wikidata.org/w/api.php"
        query = input_for_tag
        params = {
        'action': 'wbsearchentities',
        'format': 'json',
        'language': 'en',
        'limit': '3',
        'search': query
        }
        wiki_request = requests.get(API_ENDPOINT, params=params)
        wiki_return = wiki_request.json()["search"] 
        #-----------000-------------------000------------------- 
        #Put Items Into A List For Render
        for i in range(len(wiki_return)):
            try:
                tag.append(wiki_return[i]["description"])
            except KeyError:
                continue
        
        return render(request, "wikidata.html",{"tag":tag})

    return render(request, "wikidata.html",{"tag":tag})




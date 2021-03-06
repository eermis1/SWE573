from django.views.generic import (CreateView, DetailView, ListView, UpdateView, DeleteView, View)
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Community, Post, CommunityMembership, PostObject
from .forms import CommunityCreateForm, PostTypeCreateForm, UserRegistrationForm, CommunityMembershipForm,PostObjectCreateForm, CommunityEditForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils import timezone
from django.core import serializers
from .serializers import post_type_serializer
import datetime
from django.db.models import Q
import json
import requests

# Generic Note
# Model Post represents Post Type
# Model PostObject represents Post in the requirements

#----------------------------------------------------- List / Index / Detail Views -----------------------------------------------------------
class CommunityListView(ListView): 

    context_object_name = "all_communities" 
    template_name = "index.html"
    
    def get_queryset(self):
        #Sort Communities By Creation Date From Newest To Oldest
        communities  = Community.objects.order_by("-community_creation_date")
        #3 Way Search Of Community
        query = self.request.GET.get("q")
        if query:
            communities = communities.filter(Q(community_name__icontains=query) |
                                             Q(community_description__icontains=query) |
                                             Q(community_tag__icontains=query)).distinct()
        return communities
   
class Community_PostType_DetailView(DetailView):
    # This View Enables To List All Post Types According To Specified Community
    model = Community
    #context_object_name = "all_post_types"
    template_name = "index_pt.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Community_PostType_DetailView, self).get_context_data(**kwargs)
        #Search availability for Post Type Detail page       
        post_types = Post.objects.filter(community=self.object).order_by("-post_creation_date")
        query = self.request.GET.get("q")
        if query:
            post_types = post_types.filter(Q(post_title__icontains=query) |
                                           Q(post_description__icontains=query) |
                                           Q(post_tag__icontains=query)).distinct()
        context["all_post_types"] = post_types
        return context

class PostType_PostObject_DetailView(DetailView):
    # This View Enables To List All Post Objects According To Specified Post Type
    model = Post
    template_name = "index_pto.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PostType_PostObject_DetailView, self).get_context_data(**kwargs)
        #Search availability for Post Object Detail page       
        all_post_objects = PostObject.objects.filter(post=self.object).order_by("-post_object_creation_date")
        query = self.request.GET.get("q")
        if query:
            all_post_objects = all_post_objects.filter(Q(post_object_name__icontains=query) |
                                                    Q(post_object_description__icontains=query) |
                                                    Q(post_object_tag__icontains=query)).distinct()
        context["all_post_objects"] = all_post_objects
        return context

def PostObject_Detailview(request, post_id):

    post_list = PostObject.objects.get(pk = post_id)
    tmpObj = serializers.serialize("json", PostObject.objects.filter(pk=post_id).only('data_fields'))
    a = json.loads(tmpObj)
    data_fields = json.loads(a[0]["fields"]["data_fields"])
    return render(request, "index_ptod.html", {'post_list': post_list, "data_fields": data_fields})

class CommunityDetailView(DetailView):
    model = Community #Primary Key of Lists --> Community. primary key olduğunu hep model ile belirtiyoruz
    template_name = "community_detail.html"
    
    def get_queryset(self):
        return Community.objects.all()

class PostTypeListView(ListView): 

    context_object_name = "all_post_types" 
    template_name = "index_pt_all.html"
    
    def get_queryset(self):
        #Sort Communities By Creation Date From Newest To Oldest
        all_post_types  = Post.objects.order_by("-post_creation_date")
        #3 Way Search Of Community
        query = self.request.GET.get("q")
        if query:
            all_post_types = all_post_types.filter(Q(post_title__icontains=query) |
                                                   Q(post_description__icontains=query) |
                                                   Q(post_tag__icontains=query)).distinct()
        return all_post_types

class PostObjectListView(ListView): 

    context_object_name = "all_post_objects" 
    template_name = "index_pto_all.html"
    
    def get_queryset(self):
        #Sort Communities By Creation Date From Newest To Oldest
        all_post_objects  = PostObject.objects.order_by("-post_object_creation_date")
        #3 Way Search Of Community
        query = self.request.GET.get("q")
        if query:
            all_post_objects = all_post_objects.filter(Q(post_object_name__icontains=query) |
                                                       Q(post_object_description__icontains=query) |
                                                       Q(post_object_tag__icontains=query)).distinct() 
        return all_post_objects

#----------------------------------------------------- Create/Edit Vievs -----------------------------------------------------------
# To Do Community Edit

def CommunityCreate(request):
    # To Overcome Simple Lazy Object Error We Used Auhentication Check Before Community Creation
    # In Principle If A User Wants To Build A Community He/She Has To Loggin or Register First
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CommunityCreateForm(request.POST)
            if form.is_valid():
                Community = form.save(commit=False)
                Community.community_builder = request.user
                Community_community_creation_date = timezone.now()
                Community.save()
                return redirect("community:homepage")
            return redirect("community:homepage")
        else:
            form = CommunityCreateForm()
        return render(request,"community_form.html",{"form":form})
    else:    
        return render(request, 'user_login.html', {})
    
def PostTypeCreate(request, community_id):
    
    if request.user.is_authenticated:
        community = get_object_or_404(Community, pk=community_id)
        if request.method == "POST":
            form = PostTypeCreateForm(request.POST)
            if form.is_valid():
                Post = form.save(commit=False)
                Post.community = community 
                Post.post_owner = request.user
                jsonfield = request.POST.get("fieldJson")
                Post.formfield = jsonfield
                Post.save()
                return redirect("community:posttype_all")
            return redirect("community:posttype_all")
        else:
            form = PostTypeCreateForm()
        return render(request, "posttype_form.html", {"form" : form})
    else:
         return render(request, 'user_login.html', {})

def PostTypeObjectCreate(request, post_id):

    post_type = get_object_or_404(Post,pk=post_id)
    if request.user.is_authenticated:
        tmpObj = serializers.serialize("json", Post.objects.filter(pk=post_id).only('formfield'))
        a = json.loads(tmpObj)
        data_fields = json.loads(a[0]["fields"]["formfield"])
        if request.method == 'POST':
            form = PostObjectCreateForm(request.POST)
            if form.is_valid():
                PostObject = form.save(commit=False)
                PostObject.post = post_type
                PostObject.post_object_owner = request.user
                jsonfields = request.POST.get('fieldJsonpost')
                PostObject.data_fields = jsonfields
                PostObject.save()
                redirect("community:postobject_all")
            return redirect("community:postobject_all")
        else:
            form = PostObjectCreateForm()
        return render(request, 'posttypeobject_form.html', {'form': form, 'post_type': post_type, "data_fields": data_fields})
    else:
        return render(request, 'user_login.html', {})


def CommunityEdit(request, community_id):
    if request.user.is_authenticated:
        community = get_object_or_404(Community, pk=community_id)
        object = Community.objects.get(pk=community_id)
        form = CommunityEditForm(instance=object)
        community_user = Community.objects.get(pk=community_id).community_builder
        if request.user == community_user:
            if request.method == "POST":
                form = CommunityEditForm(request.POST, instance=object)
                community = form.save(commit=False)
                community.save()
                return redirect('community:homepage')
            return render (request, "community_form.html", {'form': form})
        else:
            all_communities = Community.objects.order_by("-community_creation_date")
            return render (request, "index.html",  {"error_message":"You are not autherizaed to change this community", 'community':community})
    else:    
        return render(request, 'user_login.html', {})

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

#-------------------------------------------------- Search & Join -------------------------------------------------------------

def Advanced_Search(request):
    #Load all data 
    communities  = Community.objects.order_by("-community_creation_date")
    post_types  = Post.objects.order_by("-post_creation_date")
    post_objects = PostObject.objects.order_by("-post_object_creation_date")

    #Get items to be searched
    query_all = request.GET.get('q_all')
    query_community = request.GET.get('q_com')
    query_posttype = request.GET.get('q_posttype')
    query_postobjects = request.GET.get('q_postobj')

    #Query Them
    if query_all:
        communities = communities.filter(Q(community_name__icontains=query_all) |
                                         Q(community_description__icontains=query_all) |
                                         Q(community_tag__icontains=query_all)).distinct()

        post_types = post_types.filter(Q(post_title__icontains=query_all) |
                                       Q(post_description__icontains=query_all) |
                                       Q(post_tag__icontains=query_all)).distinct()
        return render(request, "search.html", {"communities":communities, "post_types":post_types})
  
    if query_community:
        communities = communities.filter(Q(community_name__icontains=query_community) |
                                         Q(community_description__icontains=query_community) |
                                         Q(community_tag__icontains=query_community)).distinct()

        return render(request, "search.html", {"communities":communities})
    
    if query_posttype:
        post_types = post_types.filter(Q(post_title__icontains=query_posttype) |
                                       Q(post_description__icontains=query_posttype) |
                                       Q(post_tag__icontains=query_posttype)).distinct()
        return render(request, "search.html", {"post_types":post_types})

    if query_postobjects :
        post_objects = post_objects.filter(Q(post_object_name__icontains=query_postobjects ) |
                                           Q(post_object_description__icontains=query_postobjects ) |
                                           Q(post_object_tag__icontains=query_postobjects )).distinct() 

    return render(request, "search.html", {"communities":communities, "post_types":post_types, "post_objects":post_objects})

def Join_Communities(request, community_id):
    all_communities = Community.objects.order_by("-community_creation_date")
    community = get_object_or_404(Community, pk=community_id)
    
    if request.user.is_authenticated:
        form = CommunityMembershipForm(request.POST or None)
        CommunityMembership = form.save(commit=False)
        CommunityMembership.member = request.user
        CommunityMembership.community = community
        CommunityMembership.save()
        status = "Joined"
        return render(request, "index.html", {"all_communities":all_communities, "status":status})
    else:
         return render(request, 'user_login.html', {})

    return(request, "index.html",{"all_communities":all_communities})

#------------------------------------- User Registration / Loging / Logout Processes --------------------------------------

def UserRegistration(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        #cleaned / normalized data
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        email = form.cleaned_data["email"]
        user.set_password(password)
        # Save user crendentials to the database
        user.save()
        # return user objects if the credentials are correct
        user = authenticate(username = username, password = password)
        if user is not None: 
            if user.is_active:
                login(request, user)
                #redirect logged in users to homepage
                return redirect("community:homepage")
        
    return render(request, "user_registration_form.html", {"form":form})

def UserLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None: 
            if user.is_active:
                login(request, user)
                #redirect logged in users to homepage
                return redirect("community:homepage")
            else:
                return render(request, "user_login.html",{"error_message":"Your Account Has Been Disabled"})
        else:
            return render(request, "user_login.html", {"error_message":"Invalid Login Credentials"})
    
    return render(request, "user_login.html", {})

def UserLogout(request):
    logout(request)
    form = UserRegistrationForm(request.POST or None)
    return redirect("community:homepage")
                
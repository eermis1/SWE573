from django.views.generic import (CreateView, DetailView, ListView, UpdateView, DeleteView, View)
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Community, Post, CommunityMembership
from .forms import CommunityCreateForm, PostTypeCreateForm, UserRegistrationForm, CommunityMembershipForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils import timezone
import datetime
from django.db.models import Q

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
    model = Community
    #context_object_name = "all_post_types"
    template_name = "index_pt.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["all_post_types"] = Post.objects.all()
        return context

class CommunityDetailView(DetailView):
    model = Community #Primary Key of Lists --> Community. primary key olduğunu hep model ile belirtiyoruz
    template_name = "community_detail.html"
    
    def get_queryset(self):
        return Community.objects.all()

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
                return HttpResponse("Success")
            return HttpResponse("Success")
        else:
            form = PostTypeCreateForm()
        return render(request, "posttype_form.html", {"form" : form})
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


def Advanced_Search(request):
    #Load all data 
    communities  = Community.objects.order_by("-community_creation_date")
    post_types  = Post.objects.all() # order by creation date to be added
    #post to be added

    #Get items to be searched
    query_all = request.GET.get('q_all')
    query_community = request.GET.get('q_com')
    query_posttype = request.GET.get('q_posttype')

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

    return render(request, "search.html", {"communities":communities, "post_types":post_types})

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

# class MyCommunities(DetailView):
#     model = CommunityMembership
#     #context_object_name = "all_post_types"
#     template_name = "index_html"

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         context["all_community"] = Communty.objects.all()
#         return context
#-------------------------------------User Registration / Loging / Logout Processes--------------------------------------

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
                Communities = Community.objects.all() #All Dememize Rağmen Yönlendirdiği İndex Boş Gelyor ? 
                return render(request,"index.html",{"communities":Communities})
        
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
                Communities = Community.objects.all() #All Dememize Rağmen Yönlendirdiği İndex Boş Gelyor ? 
                return render(request,"index.html",{"communities":Communities})
            else:
                return render(request, "user_login.html",{"error_message":"Your Account Has Been Disabled"})
        else:
            return render(request, "user_login.html", {"error_message":"Invalid Login Credentials"})
    
    return render(request, "user_login.html", {})

def UserLogout(request):
    logout(request)
    form = UserRegistrationForm(request.POST or None)
    return render(request, "user_login.html", {"form":form})
                
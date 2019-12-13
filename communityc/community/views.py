from django.views.generic import (CreateView, DetailView, ListView, UpdateView, DeleteView, View)
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Community, Post
from .forms import CommunityCreateForm, PostTypeCreateForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils import timezone
import datetime

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
                return render(request, "community_detail.html", {"Community":Community})
            return render(request, "community_detail.html", {"Community":Community})
        else:
            form = CommunityCreateForm()
        return render(request,"community_form.html",{"form":form})
    else:    
        return render(request, 'user_login.html', {})
    
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

def Search(request):
    communities = Community.objects.all()
    post_types = Post.objects.all()
    query = request.GET.get("q") #Get Item To Be Search From Search Box Which Is Location On Index HTML
    if query:
        #Filter Community Name or Community Title Be Like Query Which Is Q
        communities = communities.filter(Q(community_name__icontains=query) | Q(community_tag__icontains=query)).distinct()
        return render(request,"index.html", {"communities":communities})
    else:
        return render(request,"index.html", {"communities":communities})


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
                
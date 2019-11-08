from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import render
from .models import Community
from. models import Post


def homepage(request):
    all_communities = Community.objects.all()
    return render(request, "index.html", {"all_communities" : all_communities} ) #context --> all communities.

def community_detail (request,community_id):
    #try:
    community = Community.objects.get(pk=community_id)
    #except Community.DoesNotExist:
 #       raise  Http404("Community Does Not Exist")
    return render(request, "detail.html", {"community" : community} )
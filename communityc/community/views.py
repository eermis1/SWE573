from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Community
from. models import Post


def homepage(request):

    all_communities = Community.objects.all()
    template = loader.get_template("community/index.html") 
    context = {
        "all_communities" : all_communities
    }
    return HttpResponse(template.render(context, request))

def community_detail (request,community_id):

    return HttpResponse("Hello, you're at the community detail page / Community :" + str(community_id))
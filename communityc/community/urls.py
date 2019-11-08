from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('<community_id>', views.community_detail, name="community_detail" )
]
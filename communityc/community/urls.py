from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListView.as_view(), name='homepage'),
    path('/<pk>', views.DetailView.as_view(), name="community_detail" )
]

#old structure
#urlpatterns = [
#    path('', views.homepage, name='homepage'),
#    path('/<community_id>', views.community_detail, name="community_detail" )
#]
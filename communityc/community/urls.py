from django.urls import path
from . import views
from .views import CommunityDetailView, CommunityListView

app_name = "community"
urlpatterns = [
    path('', views.CommunityListView.as_view(), name='homepage'),
    path("register/", views.UserRegistration, name="register"), #User Registration URL
    path("login/", views.UserLogin, name="login"), #User Login URL
    path("logout/", views.UserLogout, name="logout"), #User Logout URL
    path("join/<int:community_id>", views.Join_Communities, name="join"), #Join Communities
    path('search/', views.Advanced_Search, name="advanced_search"), #Advaced Search
    path('wikitag/', views.AddSemanticTag, name="semantic_tag"),#Community Semantic Tag Trial
    path('posttypes/<pk>/', views.Community_PostType_DetailView.as_view(), name="community_posttype_detail"), # Post Type List Based On A Specified Community
    path('postobjects/<pk>', views.PostType_PostObject_DetailView.as_view(), name="posttype_postobject_detail"), # Post Object List Based On A Specified Post Type
    path('postobjects/detail/<int:post_id>', views.PostObject_Detailview, name="postobject_detail"), # Post Object Detail
    path('posttypes/all', views.PostTypeListView.as_view(), name="posttype_all"), #All Post Types List
    path('postobjects/', views.PostObjectListView.as_view(), name="postobject_all"), #All Post  List
    path('community/edit/<int:community_id>', views.CommunityEdit, name="community_edit"), # Community Edit
    # path("mycommunities/<int:user_id>", views.MyCommunities.as_view(), name="my_communities") , #Joined Communities
    path('community/add/', views.CommunityCreate, name="community_create"), #Community Create URL
    path('posttype/add/<int:community_id>', views.PostTypeCreate, name="posttype_create"), #Post Type Create URl  
    path('posttypeobject/add/<int:post_id>', views.PostTypeObjectCreate, name="posttypeobject_create") #Post Type Object / Post Create URL
]
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
    path('<pk>/', views.Community_PostType_DetailView.as_view(), name="community_posttype_detail"), 
    # path("mycommunities/<int:user_id>", views.MyCommunities.as_view(), name="my_communities"), #Joined Communities
    path('community/add/', views.CommunityCreate, name="community_create"), #Community Create URL
    path('posttype/add/<int:community_id>', views.PostTypeCreate, name="posttype_create"), #Post Type Create URl  
    path('posttypeobject/add/<int:post_id>', views.PostTypeObjectCreate, name="posttypeobject_create") #Post Type Object / Post Create URL
]
from django.urls import path
from . import views
from .views import CommunityDetailView, CommunityListView

app_name = "community"
urlpatterns = [
    path('', views.CommunityListView.as_view(), name='homepage'),
    path("register/", views.UserRegistration, name="register"), #User Registration URL
    path("login/", views.UserLogin, name="login"), #User Login URL
    path("logout/", views.UserLogout, name="logout"), #User Logout URL
    path('wikitag/', views.AddSemanticTag, name="semantic_tag"),#Community Semantic Tag Trial
    path('<pk>/', views.CommunityDetailView.as_view(), name="community_detail" ), 
    path('community/add/', views.CommunityCreate.as_view(), name="community_create"), #Community Create URL
    path('posttype/add/<int:community_id>', views.PostTypeCreate, name="posttype_create"), #Post Type Create URl  
]
from django.db import models
from django.urls import reverse

class Community(models.Model):
    community_name = models.CharField(max_length=100)
    community_description = models.CharField(max_length=200)
    community_tag = models.CharField(max_length=150)

    def get_absolute_url(self):
        return reverse("detail.html", kwargs={"pk" : self.pk})

    def __str__ (self):
        return self.community_name + "--" +self.community_description

class Post(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    post_description = models.CharField(max_length=200)
    post_tag = models.CharField(max_length=150)


    def __str__ (self):
        return self.post_title + "--" + self.post_description

    
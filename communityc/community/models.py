from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import JSONField

class Community(models.Model):
    community_name = models.CharField(max_length=100)
    community_description = models.CharField(max_length=200)
    community_tag = models.CharField(max_length=150)

    def __str__ (self):
        return ("Community ID : " + str(self.id) +  "     " + "Community Name : " + self.community_name)

    def get_absolute_url(self):
         return reverse('community:community_detail', kwargs={"pk" : self.pk})

class Post(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    post_description = models.CharField(max_length=200)
    post_tag = models.CharField(max_length=150)
    formfield = JSONField(default = "") #The Additional/Customizable Data Fields To Be Stored In This Field

    def __str__ (self):
        return ("\nPost id : " + str(self.id) + "\nPost Title : " + self.post_title +  "\nPost Description : " + self.post_description +  "\nPost Tag : "  
                + self.post_tag + "\nPost Community id : " + str(self.community))

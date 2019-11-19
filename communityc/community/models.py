from django.db import models
from django.urls import reverse

class Community(models.Model):
    community_name = models.CharField(max_length=100)
    community_description = models.CharField(max_length=200)
    community_tag = models.CharField(max_length=150)
    #additional_data_structure = models.ManyToManyField("DataStructure")

    def __str__ (self):
        return self.community_name + "--" +self.community_description

    def get_absolute_url(self):
         return reverse('community:community_detail', kwargs={"pk" : self.pk})

class Post(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    post_description = models.CharField(max_length=200)
    post_tag = models.CharField(max_length=150)


    def __str__ (self):
        return self.post_title + "--" + self.post_description

class DataStructure(models.Model):
#Data Structure for Communities & Posts
    Text = "Txt"
    Video = "Video"
    Audio = "Audio"
    Date = "Date"
    EMail = "Email"
    Integer = "Int"
    Decimal = "Dec"
    Location = "Loc"
    URL = "URL"

    data_structures = [
        (Text, "Text"),
        (Video, "Video"),
        (Audio, "Audio"),
        (Date, "Date"),
        (EMail, "E-Mail"),
        (Integer, "Integer"),
        (Decimal, "Decimal"),
        (Location, "Location"),
        (URL, "URL")
    ]

    field_label = models.CharField(max_length=100)
    field_isrequired = models.BooleanField(default=False)
    field_dstructure = models.CharField(max_length=5, choices=data_structures, default=Text)
    #community = models.ForeignKey(Community, on_delete=models.CASCADE)
    
    def __str__ (self):
        return self.field_label + "--" + self.field_dstructure + "--" + self.field_isrequired

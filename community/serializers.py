from rest_framework import serializers
from .models import Post

class post_type_serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["datafields"]
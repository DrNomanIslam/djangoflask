from rest_framework import serializers
from .models import *

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('author_id','first_name', 'last_name','email','highest_qualification')

class ReactSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)

    class Meta:
        model = Publication
        fields = ('authors','title', 'journal','year_of_publication','volume','issue','pp')



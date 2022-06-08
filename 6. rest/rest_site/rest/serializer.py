from rest_framework import serializers
from rest.models import Rest

class RestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rest
        fields = ["task", "completed", "timestamp", "updated", "user"]
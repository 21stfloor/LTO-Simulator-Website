from django.urls import path, include
from system.models import Reviewer, Score
from rest_framework import routers, serializers, viewsets

class ReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviewer
        fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('user', 'score', 'lesson_name', 'time','summary')
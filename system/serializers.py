from django.urls import path, include
from system.models import Question, Reviewer, Score
from rest_framework import routers, serializers, viewsets

class ReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviewer
        fields = ['key', 'picture', 'content', 'order_position']

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('user', 'score', 'lesson_name', 'time','summary')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'category', 'choice1', 'choice2', 'choice3', 'correct_choice']

    def validate(self, data):
        # Check that none of the choices are blank
        if not data.get('choice1') or not data.get('choice2') or not data.get('choice3'):
            raise serializers.ValidationError("All choices must be provided and cannot be blank.")
        
        # Check that the correct_choice is one of the choices
        if data.get('correct_choice') not in [data.get('choice1'), data.get('choice2'), data.get('choice3')]:
            raise serializers.ValidationError("Correct choice must be one of the given choices.")
        
        return data
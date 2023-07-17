from rest_framework import serializers

from .models import Category, Option, Question


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = ['title', 'is_true']


class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    correct_option = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question', 'options', 'correct_option']

    def get_options(self, instance):
        options = instance.option.values('title', 'is_true')
        return options

    def get_correct_option(self, instance):
        correct_option = instance.option.filter(is_true=True).first()
        if correct_option:
            return correct_option.title
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        options = representation.pop('options')
        representation['options'] = [option['title'] for option in options]
        representation['correct_option'] = self.get_correct_option(instance)
        return representation

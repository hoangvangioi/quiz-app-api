from django.http import Http404
from django.shortcuts import render
from rest_framework.generics import ListAPIView, get_object_or_404

from .models import Category, Question
from .serializers import CategorySerializer, QuestionSerializer

# Create your views here.


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class QuestionListAPIView(ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        question_count = self.kwargs['question_count']

        try:
            question_count = int(question_count)
        except ValueError:
            raise Http404('Invalid question_count value')

        category = get_object_or_404(Category, slug=slug)
        qs = Question.objects.filter(category=category).order_by('?')[:question_count]
        return qs

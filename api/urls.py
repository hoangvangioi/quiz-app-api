from django.urls import path, re_path
from .views import CategoryListAPIView, QuestionListAPIView


urlpatterns = [
    path('category', CategoryListAPIView.as_view()),
    re_path(
        r'^category/(?P<slug>[-\w]+)/questions/(?P<question_count>\d+)/$', QuestionListAPIView.as_view()),
]

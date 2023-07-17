from django.contrib import admin

from .models import Category, Option, Question

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'slug', 'created_date')
    list_display_links = ['id', 'name']
    list_filter = ('name', )
    search_fields = ('name',)
    ordering = ['id', 'name', 'created_date']


class OptionInLineModel(admin.TabularInline):
    model = Option
    readonly_fields = ('id',)
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'category']
    list_display_links = ['id', 'question', 'category']
    inlines = [OptionInLineModel]
    list_filter = ['category']


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_true', 'question']
    list_display_links = ['id', 'title']
    list_filter = ['is_true', 'question']

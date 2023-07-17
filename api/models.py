from django.db import IntegrityError, models
from django.db.models import Q, UniqueConstraint
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify

from .utils import unique_slug_generator


class TimeStamp(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Category(TimeStamp):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=False)
        super(Category, self).save(*args, **kwargs)


def pre_save_category_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_category_receiver, sender=Category)


class Question(TimeStamp):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Category', db_index=True)
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 verbose_name='Question', db_index=True, related_name='option')
    title = models.CharField(max_length=255, verbose_name='answer')
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['question'],
                condition=Q(is_true=True),
                name='unique_correct_option'
            )
        ]

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except:
            raise IntegrityError(
                'Only one option can be marked as correct for a question.')

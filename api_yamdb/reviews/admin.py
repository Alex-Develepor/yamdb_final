from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Category, Genre)
class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')
    ordering = ('name', )
    search_fields = ('name', 'slug')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'review', 'pub_date')
    list_display_links = ('id', 'text')
    search_fields = ('text', 'author__username')
    list_filter = ('pub_date',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_display_links = ('id', 'name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'score', 'pub_date')
    list_display_links = ('id', 'author', 'title')
    search_fields = ('author__username', 'title__name')
    list_filter = ('pub_date',)

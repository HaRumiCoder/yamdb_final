from django.contrib import admin
from django.contrib.auth import get_user_model

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'last_name',
        'first_name',
        'role',
        'email'
    )
    list_editable = ('role',)
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)

from django.contrib import admin
from django import forms
from mptt.admin import MPTTModelAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from .models import *

class PostAdminForm(forms.ModelForm):
    intro_text = forms.CharField(widget=CKEditorUploadingWidget())
    full_text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = PostAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'category', 'created_at', 'updated_at', 'get_photo', 'views', 'visible')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'full_text',)
    list_editable = ('visible',)
    list_filter = ('created_at', 'visible', 'tags')
    readonly_fields = ('created_at', 'updated_at', 'get_photo',)
    fields = ('title', 'title_seo', 'slug', 'author', 'category', 'tags', 'description', 'intro_text', 'full_text', 'photo', 'get_photo', 'feature', 'created_at', 'updated_at', 'visible', 'views')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        return 'нет фото'
    get_photo.short_description = 'Изображение'
'''
# описание рецептов блюд
class RubricAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Rubric
        fields = '__all__'

class RubricAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)} # параметр, который позволяет формировать slug из title автоматически
    form = RubricAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'parent', 'description', 'get_photo', 'visible')
    list_display_links = ('id', 'title')
    list_filter = ('title', 'visible',)
    search_fields = ('title', 'description',)
    readonly_fields = ('get_photo',)
    fields = (
    'title', 'title_menu', 'slug', 'description', 'content', 'parent', 'photo', 'get_photo', 'visible')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        return '-'
    get_photo.short_description = 'Изображение'
'''
class CategoryAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Category
        fields = '__all__'

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)} # параметр, который позволяет формировать slug из title автоматически
    form = CategoryAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'title_menu','slug', 'description', 'get_photo', 'visible')
    list_display_links = ('id', 'title')
    list_filter = ('title', 'visible',)
    search_fields = ('title', 'description',)
    readonly_fields = ('get_photo',)
    fields = (
    'title', 'title_menu', 'slug', 'description', 'content', 'photo', 'get_photo', 'visible')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        return '-'
    get_photo.short_description = 'Изображение'


class AuthorAdminForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm
    save_as = True
    list_display = ('id', 'name', 'surname', 'username', 'get_avatara', 'email_address')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name', 'username',)
    readonly_fields = ('get_avatara',)
    fields = ('name', 'surname', 'username', 'avatara', 'get_avatara', 'email_address')

    def get_avatara(self, obj):
        if obj.avatara:
            return mark_safe(f'<img src="{obj.avatara.url}" width="70">')
        return 'нет фото'

class TagAdminForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm
    save_as = True
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('title',)
    fields = ('title', 'slug')

class CommentAdminForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'message', 'name', 'email', 'post', 'created_at', 'active')
    list_display_links = ('id', 'message')
    list_filter = ('active', 'created_at', 'name',)
    search_fields = ('name', 'email', 'bogy',)
    readonly_fields = ('created_at', 'updated')
    fields = ('post', 'name', 'email', 'message', 'website', 'created_at', 'updated', 'active')
    actions = ['approve_comments']
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        return 'нет фото'

# Регистрация моделей

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)

admin.site.site_header = "Администратор портала"
admin.site.site_title = "Интеллектуальные ресурсы"
admin.site.index_title = "Портал 'Виртуальный колледж IRBIS'"



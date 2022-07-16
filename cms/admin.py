from django.contrib import admin
from django.contrib import admin # предоставляет интерфейс администратора по умолчанию
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from .models import *  # импортирует все модели сразу

class RubricAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Rubric
        fields = '__all__'

class RubricAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)} # параметр, который позволяет формировать slug из title автоматически
    form = RubricAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'title_menu','slug', 'description', 'get_photo', 'visible')
    list_display_links = ('id', 'title')
    list_filter = ('title', 'visible',)
    search_fields = ('title', 'description',)
    readonly_fields = ('get_photo',)
    fields = ('title', 'title_menu', 'slug', 'description', 'content', 'photo', 'get_photo', 'visible')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        return '-'

class PageAdminForm(forms.ModelForm):
    intro_text = forms.CharField(widget=CKEditorUploadingWidget())
    full_text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Page
        fields = '__all__'

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = PageAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'rubric', 'created_at', 'get_photo', 'views', 'visible')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'full_text',)
    list_editable = ('visible',)
    list_filter = ('created_at', 'visible')
    readonly_fields = ('created_at', 'updated_at', 'get_photo',)
    fields = ('title', 'title_seo', 'slug', 'rubric', 'description', 'intro_text', 'full_text', 'photo', 'get_photo', 'created_at',
              'updated_at', 'views', 'visible', 'feature')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        return 'нет фото'
    get_photo.short_description = 'Изображение'


class ServiceAdminForm(forms.ModelForm):
    intro_text = forms.CharField(widget=CKEditorUploadingWidget())
    full_text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Service
        fields = '__all__'

class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = ServiceAdminForm
    save_as = True
    save_on_top = True
    list_display = ('id', 'title', 'slug', 'created_at', 'updated_at', 'get_photo', 'views', 'visible')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'full_text',)
    list_editable = ('visible',)
    list_filter = ('created_at', 'visible')
    readonly_fields = ('created_at', 'updated_at', 'get_photo',)
    fields = ('title', 'slug', 'description', 'intro_text', 'full_text', 'photo', 'get_photo', 'created_at', 'updated_at', 'visible', 'views')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        return 'нет фото'
    get_photo.short_description = 'Изображение'

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

class ContactAdminForm(forms.ModelForm):
    intro_text = forms.CharField(widget=CKEditorUploadingWidget())
    full_text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Contact
        fields = '__all__'

class ContactAdmin(admin.ModelAdmin):
    form = ContactAdminForm
    save_as = True
    prepopulated_fields = {"email": ("first_name",)}
    list_display = ('id', 'first_name', 'email')
    list_display_links = ('id', 'first_name')
    search_fields = ('first_name',)
    list_filter = ('first_name',)
    fields = ('first_name', 'last_name', 'email', 'message')

# Регистрация моделей
admin.site.register(Rubric, RubricAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Contact, ContactAdmin)



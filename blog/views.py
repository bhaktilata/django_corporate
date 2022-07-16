from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from .models import Category, Post, Author, Comment, Tag
from django.db.models import F  # класс  F для работы с Model API
from .forms import CommentForm, PostForm
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
#from django.views.decorators.cache import cache_page
from django.urls import reverse_lazy

def get_blog(request):
    return render(request, 'blog/index.html')


class GetCategory(ListView):  # выводит список категорий
    model = Category
    template_name = 'blog/categories.html'
    context_object_name = 'category_blog'
    paginate_by = 5

    def get_queryset(self):
        return Category.objects.filter(visible=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Путь духовного воина'
        return context

class PostByCategory(ListView):  # выводит список статей выбранной категории
    template_name = 'blog/post_list_category.html'
    context_object_name = 'posts_list'
    paginate_by = 5
    allow_empty = True  # ошибка 404 при несуществующей категории

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'], visible=True).select_related(
            'author')  # обращается к полю 'slug' связанной модели category, который получается в маршруте
        # поэтому здесь выводятся статьи только выбранной категории

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context
'''
class GetPost(DetailView):  # выводит полную страницк
    model = Post
    template_name = 'blog/single-post.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(visible=True)  # управляет выводом опубликованных материалов

    def get_context_data(self, *, object_list=None, **kwargs):  # в контексте мы не только задавать title, но и выполнять некоторые действия с данными
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1                # извлекает значение из поля таблицы views, увеличивет на едеицу
        self.object.save()                                #  и снова сохраняем в таблицу
        self.object.refresh_from_db()                     # поскольку теперь в object содержится выражение F(views) + Value(1), то мы перезапрашиваем данные непосредственно из БД
        return context

'''
'''
class CreateComment(CreateView):
#class CreateComment(DetailView):
    model = Comment
    form_class = CommentForm
    success_msg = 'Комментарий успешно создан, ожидайте модерации'

    def get_success_url(self):
        return reverse_lazy('post_single', kwargs={'slug': self.get_object().slug})

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('slug')
        #form.instance.post_id = self.kwargs.get('slug') # по post_id в таблице комментариев получает slug статьи
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()
'''
class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.slug)


class GetPost(CustomSuccessMessageMixin, FormMixin, DetailView):  # выводит полную статью CustomSuccessMessageMixin,
    model = Post
    template_name = 'blog/single-post.html'
    context_object_name = 'get_post'
    #slug_url_kwarg = 'post_slug'
    form_class = CommentForm
    success_msg = 'Комментарий успешно создан, ожидайте модерации!'

    def get_success_url(self, **kwargs):
        return reverse_lazy('post_single', kwargs={'slug': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object() # данные о статье находится в get_object() и это можно проверить
        self.object.author = self.request.user # информация об авторе находятся в request
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Материалы по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        # context['form'] = CommentForm()
        self.object.views = F('views') + 1  # извлекает значение из поля таблицы views, увеличивет на едеицу
        self.object.save()  # и снова сохраняем в таблицу
        self.object.refresh_from_db()  # поскольку теперь в object содержится выражение F(views) + Value(1), то мы перезапрашиваем данные непосредственно из БД
        return context

    def get_context_data(self, *, object_list=None,
                         **kwargs):  # в контексте мы не только задавать title, но и выполнять некоторые действия с данными
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        self.object.views = F('views') + 1  # извлекает значение из поля таблицы views, увеличивет на едеицу
        self.object.save()  # и снова сохраняем в таблицу
        self.object.refresh_from_db()  # поскольку теперь в object содержится выражение F(views) + Value(1), то мы перезапрашиваем данные непосредственно из БД
        return context



class PostsByTag(ListView):  # Выводит материалы по тегу
    template_name = 'blog/post_tag_list.html'
    context_object_name = 'post_tag'
    paginate_by = 6
    allow_empty = True

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'по тэгу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['title'] = 'Поиск по сайту'
        return context

def  get_author(request):
    return render(request, 'blog/author.html')

def get_blog(request):
    return render(request, 'blog/index.html')

def page_not_found_view(request, exception):
    return render(request, 'blog/404.html', status=404)


def get_error(request):
    return render(request, 'blog/404.html')


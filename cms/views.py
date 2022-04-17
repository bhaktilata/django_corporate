from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Rubric, Page
from django.contrib import messages

def index(request):
    return render(request, 'cms/index.html')

class PageByRubric(ListView):    # выводит список статей выбранной категории
    template_name = 'cms/page_list_rubric.html'
    context_object_name = 'page_list'
    paginate_by = 6
    allow_empty = True # ошибка 404 при несуществующей категории

    def get_queryset(self):
        #return Post.objects.filter(visible=True) # управляет выводом опубликованных всех материалов всех категорий
        return Page.objects.filter(rubric__slug=self.kwargs['slug'], visible=True).select_related('author') # обращается к полю 'slug' связанной модели category, который получается в маршруте
                                                                       # поэтому здесь выводятся статьи только выбранной категории

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Rubric.objects.get(slug=self.kwargs['slug']) # извлекаем title, название текущей категории по слагу благодаря связанным моделям
        return context


class GetPage(DetailView):  # выводит полную страницу
    model = Page
    template_name = 'cms/page.html'
    context_object_name = 'page_single'

    def get_queryset(self):
        return Page.objects.filter(visible=True)  # управляет выводом опубликованных материалов

    def get_context_data(self, *, object_list=None, **kwargs):  # в контексте мы не только задавать title, но и выполнять некоторые действия с данными
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1                # извлекает значение из поля таблицы views, увеличивет на едеицу
        self.object.save()                                #  и снова сохраняем в таблицу
        self.object.refresh_from_db()                     # поскольку теперь в object содержится выражение F(views) + Value(1), то мы перезапрашиваем данные непосредственно из БД
        return context



class Portfolio(ListView):  # выводит список материалов раздела портфолио
    template_name = 'portal/portfolio_list.html'
    context_object_name = 'portfolio_list'
    paginate_by = 3
    allow_empty = False  # ошибка 404 при несуществующей категории

    def get_queryset(self):
        return Portfolio.objects.filter(visible=True) # управляет выводом опубликованных всех материалов

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Портфолио Maha Deva'
        return context


def get_rubric(request):
    return render(request, 'cms/get_rubric.html', {'get_rubric': Rubric.objects.all()})
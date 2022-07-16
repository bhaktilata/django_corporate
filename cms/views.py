from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Page, Rubric, Service, Portfolio, Tag, Contact
from django.db.models import F      # класс  F для работы с Model API
from .forms import ContactForm
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from django.core.mail import send_mail
from blog.models import Post
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.urls import reverse_lazy

def Home(request):
    return render(request, 'cms/index.html')

class GetRubric(ListView):    # выводит список рубрик страниц: about, service, portfolio
    model = Rubric
    template_name = 'cms/rubric_list.html'
    context_object_name = 'rubric_blog'
    paginate_by = 2

    def get_queryset(self):
        return Rubric.objects.filter(visible=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Путь духовного воина'
        return context

class PageByRubric(ListView):    # выводит список страниц выбранной рубрики
    template_name = 'cms/page_list_rubric.html'
    context_object_name = 'pages_list'
    paginate_by = 6
    allow_empty = True # ошибка 404 при несуществующей категории

    def get_queryset(self):
        #return Post.objects.filter(visible=True) # управляет выводом опубликованных всех материалов всех категорий
        return Page.objects.filter(category__slug=self.kwargs['slug'], visible=True) # обращается к полю 'slug' связанной модели category, который получается в маршруте
                                                                       # поэтому здесь выводятся статьи только выбранной категории

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Rubric.objects.get(slug=self.kwargs['slug']) # извлекаем title, название текущей категории по слагу благодаря связанным моделям
        return context

class GetPage(DetailView):  # выводит полную страницк
    model = Page
    template_name = 'cms/page.html'
    context_object_name = 'page'

    def get_queryset(self):
        return Page.objects.filter(visible=True)  # управляет выводом опубликованных материалов

    def get_context_data(self, *, object_list=None, **kwargs):  # в контексте мы не только задавать title, но и выполнять некоторые действия с данными
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1                # извлекает значение из поля таблицы views, увеличивет на едеицу
        self.object.save()                                #  и снова сохраняем в таблицу
        self.object.refresh_from_db()                     # поскольку теперь в object содержится выражение F(views) + Value(1), то мы перезапрашиваем данные непосредственно из БД
        return context
'''
class GetService(ListView):    # выводит список категорий
    model = Service
    template_name = 'cms/service.html'
    context_object_name = 'service_blog'
    paginate_by = 2
    allow_empty = True

    def get_queryset(self):
        return Service.objects.filter(visible=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Путь духовного воина'
        return context

'''
class GetService(ListView):  # выводит список материалов раздела сервис
    #template_name = 'portal/service_list.html'
    template_name = 'cms/service_list.html'
    context_object_name = 'services_list'
    paginate_by = 3
    allow_empty = True

    def get_queryset(self):
        return Service.objects.filter(visible=True)  # управляет выводом опубликованных материалов

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['title'] = 'Материалы по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context

class GetPortfolio(ListView):  # выводит список материалов раздела сервис
    template_name = 'cms/portfolio_list.html'
    context_object_name = 'portfolio_list'
    paginate_by = 3
    allow_empty = True

    def get_queryset(self):
        return Portfolio.objects.filter(visible=True)  # управляет выводом опубликованных материалов

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['title'] = 'Материалы по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context

class Search(ListView):
    template_name = 'cms/search.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        context['kayword'] = f"{self.request.GET.get('s')}"
        context['title'] = 'Поиск по сайту'
        return context

def get_contact(request):
    model = Contact
    form_class = ContactForm
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            }
            message = "\n\n".join(body.values())
            mail = send_mail(form.cleaned_data['subject'], message,
                          'admin@inicons.ru',
                          ['bvlata@mail.ru'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо успешно отправлено!')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки сообщения!')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = ContactForm()
    return render(request, 'cms/feedback.html', {"form": form})

'''
class ContactCreate(CreateView):
    model = Contact
    template_name = 'cms/feedback.html'
    success_url = reverse_lazy('success_page')
    error_url = reverse_lazy('error_page')
    form_class = ContactForm

    def form_valid(self, form):
        # Формируем сообщение для отправки администратору
        data = form.data
        subject = f'"IRBIS Colledj", отправитель: {data["first_name"]} {data["last_name"]}, почта: {data["email"]}'
        mail(subject, data['message'])
        return super().form_valid(form)

# Функция отправки сообщения
def mail(subject, content):
    send_mail(subject,
        content,
        'admin@inicons.ru',
        ['bvlata@mail.ru']
    )

# Функция, которая вернет сообщение в случае успешного заполнения формы
def success(request):
   messages.success(request, 'Письмо успешно отправлено!')
   return redirect('contact')
    
'''
'''
def post_mailing(request, slug):
    # Получить сообщение по идентификатору
    post = get_object_or_404(Post, slug=slug, visible='True')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} рекомендует вам прочитать {post.title}"
            message = f"Прочтите {post.title} в {post_url}\n\n" \
                      f"{cd['name']} Поделился комментарием к статье: {cd['comments']}"
            send_mail(subject, message, 'admin@inicons.ru', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'cms/share.html', {'post': post,
                                                 'form': form,
                                                 'sent': sent})
 '''
class StaticViewSitemap(Sitemap):
    def items(self):
        return ['about']

    def location(self, item):
        return reverse(item)

class DynamicViewSitemap(Sitemap):
    def items(self):
        return Post.objects.all()

    def location(self, item):
        # return reverse('news-page', args=[item.pk])
        return f'/post/{item.slug}/'

def get_about(request):
    return render(request, 'cms/about.html')

def get_service(request):
    return render(request, 'cms/service.html')

def page_not_found_view(request, exception):
    return render(request, 'cms/404.html', status=404)

def get_error(request):
    return render(request, 'cms/404.html')

def get_subscribe(request):
    return render(request, 'cms/subscribe.html')
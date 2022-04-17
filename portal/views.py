from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Category, Post, Tag, Comment
from django.db.models import F      # класс  F для работы с Model API
from .forms import UserRegisterForm, UserLoginForm, ContactForm, CommentForm, EmailPostForm
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
#from django.views.decorators.cache import cache_page
from .models import Category


def index(request):
    return render(request, 'portal/index.html')

class Home(ListView):
    model = Post
    template_name = 'portal/index.html'
    context_object_name = 'latest_news'

    def get_queryset(self):
        return Post.objects.filter(visible=True)  # управляет выводом опубликованных материалов

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Персональный сайт Maha Deva'
        return context

class GetCategory(ListView):    # выводит список категорий
    model = Category
    template_name = 'portal/categories.html'
    context_object_name = 'category_blog'
    paginate_by = 2

    def get_queryset(self):
        return Category.objects.filter(visible=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Путь духовного воина'
        return context

class PostByCategory(ListView):    # выводит список статей выбранной категории
    template_name = 'portal/post_list_category.html'
    context_object_name = 'posts_list'
    paginate_by = 6
    allow_empty = True # ошибка 404 при несуществующей категории

    def get_queryset(self):
        #return Post.objects.filter(visible=True) # управляет выводом опубликованных всех материалов всех категорий
        return Post.objects.filter(category__slug=self.kwargs['slug'], visible=True).select_related('author') # обращается к полю 'slug' связанной модели category, который получается в маршруте
                                                                       # поэтому здесь выводятся статьи только выбранной категории

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug']) # извлекаем title, название текущей категории по слагу благодаря связанным моделям
        return context

class PostByBlog(ListView):  # выводит список статей блога
    template_name = 'portal/post_list.html'
    context_object_name = 'post'
    paginate_by = 2
    allow_empty = False  # ошибка 404 при несуществующей категории

    def get_queryset(self):
        return Post.objects.filter(visible=True) # управляет выводом опубликованных материалов

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог Maha Deva'
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


class GetPost(DetailView):  # выводит полную статью
    model = Post
    template_name = 'portal/single-sidebar.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(visible=True)  # управляет выводом опубликованных материалов

    def get_context_data(self, *, object_list=None, **kwargs):  # в контексте мы не только задавать title, но и выполнять некоторые действия с данными
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1                # извлекает значение из поля таблицы views, увеличивет на едеицу
        self.object.save()                                #  и снова сохраняем в таблицу
        self.object.refresh_from_db()                     # поскольку теперь в object содержится выражение F(views) + Value(1), то мы перезапрашиваем данные непосредственно из БД
        return context

class GetService(ListView):  # выводит список материалов раздела сервис
    #template_name = 'portal/service_list.html'
    template_name = 'portal/single-sidebar.html'
    context_object_name = 'services_list'
    paginate_by = 3
    allow_empty = True

    def get_queryset(self):
        return Post.objects.filter(visible=True)  # управляет выводом опубликованных материалов

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['title'] = 'Материалы по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class PostsByTag(ListView):  # Выводит материалы по тегу
    template_name = 'portal/post_tag_list.html'
    context_object_name = 'post_tag'
    paginate_by = 6
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'по тегу: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class Search(ListView):
    template_name = 'portal/search.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('search')) # получаем в виде параметра запрос в форме поиска из поля с имнем name="search"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = f"search={self.request.GET.get('search')}&"
        context['title'] = 'Поиск по сайту'
        return context

#@cache_page(60)
def post_comment(request, slug):               # функция для создания комментарий
    #form_class =  CommentForm
    #template_name = 'portal/post_single.html'
    template_name = 'portal/single-sidebar.html'
    post = get_object_or_404(Post, slug=slug) # назначаем переменной 'post' все данные объекта Post, выбираемого по слагу
    comments = post.comments.filter(active=True) # извлекает из базы данных все одобренные комментарии
    # Поскольку это та же самая страница, на которой пользователи будут создавать новые комментарии, мы инициализировали
    # переменную new_comment, установив для нее значение none.
    new_comment = None
    # Comment posted

    if request.method == 'POST': # переменная comment_form будет содержать данные пользовательского ввода
        comment_form = CommentForm(data=request.POST) # создаем экземпляр класса формы комметнраия
        if comment_form.is_valid():
            # Создаем новый объект комментария Comment, вызывая метод формы save(), присваимваем его переменной new_comment,
            # но пока не сохранять в базе данных, потому что нам все еще нужно связать его с объектом сообщения (статьей)
            new_comment = comment_form.save(commit=False)
            # привязываем объект комментария к текущему посту
            new_comment.post = post
            # Сохраните объект (комментарий) в базе данных
            new_comment.save()
            messages.success(request, 'Вы успешно отправили ваше сообщение и ожидает модерации')
            return redirect('home')
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-visible')[:3]
    return render(request, template_name, {'post': post,
                                           'comments': comments,  # выводит список комментарий
                                           'new_comment': new_comment, # выводит новый комментарий
                                           'comment_form': comment_form, # выводит форму омментарий
                                           'similar_posts': similar_posts
    })

def get_about(request):
    return render(request, 'portal/about.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) # создаем экземпляр формы и заполняем данными из POST (формы), затем передаем в контекст
        if form.is_valid():
            user = form.save()        # если форма валидна, то объект пользователя сохраеняем в переменной user
            login(request, user)      # и сразу вызываем метод login, передав ему request  и полученного прользовател для его авторизации, поэтому пользователю не придется авторизоваться
            messages.success(request, 'Вы успешно зарегистрировались') # используем компонет джанго messages об успехе, выводится в base.html перед контентом
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()      # иначе показываем не связанную с данными форму (пустая)
    return render(request, 'portal/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()   # получаем пользователя из формы
            login(request, user)      # передаем user в метод login
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'portal/login.html', {"form": form})

def user_logout(request):
    logout(request)
    return redirect('login')

def get_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            body = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }
            message = "\n\n".join(body.values())
            mail = send_mail(form.cleaned_data['subject'], message,
                          'admin@inicons.ru',
                          ['bvlata@mail.ru'])
            if mail:
                messages.success(request, 'Письмо успешно отправлено!')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = ContactForm()
    return render(request, 'portal/feedback.html', {"form": form})

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
    return render(request, 'portal/share.html', {'post': post,
                                                 'form': form,
                                                 'sent': sent})

def page_not_found_view(request, exception):
    return render(request, 'portal/404.html', status=404)

def get_error(request):
    return render(request, 'portal/404.html')
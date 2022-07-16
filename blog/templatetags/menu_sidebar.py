from django import template #нужен для регистрации шаблонного тега
from blog.models import Category, Post

register = template.Library() #тут мы присваем значение

@register.inclusion_tag('blog/menu_tpl.html')  #декоратор для регистрации шаблона для подключения (я его указал в папке templates
def show_menu():
    categories = Category.objects.all()
    return {"categories": categories}


'''
@register.inclusion_tag('portal/menu_tpl.html')  #декоратор для регистрации шаблона для подключения (я его указал в папке templates
def show_page(menu_class='collapse navbar-collapse'):
    pages = Page.objects.all()
    return {"pages": pages}
'''
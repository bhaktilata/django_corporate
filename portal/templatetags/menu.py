from django import template #нужен для регистрации шаблонного тега
from portal.models import Category
from cms.models import Page

register = template.Library() #тут мы присваем значение

@register.inclusion_tag('portal/menu_tpl.html')  #декоратор для регистрации шаблона для подключения (я его указал в папке templates
def show_menu(menu_class='collapse navbar-collapse'):
    categories = Category.objects.all()
    return {"categories": categories}
'''
@register.inclusion_tag('portal/menu_tpl.html')  #декоратор для регистрации шаблона для подключения (я его указал в папке templates
def show_page(menu_class='collapse navbar-collapse'):
    pages = Page.objects.all()
    return {"pages": pages}
'''

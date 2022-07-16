from django import template #нужен для регистрации шаблонного тега
#from cms.models import Category

register = template.Library() #тут мы присваем значение

#@register.inclusion_tag('cms/menu_tpl.html')  #декоратор для регистрации шаблона для подключения (я его указал в папке templates
#def show_menu(menu_class='collapse navbar-collapse'):
#    categories = Category.objects.all()
#    return {"categories": categories, "menu_class": menu_class}

#@register.inclusion_tag('portal/top_menu_tpl.html')
#def show_rubrics(menu_class='collapse navbar-collapse'):
#    rubrics = Rubric.objects.all()
#    return {"rubrics": rubrics, "menu_class": menu_class}


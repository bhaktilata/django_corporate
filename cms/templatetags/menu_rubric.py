from django import template #нужен для регистрации шаблонного тега
from cms.models import Rubric

register = template.Library() #тут мы присваем значение

@register.inclusion_tag('cms/menu_tpl.html')  #декоратор для регистрации шаблона для подключения (я его указал в папке templates
def show_rubric(menu_class='collapse navbar-collapse'):
    rubrics = Rubric.objects.all()
    return {"rubrics": rubrics}

#@register.inclusion_tag('portal/top_menu_tpl.html')
#def show_rubrics(menu_class='collapse navbar-collapse'):
#    rubrics = Rubric.objects.all()
#    return {"rubrics": rubrics, "menu_class": menu_class}


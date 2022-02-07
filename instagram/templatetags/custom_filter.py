from django import template

register = template.Library()


@register.filter(name='get_url_pk')
def get_url_pk(str_url):
    """ url path 에서 pk를 추출 """

    return str_url.split('/')[-1]


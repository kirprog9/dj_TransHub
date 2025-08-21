from django.db.models import Count
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from transport.models import Transport
from main.models import Frozen

from .models import *

menu = [{'title': "О сайті", 'url_name': 'about'},
        {'title': "О перевезеннях", 'url_name': 'about_cargo'},
        {'title': "Зворотній зв'язок", 'url_name': 'contact'},
]
class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        return context

class DataMixin2:
    def get_user_context(self, **kwargs):
        context = kwargs
        id_user = self.request.user.pk

        transport = Transport.objects.filter(author=id_user, published=True, status='Search')

        context['user_transport'] = transport

        return context

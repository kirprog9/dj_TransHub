from django.db.models import Count
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from .models import *


menu = [{'title': "О сайті", 'url_name': 'about'},
        {'title': "О перевезеннях", 'url_name': 'about_cargo'},
        {'title': "Зворотній зв'язок", 'url_name': 'contact'},
]

class DataMixin:
    def get_user_context(self,**kwargs):
        context = kwargs
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        user_id = self.request.user.pk

        countrev = Review.objects.annotate(Count('target_user')).filter(target_user=user_id)
        countcom = Complaint.objects.annotate(Count('target_user')).filter(target_user=user_id)
        context['countrev'] = countrev
        context['countcom'] = countcom
        context['menu'] = user_menu
        if 'cat_selected' not in context:
            context['cat_selected']=0
        return context


class ProfileMixin:
    def get_user_context(self,**kwargs):
        context = kwargs
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        user_id = self.request.user.pk

        context['rev_my'] = Review.objects.filter(user=user_id).select_related("user", "target_user")
        context['rev_for_me'] = Review.objects.filter(target_user=user_id).select_related("user", "target_user")
        context['com_my'] = Complaint.objects.filter(user=user_id).select_related("user", "target_user")
        context['com_for_me'] = Complaint.objects.filter(target_user=user_id).select_related("user", "target_user")

        context['menu'] = user_menu
        if 'cat_selected' not in context:
            context['cat_selected']=0
        return context


class Rev_Com_Mixin:
    def get_user_context(self,**kwargs):
        context = kwargs
        user_menu = menu.copy()

        user_id = self.request.user.pk

        context['menu'] = user_menu
        if 'cat_selected' not in context:
            context['cat_selected']=0
        return context
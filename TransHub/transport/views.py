from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView, UpdateView
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from .utils import *
from .models import *
from .forms import *
from main.models import City, Region


def load_regions(request):
    country_id = request.GET.get('country_id')
    if country_id:
        regions = Region.objects.filter(country_id=country_id).order_by('name')
        return render(request, 'transport/region_dropdown_list_options.html', {'regions': regions})
    return render(request, 'transport/region_dropdown_list_options.html', {'regions': Region.objects.none()})


def load_cities(request):
    region_id = request.GET.get('region_id')
    if region_id:
        cities = City.objects.filter(region_id=region_id).order_by('name')
        return render(request, 'transport/city_dropdown_list_options.html', {'cities': cities})
    return render(request, 'transport/city_dropdown_list_options.html', {'cities': City.objects.none()})


class AddTransport(LoginRequiredMixin, DataMixin, CreateView):
    form_class = TransportForm
    template_name = 'transport/add_transport.html'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Додати транспорт')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('transport:my_transport')


class AllTransport(LoginRequiredMixin, DataMixin, ListView):
    paginate_by = 50
    model = Transport
    template_name = 'transport/all_transport.html'
    form_class = TranportFilterForm
    context_object_name = 'transports'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Пошук Транспорту')
        form = self.form_class(self.request.GET or None)
        context['form'] = form
        return dict(list(context.items())+list(c_def.items()))

    def get_queryset(self):
        queryset = Transport.objects.order_by('-updated_at').filter(published=True, status='Search',freeze=False).exclude(
            author_id=self.request.user.pk).select_related("author").prefetch_related('body_type', 'load_unload', 'permissions')
        form = self.form_class(self.request.GET or None)

        # Якщо форма валідна, застосовуємо фільтри
        if form.is_valid():
            country_from = form.cleaned_data.get('country_from')
            region_from = form.cleaned_data.get('region_from')
            city_from = form.cleaned_data.get('city_from')
            country_to = form.cleaned_data.get('country_to')
            region_to = form.cleaned_data.get('region_to')
            city_to = form.cleaned_data.get('city_to')
            weight_max = form.cleaned_data.get('weight_max')
            volume_max = form.cleaned_data.get('volume_max')
            body_type = form.cleaned_data.get('body_type')
            load_unload = form.cleaned_data.get('load_unload')

            # Применение фильтров на основе заполненных полей
            if country_from:
                queryset = queryset.filter(country_from=country_from)
            if region_from:
                queryset = queryset.filter(region_from=region_from)
            if city_from:
                queryset = queryset.filter(city_from=city_from)
            if country_to:
                queryset = queryset.filter(country_to=country_to)
            if region_to:
                queryset = queryset.filter(region_to=region_to)
            if city_to:
                queryset = queryset.filter(city_to=city_to)
            if weight_max:
                queryset = queryset.filter(weight_max__lte=weight_max)
            if volume_max:
                queryset = queryset.filter(volume_max__lte=volume_max)
            if body_type:
                queryset = queryset.filter(body_type__in=body_type)
            if load_unload:
                queryset = queryset.filter(load_unload__in=load_unload)

        return queryset


class MYTransport(LoginRequiredMixin, DataMixin, ListView):
    paginate_by = 50
    model = Transport
    template_name = 'transport/my_transport2.html'
    context_object_name = 'transports'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Мій транспорт')
        return dict(list(context.items())+list(c_def.items()))

    def get_queryset(self):
        id_user = self.request.user.pk
        return Transport.objects.filter(author=id_user).order_by('-status','published','-updated_at' ).prefetch_related('body_type','load_unload','permissions')


class Transport_update(LoginRequiredMixin,DataMixin, UpdateView):
    model = Transport
    form_class = TransportForm
    template_name = 'transport/add_transport.html'

    def get_object(self, queryset=None):
        transport = super().get_object(queryset)
        if transport.author != self.request.user:
            raise Http404("Transport not found.")
        return transport

    def get_success_url(self):
        return reverse_lazy('transport:my_transport')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Оновити Інформацію про Транспорт')
        return dict(list(context.items())+list(c_def.items()))

class ShowTr(LoginRequiredMixin, DataMixin, DetailView):
    model = Transport
    template_name = 'transport/one_transport.html'
    pk_url_kwarg = 'tr_pk'
    context_object_name = 'transport'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['transport'])
        return dict(list(context.items()) + list(c_def.items()))

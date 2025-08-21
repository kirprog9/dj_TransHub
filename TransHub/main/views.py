from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import *
from .utils import *
import math

from django.http import FileResponse, Http404
import os



class Home(DataMixin, TemplateView):
    template_name = 'main/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Головна Сторінка')
        return dict(list(context.items())+list(c_def.items()))

def logout_user(request):
    logout(request)
    return redirect('home')


class MainLogin(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'main/log_good.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Головна сторінка')
        return dict(list(context.items())+list(c_def.items()))


class About(DataMixin, TemplateView):
    template_name = 'main/about.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Про сайт')
        return dict(list(context.items())+list(c_def.items()))

class About_Cargo(DataMixin, TemplateView):
    template_name = 'main/about_cargo.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О перевезеннях')
        return dict(list(context.items())+list(c_def.items()))

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'main/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Зворотний зв'язок")
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


def take_cargo(request):
    cargo_id = request.POST.get('cargo_id')
    cargo = get_object_or_404(Cargo, id=cargo_id)
    frozen = get_object_or_404(Frozen, cargo=cargo)

    Event.objects.create(cargo=frozen.cargo, transport=frozen.transport,arrived=False)

    frozen.cargo.freeze = False
    frozen.transport.freeze = False
    frozen.cargo.status = "IN_TRANSIT"
    frozen.transport.status = 'IN_TRANSIT'
    frozen.cargo.save()
    frozen.transport.save()
    frozen.delete()

    return redirect('cargo:my_cargo')


def freeze_cargo_tr(request):
    cargo_id = request.POST.get('cargo_id')
    cargo = get_object_or_404(Cargo, id=cargo_id)
    transport_id = request.POST.get('transport_id')
    transport = get_object_or_404(Transport, id=transport_id, author=request.user)

    fr = Frozen.objects.create(
        cargo=cargo,
        transport=transport,
    )

    cargo.freeze = True
    transport.freeze = True
    cargo.save()
    transport.save()

    return redirect('transport:my_transport')

def un_freeze_cargo_tr(request):
    cargo_id = request.POST.get('cargo_id')
    cargo = get_object_or_404(Cargo, id=cargo_id)
    frozen = get_object_or_404(Frozen, cargo=cargo)

    frozen.cargo.freeze = False
    frozen.transport.freeze = False
    cargo.save()
    frozen.cargo.save()
    frozen.transport.save()

    frozen.delete()

    return redirect('cargo:my_cargo')
def un_freeze_tr(request):
    transport_id = request.POST.get('cargo_id')
    transport = get_object_or_404(Transport, id=transport_id)
    frozen = get_object_or_404(Frozen, transport=transport)

    frozen.cargo.freeze = False
    frozen.transport.freeze = False
    frozen.cargo.save()
    frozen.transport.save()

    frozen.delete()

    return redirect('transport:my_transport')

def delivered_cargo(request):
    cargo_id = request.POST.get('cargo_id')
    cargo = get_object_or_404(Cargo, id=cargo_id)
    event = get_object_or_404(Event, cargo=cargo)

    event.cargo.status = "DELIVERED"
    event.transport.status = 'Search'
    event.cargo.save()
    event.transport.save()
    event.arrived = True
    event.save()

    return redirect('cargo:my_cargo')


def create_docs(request):
    ev_id = request.POST.get('ev_id')
    event = get_object_or_404(Event, id=ev_id)

    car = event.cargo
    tr = event.transport
    replacements = {
        "[company_cargo]": car.author.name_company,
        "[cargo_fio]": f"{car.author.first_name} {car.author.last_name} {car.author.third_name}",
        "[company_transport]": tr.author.name_company,
        "[from]": f"{car.city_from}",
        "[to]": f"{car.city_to}",
        "[type]": tr.model,
        "[nomer]": tr.license_plate,
        "[nomer_act]": f'{event.id:07}',

        "[data]": event.event_date.strftime("%d.%m.%Y"),

        "[amaunt]": f'{car.amount}',
        "[amaunt_type]": f'_{car.currency}',
        "[transport_short_fio]": f" {tr.author.last_name} {tr.author.first_name[0]}. {tr.author.third_name[0]}.",
        "[cargo_short_fio]": f" {car.author.last_name} {car.author.first_name[0]}. {car.author.third_name[0]}.",
    }

    replace_docs(replacements, event.act_file)
    replace2_docs(replacements, event.invoice_file)
    return redirect('my_doc')

class MYDoc(LoginRequiredMixin, DataMixin, ListView):
    model = Event
    template_name = 'main/my_doc.html'
    context_object_name = 'events'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Мої документи')
        user_id = self.request.user.pk

        events_as_cargo_author = Event.objects.filter(cargo__author=user_id)
        events_as_transport_author = Event.objects.filter(transport__author=user_id)
        context.update({
            'events_as_cargo_author': events_as_cargo_author,
            'events_as_transport_author': events_as_transport_author,
            **c_def
        })
        return context


def download_file(request, file_type, event_id):
    event = get_object_or_404(Event, id=event_id)

    if file_type == 'act' and event.act_file:
        file_path = event.act_file.path
    elif file_type == 'invoice' and event.invoice_file:
        file_path = event.invoice_file.path
    else:
        raise Http404("Файл не знайден.")

    if not os.path.exists(file_path):
        raise Http404("Файл не знайден.")

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
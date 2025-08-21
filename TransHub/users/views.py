from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.db.models import Count, Q, F

from .models import *
from main.models import Event
from .forms import *
from .utils import *
# Create your views here.

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Реєстрація')
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    context_object_name = 'users'
    template_name = 'users/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизація')
        return dict(list(context.items())+list(c_def.items()))


def logout_user(request):
    logout(request)
    return redirect('home')

class ProfileUser(LoginRequiredMixin,DataMixin,UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'

    def get_object(self):
        return self.request.user
    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Профіль')
        return dict(list(context.items())+list(c_def.items()))

class ProfilesUser(LoginRequiredMixin,DataMixin, ListView):
    model = get_user_model()
    template_name = 'users/profiles.html'
    context_object_name = 'users'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Профілі')
        return dict(list(context.items())+list(c_def.items()))

    def get_queryset(self):
        return get_user_model().objects.all()

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"


class ReviewView(LoginRequiredMixin,DataMixin, CreateView):
    form_class = ReviewForm
    template_name = 'users/rev_add.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Відгук')
        return dict(list(context.items())+list(c_def.items()))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        w = form.save(commit=False)
        w.user = self.request.user
        return super().form_valid(form)


class ComplaintView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = ComplaintForm
    template_name = 'users/com_add.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Скарга')
        return dict(list(context.items())+list(c_def.items()))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        w = form.save(commit=False)
        w.user = self.request.user
        return super().form_valid(form)


def user_list(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(models.Q(username__icontains=query) | models.Q(email__icontains=query))
    else:
        users = User.objects.all()

    users = users.annotate(
        ev_count=Count("author__event_cargo", distinct=True)+Count("author1__event_transport", distinct=True),
        review_count=Count('rev_target_user', distinct=True),
        complaint_count=Count('com_target_user', distinct=True)
    )
    return render(request, 'users/user_list.html', {'users': users})


def user_detail(request, user_id):
    user2 = get_object_or_404(User, id=user_id)
    reviews = Review.objects.filter(target_user=user2)
    claims = Complaint.objects.filter(target_user=user2)  # Предполагаем, что поле связи с User называется `user`
    ev_count = Event.objects.filter(cargo__author=user2).count() + Event.objects.filter(transport__author=user2).count()
    return render(request, 'users/user_detail.html', {
        'user2': user2,
        'reviews': reviews,
        'claims': claims,
        'ev_count': ev_count
    })
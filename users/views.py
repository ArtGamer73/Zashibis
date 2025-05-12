from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import User, Group
from .forms import UserForm, EmailPasswordForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
import blog.settings as core
# Create your views here.

@login_required

def account(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:account')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/account.html', {'form': user_form, 'profile_form': profile_form})

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

class ProfileAboutView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/account.html'
    context_object_name = 'account_detail'

    def get_object(self):
        return self.request.user
    
class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/update_account.html'
    success_url = reverse_lazy('users:account')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Your profile has been successfully updated")
        return response
    
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home:home')

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                request.session['username'] = user.username

                subject = user.username
                message = f'Вітаємо, {subject}. You have successfully registered! We are glad to see you'
                from_email = core.settings.EMAIL_HOST_USER
                to_email = user.email
                send_mail(
                    subject,
                    message,
                    from_email, 
                    [to_email],
                    fail_silently=False
                )
                group_name = "Адміністратор" if user.email in core.settings.ADMIN_EMAIL else "User"
                group = Group.objects.filter(name=group_name).first()
                if group:
                    user.groups.add(group)

                return redirect('home')
            except IntegrityError:
                messages.error(request, 'The user with this email address is already registered.')
        else:
            messages.error(request, 'An error occurred. Please check the data you entered.')
    else:
        form = UserForm()
    
    return render(request, 'users/create_user.html', {'form': form, 'create_user': True})
def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created! Log in.')
            return redirect('users:login')  # Направляє на сторінку входу після створення користувача
        else:
            messages.error(request, 'An error occurred. Please check the data you entered.')
    else:
        form = UserCreationForm()
    return render(request, 'users/create_user.html', {'form': form, 'create_user': True})

# filepath: /Users/artemmelnyk/Documents/MyFirstBlog_73/blog/users/views.py
def request_login(request):
    if request.method == 'POST':
        form = EmailPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Аутентифікація користувача
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['username'] = user.username
                return redirect('articles:article_list')  # Використовуйте правильне ім'я маршруту
            else:
                messages.error(request, 'Incorrect login or password!')
                return redirect('users:login')
    else:
        form = EmailPasswordForm()
    return render(request, 'users/request_login.html', {'form': form})
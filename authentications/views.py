from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View
from django.contrib.auth import authenticate
from authentications.form import CreateUserForm


class LoginUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'authentications/login.html')

    def post(self, request):
        email_address = request.POST.get('emailaddress').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=email_address, password=password)

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            message = 'Password or email is incorrect'
            context = {'message': message}
            return render(request, 'authentications/login.html', context)


class RegisterUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'authentications/register.html', context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        context = {'form': form}
        return render(request, 'authentications/register.html', context)


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('home')

from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            # Check username 
            if User.objects.filter(username = username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email = email).exists():
                    messages.error(request, 'That email is already registered')
                    return redirect('register')
                else:
                    #looks good 
                    user = User.objects.create_user(username=username, email = email, first_name = first_name, last_name = last_name, password=password)
                    # auth.login(request,user)
                    # messages.success(request, 'You are now logged in!')
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'You are now registered and can login!')
                    return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('register')
    return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password = password)
        if user:
            auth.login(request,user)
            messages.success(request, 'You are now logged in!')
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials')
        return redirect('login')
    return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id = request.user.id)
    context = {
        'contacts':user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)
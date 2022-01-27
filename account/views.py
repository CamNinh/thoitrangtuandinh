from django.shortcuts import render
from django.http import HttpResponse

from account.forms import RegistrationForm

#authentication function:
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return HttpResponse ('You are authenticated')
    else:
        form = RegistrationForm()
        if request.method == 'post' or request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Your Account has been created')

        context = {
            'form':form
        }
    return  render(request, 'register.html', context)


def Customerlogin(request):
    if request.user.is_authenticated:
        return HttpResponse('You are login')
    else:
        if request.method == 'POST' or request.method == 'post':
            username = request.POST.get('username')
            password = request.POST.get('password')
            customer = authenticate(request, username = username, password = password)
            if customer is not None:
                login(request,customer)
                return HttpResponse("You are logged in successfully")
            else:
                return HttpResponse('404')
    return render(request,'login.html')
# from django.shortcuts import render
# from django.http import HttpResponse
# from account.forms import RegistrationForm
# #authentication function:
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login, logout, authenticate
# # Create your views here.
# def register(request):
#     if request.user.is_authenticated:
#         return HttpResponse ('You are authenticated')
#     else:
#         form = RegistrationForm()
#         if request.method == 'post' or request.method == "POST":
#             form = RegistrationForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponse('Your Account has been created')
#
#         context = {
#             'form':form
#         }
#     return  render(request, 'register.html', context)
#
#
# def Customerlogin(request):
#     if request.user.is_authenticated:
#         return HttpResponse('You are login')
#     else:
#         if request.method == 'POST' or request.method == 'post':
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             customer = authenticate(request, username = username, password = password)
#             if customer is not None:
#                 login(request,customer)
#                 return HttpResponse("You are logged in successfully")
#             else:
#                 return HttpResponse('404')
#     return render(request,'login.html')


from re import split
from order.models import Cart, Order
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator

from .forms import RegistrationForm
from account.models import Profile
from order.views import cart_view

import requests


def register(request):
    if request.method == 'POST' or request.method == 'post':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Profile.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            # user.phone_number = phone_number
            user.save()

            # current_site = get_current_site(request=request)
            # mail_subject = 'Activate your blog account.'
            # message = render_to_string('accounts/active_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user)
            # })
            # send_email = EmailMessage(mail_subject, message, to=[email])
            # send_email.send()
            # messages.success(
            #     request=request,
            #     message="Please confirm your email address to complete the registration"
            # )
            return redirect('register')
        else:
            messages.error(request=request, message="Register failed!")
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, '../templates/register.html', context)


def login(request):
    if request.method == "POST" or request.method == "post":
        email = request.POST.get('email')

        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=cart_view(request))
                cart_items = Order.objects.filter(cart=cart)
                if cart_items.exists():
                    product_variation = []
                    for cart_item in cart_items:
                        variations = cart_item.variations.all()
                        product_variation.append(list(variations))
                        # cart_item.user = user
                        # cart_item.save()
                    cart_items = Order.objects.filter(user=user)
                    existing_variation_list = [list(item.variations.all()) for item in cart_items]
                    id = [item.id for item in cart_items]

                    for product in product_variation:
                        if product in existing_variation_list:
                            index = existing_variation_list.index(product)
                            item_id = id[index]
                            item = Order.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_items = Order.objects.filter(cart=cart)
                            for item in cart_items:
                                item.user = user
                                item.save()
            except Exception:
                pass
            auth.login(request=request, user=user)
            messages.success(request=request, message="Login successful!")

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    next_page = params["next"]
                    return redirect(next_page)
            except Exception:
                return redirect('/store/')
        else:
            messages.error(request=request, message="Login failed!")
    context = {
        'email': email if 'email' in locals() else '',
        'password': password if 'password' in locals() else '',
    }
    return render(request, '../templates/login.html', context=context)


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.success(request=request, message="You are logged out!")
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Profile.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request=request, message="Your account is activated, please login!")
        return render(request, '../templates/login.html')
    else:
        messages.error(request=request, message="Activation link is invalid!")
        return redirect('home')


@login_required(login_url="login")
def dashboard(request):
    return render(request, "accounts/dashboard.html")


def forgotPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = Profile.objects.get(email__exact=email)

            current_site = get_current_site(request=request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()

            messages.success(
                request=request, message="Password reset email has been sent to your email address")
    except Exception:
        messages.error(request=request, message="Account does not exist!")
    finally:
        context = {
            'email': email if 'email' in locals() else '',
        }
        return render(request, "accounts/forgotPassword.html", context=context)


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Profile.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request=request, message='Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request=request, message="This link has been expired!")
        return redirect('home')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Profile.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, message="Password reset successful!")
            return redirect('login')
        else:
            messages.error(request, message="Password do not match!")
    return render(request, 'accounts/reset_password.html')

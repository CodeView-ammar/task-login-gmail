from django.contrib.auth import views as auth_views
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import generic
from django.urls import reverse_lazy

from .forms import LoginForm  # RegisterForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic

from .models import Profile, CustomUser
from .forms import SignUpForm, ProfileUpdateForm, UserUpdateForm

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model

UserModel = get_user_model()
from .tokens import account_activation_token


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('login')

def signup_view(request):
    """
    View function for user signup.
    """
    if request.method == "POST":
        # If the request method is POST, the form data is submitted.
        form = SignUpForm(request.POST)
        if form.is_valid():
            # If the form data is valid, a new user is created.
            user = form.save()

            # The user's profile is also created.
            user.profile.address = form.cleaned_data.get('address')
            user.save()

            # An activation email is sent to the user.
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('account-active.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            msg = EmailMultiAlternatives(mail_subject, mail_subject, to=[to_email])
            html_content = message            
            msg.attach_alternative(html_content, "text/html")

            try:
                # The email is sent.
                msg.send()
                messages.info(request, 'verify Your email!')
            except:
                messages.info(request, 'Your email wrong!')
            return redirect('blog-home')
        else:
            # If the form data is invalid, the errors are displayed to the user.
            messages.error(request, 'Correct the errors below')
    else:
        # If the request method is GET, a blank form is rendered to the user.
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})



def activate(request, uidb64, token):
    """
    Activates a user account.

    Args:
        request: The Django request object.
        uidb64: The base64-encoded user ID.
        token: The activation token.

    Returns:
        The response object.

    """

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # The user exists and the token is valid.
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('blog-home')
    else:
        # The user does not exist or the token is invalid.
        return HttpResponse('Activation link is invalid!')



@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def update(request):
    """
    Updates the user profile.

    Args:
        request: The Django request object.

    Returns:
        The response object.

    """

    if request.method == 'POST':
        # If the request method is POST, the form data is submitted.
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            # If the form data is valid, the user profile is updated.
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        # If the request method is GET, blank forms are loaded.
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}

    return render(request, 'profileUpdate.html', context)


def user_logout(request):
    logout(request)
    return redirect('blog-home')


def home_view(request):
    user = CustomUser.objects.all()
    return render(request, 'home.html', )


class UserDelete(generic.DeleteView):
    model = CustomUser
    template_name = "user_delete.html"
    success_url = reverse_lazy('blog-home')

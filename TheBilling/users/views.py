from django.views import generic
from django.shortcuts import redirect, reverse, render
from django.contrib.auth import logout, login
# from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import UserForm, AuthForm, UserProfileForm, UserAlterationForm
from .models import UserProfile


class SignInView(generic.FormView):
    """
    Basic user sign up page.

    **Template:**

    :template:`users/sign_in.html`
    """
    template_name = "users/sign_in.html"
    form_class = AuthForm
    success_url_name = '/'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url_name())


def sign_out(request):
    """
    Basic user sign out page.
    """
    logout(request)
    return redirect(reverse('users:sign-in'))


@login_required
def AccountView(request):
    """
    User account page. CRUD account details.

    **Template:**

    :template:`users/account.html`
    """
    # user = request.user
    # if not hasattr(user, 'userprofile'):
    #     user.userprofile = UserProfile(user=user)
    # up = request.user.userprofile
    up, _ = UserProfile.objects.get_or_create(user=request.user)
    up_form = UserProfileForm(instance=up)
    context = {'form': up_form}

    if request.method == "POST":
        form = UserProfileForm(instance=up, data=request.POST, files=request.FILES)
        if form.is_valid:
            form.save()
            return redirect('users:account')
    else:
        return render(request, 'users/account.html', context)


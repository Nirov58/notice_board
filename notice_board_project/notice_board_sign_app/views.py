from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from .models import BaseRegisterForm, CodeRegisterForm, OneTimeCode
from .decorators import logout_required


@method_decorator(logout_required, name='dispatch')
class BaseSignUp(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/sign/signup/confirm'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        OneTimeCode.objects.create(code=OneTimeCode.generate_otc(), user=user)
        return super().form_valid(form)


@logout_required()
def check_otc(request):
    if request.method == 'POST':
        form = CodeRegisterForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            user = User.objects.get(email=email)
            code = request.POST['code']
            if OneTimeCode.objects.filter(user=user, code=code).exists():
                user.is_active = True
                user.save()
                OneTimeCode.objects.get(user=user, code=code).delete()
                return redirect('../signin/')
    else:
        form = CodeRegisterForm()

    return render(request, 'sign/sign_up_otc.html', {'form': form})


class RestrictedLoginView(LoginView):

    @method_decorator(logout_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

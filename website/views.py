__author__ = 'rrmerugu'
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return HttpResponse("Hello, world!, website starts here .")


def home_page(request):
    is_loggedin = True
    response = render_to_response('homepage.html', {'title':'RSQUARE LABS | Localised Intelligence', 'is_loggedin': is_loggedin}, context_instance=RequestContext(request))
    response.status_code = 200
    return response


def login(request):
    is_loggedin=  False
    response = render_to_response('login.html', {'title':'Login | Localised Intelligence', 'is_loggedin': is_loggedin}, context_instance=RequestContext(request))
    response.status_code = 200
    return response



from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render_to_response,redirect
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from .forms import RegistrationForm
from core.auth import User


from django.contrib.auth.tokens import default_token_generator

def login_user(request):
    # logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print authenticate(username=username)
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/user/')

    return render_to_response('login.html', context_instance=RequestContext(request))



@login_required(login_url='/auth/login/')
def main(request):
    return render_to_response('main.html', context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/auth/welcome/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, { 'form': form })

    return render_to_response( 'register.html', variables, )


def register_success(request):
    return render_to_response( 'register_success.html', )



def handler404(request):
    response = render_to_response('errors/404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('errors/505.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response
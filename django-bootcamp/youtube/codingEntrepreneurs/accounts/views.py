from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

# Create your views here.
from .forms import LoginForm, RegisterForm

User = get_user_model()

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        try:
            user = User.objects.create_user(username, email, password)
        except:
            user = None
        if user != None:
            login(request, user)
            return redirect("/search")
        else:
            request.session['register_error'] = 1 # 1 == True
    return render(request, 'forms.html', {'form': form})

# user_obj.set_password()

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user != None:
            ## user is valid and active -> is_active
            # request.user == user
            login(request, user)
            return redirect("/")
        else:
            ## For handling attempts
            # attempt = request.session.get('attempt') or 0
            # request.session['attempt'] = attempt + 1
            # return redirect('/invalid-password')
            request.session['invalid_user'] = 1 # 1 == True
    return render(request, 'forms.html', {'form': form})


def logout_view(request):
    logout(request)
    # request.user == Annonymous user
    return redirect('/login')


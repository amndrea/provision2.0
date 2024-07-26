from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

# ------------------------------------------------------ #
# View per effettuare il login con username e password
# ------------------------------------------------------ #
def login_view (request):

    if request.method == "GET":
        return render(request, template_name="login.html")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("login fallito")
            print("username ==> ", username)
            messages.error(request, 'Usrname o password non validi')
            return redirect('login')

# ------------------------------------------------------ #
# View che mostra la home dell'utente loggato 
# ------------------------------------------------------ #
def home (request):
    return render(request, template_name="home.html")


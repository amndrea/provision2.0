from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
import os 
from django.http import FileResponse
from django.conf import settings
from django.http import HttpResponse

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

# ------------------------------------------------------ #
# View per scaricare il template di esempio
# ------------------------------------------------------ #
def download_template(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'TemplateEs.xlsx')
    if os.path.exists(file_path):
        response = FileResponse(open(file_path,'rb'))
        response['Content-Disposition'] = 'attachment; filename="TemplateEs.xlsx"'
        return response
    else:
        return HttpResponse("Il file richiesto non esiste.", status=404)

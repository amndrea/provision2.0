from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import *
from .tools import *



# -------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------FINE FUNZIONI UTILI --------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------------------------#
# View per creare un nuovo utente e mandare a lui il link per la creazione della sua password
# ---------------------------------------------------------------------------------------------#
@login_required
@user_passes_test(lambda u: u.is_staff)
def crea_utente(request):

    if request.method == 'GET':
        return render(request, 'userApp/crea_utente.html')

    if request.method == 'POST':

        # Creo un utente
        nome = request.POST.get('Username')
        email = request.POST.get('Email')
        amministrazione = request.POST.get('Amministrazione')
        acquisti = request.POST.get('Acquisti')
        # Se esiste già un utente con quell'username, rendero sulla pagina di creazione utente con un errore
        if User.objects.filter(username=nome).exists():
            messages.error(request, f'Errore: L\'utente {nome} è gia presente')
            return render(request, template_name='UserApp/crea_utente.html')

        utente_tmp = User(username=nome, email=email)
        utente_tmp.save()

        # creo un hash della pk dell utente per mandare la mail
        token_user = generate_reset_token(utente_tmp.pk)
        hash_user = UserHashPassword(user=utente_tmp, hash_password=token_user)
        hash_user.save()

        # Mando la mail per il reset password
        print("sono qua")
        reset_link = f"http://localhost:8080/user/reset_password/{hash_user.hash_password}/"
        reset_link = str(reset_link)
        corpo = "Link per il reset password di Provision2 \n" + reset_link

        try:
            send_mail(email, 'Link per il reset password Provision2', corpo)
            if acquisti is not None:
                # Aggiungo l'utente al gruppo ACQUISTI
                g = Group.objects.get(name="Acquisti")
                g.user_set.add(utente_tmp)

            # Creo l'oggetto che mostra il menu prima della chat
            if amministrazione is not None:
                # Aggiungo l'utente al gruppo amministrazione
                g = Group.objects.get(name="Amministrazione")
                g.user_set.add(utente_tmp)
            return render(request, template_name='UserApp/riassunto_crea_user.html', context={'user': utente_tmp})
        except SMTPRecipientsRefused as e:
            # Se la mail era errata cancello l'utente appena creato e rendero un messaggio di errore
            utente_tmp.delete()
            print("sono nell'eccezione della mail errata")
            return render(request, template_name='UserApp/crea_utente.html', context={'errore': 'mail_errata'})

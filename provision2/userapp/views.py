from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import *
from .tools import *


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


SERVER_IP = "http://localhost:8000/"
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
        return render(request, 'userapp/crea_utente.html', context={'societa_context': Societa.objects.all().order_by('societa_nome')})

    if request.method == 'POST':

        # Creo un utente
        nome = request.POST.get('Username')
        email = request.POST.get('Email')
        amministrazione = request.POST.get('Amministrazione')
        acquisti = request.POST.get('Acquisti')

        # Se esiste già un utente con quell'username, rendero sulla pagina di creazione utente con un errore
        if User.objects.filter(username=nome).exists():
            messages.error(request, f'Errore: L\'utente {nome} è gia presente')
            return redirect(reverse('userapp:crea_utente'))

        utente_tmp = User(username=nome, email=email)
        utente_tmp.save()

        # creo un hash della pk dell utente per mandare la mail
        token_user = generate_reset_token(utente_tmp.pk)
        hash_user = UserHashPassword(user=utente_tmp, hash_password=token_user)
        hash_user.save()

        # Mando la mail per il reset password
        print("sono qua")
        reset_link = f"{SERVER_IP}user/reset_password/{hash_user.hash_password}/"
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

                societa_ids = request.POST.getlist('Societa')
                for societa_id in societa_ids:
                    societa = Societa.objects.get(pk=societa_id)
                    UserSocieta.objects.create(user=utente_tmp, societa=societa)
            messages.success(request, "Utente creato con successo")
            return redirect(reverse('userapp:crea_utente'))
        except SMTPRecipientsRefused as e:
            # Se la mail era errata cancello l'utente appena creato e rendero un messaggio di errore
            utente_tmp.delete()
            print("sono nell'eccezione della mail errata")
            messages.error(request, "Errore: La mail inserita è errata")
            return redirect(reverse('userapp:crea_utente'))



class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'userapp/lista_utenti.html'
    context_object_name = 'users'
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=False).order_by('username')

        username = self.request.GET.get('username')
        ruolo = self.request.GET.get('ruolo')
        societa = self.request.GET.get('societa')

        if username:
            queryset = queryset.filter(username__icontains=username)

        if ruolo:
            queryset = queryset.filter(groups__name=ruolo)

        if societa:
            queryset = queryset.filter(usersocieta__societa_id=societa)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        for user in context['users']:
            user.ruolo = user.groups.first().name if user.groups.exists() else '-'

        context['societa'] = Societa.objects.all().order_by('societa_nome')
        context['ruolo'] = self.request.GET.get('ruolo', '')
        context['societa_selected'] = self.request.GET.get('societa', '')
        context['username_filter'] = self.request.GET.get('username', '')

        return context

# ------------------------------------------------------------------------ #
# Funzione per eliminare un utente
# ------------------------------------------------------------------------ #
@login_required
@user_passes_test(lambda u: u.is_staff)
def elimina_utente(request, utente_pk):
    user_to_delete = get_object_or_404(User, id=utente_pk)
    if request.method == 'POST':
        if user_to_delete == request.user:
            messages.error(request, "Errore: impossibile eliminare se stessi")
            return redirect(reverse('userapp:user_list'))
        messages.success(request, f"Utente {user_to_delete.username} eliminato con successo")
        user_to_delete.delete()
        return redirect(reverse('userapp:user_list'))



# ------------------------------------------------------------------------ #
# funzione per il reset della password
# ------------------------------------------------------------------------ #
def reset_password(request, reset_token):
    try:
        utente_hash = UserHashPassword.objects.get(hash_password=reset_token)
    except UserHashPassword.DoesNotExist:
        messages.error(request, "Link non valido o scaduto. Richiedi un nuovo link di reset.")
        return redirect('login')  # Reindirizza a una pagina appropriata

    if not utente_hash.is_valid():
        messages.error(request, "Questo link è scaduto. Richiedine uno nuovo all'amministratore.")
        return redirect('login')  # Reindirizza a una pagina appropriata

    user = User.objects.get(pk=utente_hash.user.pk)
    context = {'hash': reset_token, 'utente': user}

    if request.method == 'POST':
        password = request.POST.get('password')
        conferma_password = request.POST.get('conferma_password')

        if password != conferma_password:
            messages.error(request, "Le password non corrispondono.")
        elif len(password) < 8:
            messages.error(request, "La password è troppo corta.")
        elif not contiene_carattere_speciale(password):
            messages.error(request, "La password non contiene nessun carattere speciale.")
        elif not contiene_maiuscola(password):
            messages.error(request, "La password non contiene nessuna lettera maiuscola.")
        else:
            user.set_password(password)
            user.save()
            utente_hash.delete()  # Opzionale: elimina il token dopo l'uso
            messages.success(request, "Password reimpostata con successo. Ora puoi accedere con la nuova password.")
            return redirect('login')

    return render(request, 'userapp/reset_password.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def send_reset_password(request, user_pk):
    user = User.objects.get(pk=user_pk)
    # creo un hash della pk dell utente per mandare la mail
    token_user = generate_reset_token(user_pk)
    hash_user = UserHashPassword(user=user, hash_password=token_user)
    hash_user.save()

    # Mando la mail per il reset password
    reset_link = f"{SERVER_IP}user/reset_password/{hash_user.hash_password}/"
    reset_link = str(reset_link)
    corpo = "Link per il reset password Provision2  \n" + reset_link

    try:
        send_mail(user.email, 'Link per il reset password ElisaGPT', corpo)
        messages.success(request, "Link per il reset password inviato")
    except Exception:
        messages.error(request, "Errore: errore nell'invio del link per il reset password")
    return redirect(reverse('userapp:user_list'))



@login_required
def situazione_utente_societa(request, utente_pk):
    utente = get_object_or_404(User, pk=utente_pk)
    societa_utente = UserSocieta.objects.filter(user=utente).order_by('societa__societa_nome')
    societa_disponibili = Societa.objects.exclude(id__in=societa_utente.values_list('societa', flat=True)).order_by('societa_nome')

    if request.method == 'POST':
        societa_id = request.POST.get('societa')
        if societa_id:
            societa = get_object_or_404(Societa, pk=societa_id)
            UserSocieta.objects.create(user=utente, societa=societa)
            messages.success(request, f"Società {societa.societa_nome} aggiunta all'utente {utente.username}")
            return redirect('userapp:situazione_utente_societa', utente_pk=utente.pk)

    context = {
        'utente': utente,
        'societa_utente': societa_utente,
        'societa_disponibili': societa_disponibili,
    }
    return render(request, 'userapp/situazione_utente_societa.html', context)

@login_required
def delete_societa_utente(request, societa_pk, utente_pk):
    user_societa = get_object_or_404(UserSocieta, user_id=utente_pk, societa_id=societa_pk)
    societa_nome = user_societa.societa.societa_nome
    user_societa.delete()
    messages.success(request, f"Società {societa_nome} rimossa dall'utente {user_societa.user.username}")
    return redirect('userapp:situazione_utente_societa', utente_pk=utente_pk)
# Django imports
from django.core import mail
from django.shortcuts import render
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse


# Local imports
from eventex.subscriptions.forms import SubscriptionForm

def subscribe(request):
    # sourcery skip: remove-unnecessary-else, swap-if-else-branches
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            body = render_to_string('subscriptions/subscription_email.txt', form.cleaned_data)
            
            mail.send_mail("Confirmação de inscrição", body,
                        "contanto@eventex.com.br", ['contato@eventex.com.br', form.cleaned_data['email']])

            messages.success(request, 'Inscrição realizada com sucesso!')
            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscriptions/subscription_form.html', {'form': form})
        
    context = {'form': SubscriptionForm()} 
    return render(request, 'subscriptions/subscription_form.html', context)



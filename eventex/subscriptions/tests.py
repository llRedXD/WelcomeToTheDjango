#  Django imports
import email
from django.core import mail
from django.test import TestCase

# Local imports
from eventex.subscriptions.forms import SubscriptionForm


class subscribeTest(TestCase):

    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """GET /inscricao/ deve retorna code status 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Deve usar subscriptions/subscription_form.html"""
        self.assertTemplateUsed(
            self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html deve conter as input tags"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """Html deve conter csrf"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have the subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)
        
    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))
        
        
class SubscripePostTest(TestCase):
    def setUp(self):
        data = dict(name='Gabriel Neira', cpf='12345678901',email="gh.o.neira@hotmail.com", phone='11-99999999')
        self.resp = self.client.post('/inscricao/', data)
    
    def test_post(self):
        """Valida o  POST e redireciona para  /inscricao/"""
        self.assertEqual(302, self.resp.status_code)
        
        
    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))
        
        
    def test_subscription_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'
        
        self.assertEqual(expect, email.subject)
        
        
    def test_subscription_email_from(self):
        email = mail.outbox[0]
        expect = 'contanto@eventex.com.br'
        
        self.assertEqual(expect, email.from_email)
        
        
    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'gh.o.neira@hotmail.com']
        
        self.assertEqual(expect, email.to)
        
        
    def test_subscription_email_body(self):
        email = mail.outbox[0]
        
        self.assertIn('Gabriel Neira', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('gh.o.neira@hotmail.com', email.body)
        self.assertIn('11-99999999', email.body)
        
        
class SubscripeInvalidPostTest(TestCase):
    def setUp(self):
        data = dict(name='Gabriel Neira', cpf='12345678901',
                     email="gh.o.neira@hotmail.com", phone='11-99999999')
        self.resp = self.client.post('/inscricao/', {})
        
        
    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)
        
        
    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')
        
        
    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)
        
        
    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)
    
    
    
class SubscribeSuccessMessage(TestCase):
    def setUp(self):
        data = dict(name='Gabriel Neira', cpf='12345678901',
                    email="gh.o.neira@hotmail.com", phone='11-99999999')
        self.resp = self.client.post('/inscricao/', data, follow=True)
        
    
    def test_message(self):
        self.assertContains(self.resp, 'Inscrição realizada com sucesso!')

from django.test import TestCase

class ContactTestCase(TestCase):
    
    def setUp(self):
        self.response = self.client.get('/')
    
    def test_get(self):
        """GET / must return status code 200"""
        self.assertEqual(200, self.response.status_code)
    
    def test_template(self):
        """Must use index.html"""
        self.assertTemplateUsed(self.response, 'index.html')
        
        
    def test_subscription_link(self):
        """Context must have subscription link"""
        expected = 'href="/inscricao/"'
        self.assertContains(self.response, expected)
from django.contrib import admin
from django.urls import path
import eventex.core.views
from eventex.subscriptions.views import subscribe

urlpatterns = [
    path("inscricao/", subscribe),
    path('', eventex.core.views.home, name='home'),
    path('admin/', admin.site.urls),
]

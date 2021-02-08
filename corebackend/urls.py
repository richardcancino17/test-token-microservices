"""ipet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from corebackend.settings import base
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^api/v1.0/user/',
                      include('apps.account.api.urls', namespace='account')),
                  # url(r'^api/discount/',
                  #     include('account.discounts.urls', namespace='discount',)),
                  # url(r'^api/albums/',
                  #     include('account.albums.urls', namespace='albums',)),
                  # Docs URL
                  url(r'^docs/', include('rest_framework_docs.urls')),
              ] + static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)

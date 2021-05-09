"""mystorys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#зависимости
#django-debug-toolbar 3.2

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('index/', include('index.urls')),
    path('usermanager/', include('usermanager.urls')),
    path('newpost/', include('newpost.urls')),
    path('post/', include('post.urls')),
    path('user/', include('user.urls')),
    path('smalltasks/', include('smalltasks.urls')),
    path('search/', include('search.urls')),
    path('subs/', include('subs.urls')),
    path('aboutus/', include('aboutus.urls')),
    path('messages/', include('messages.urls')),
    path('postmanager/', include('postmanager.urls')),
    path('commentmanager/', include('commentmanager.urls')),
    path('sitemap/', include('sitemap.urls')),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(r'/favicon.ico', document_root='static/favicon.ico')


#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

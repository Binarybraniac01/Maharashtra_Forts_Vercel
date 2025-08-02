"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from home.utils import *

from home.views import *
from user.views import *
from recommendations.views import *
from knowaboutforts.views import *
from feedback.views import *

# for media url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home_view, name='home_view'),
    path('search/', search_api, name='search_api'),
    path('send-coordinates/', send_coordinates), # remember to delete user specific coordinates and optimize code for that
    path('generateplan/', generateplan, name='generateplan'),

    path('ourplans/', ourplans, name='ourplans'),
    path('recommdirection/', recommdirection, name='recommdirection'),
    path('recommdirection/send-coordinates/', send_coordinates, name='send_coordinates'),
    path('recommgenerateplan/', recom_generateplan, name='recom_generateplan'),

    path('knowaboutforts/', knowaboutforts, name='knowaboutforts'),
    path('getdistforts/<dist>/', getdistforts, name='getdistforts'),
    path('searchfortname/', searchfortname, name='searchfortname'),
    path('viewmore/<fortname>/', viewmore, name='viewmore'),

    path('feedback/', feedback, name='feedback'),

    path('register-page/', register_page),
    path('login-page/', login_page),
    path('guest-acc/', guest_acc),
    path('logout/', logout_view),
    path('admin/', admin.site.urls),

    path('keep-db-alive/', keep_db_alive, name='keep_db_alive')
]



# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += staticfiles_urlpatterns()


# Serve media files in development and prod

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# else:
#     from django.views.static import serve
#     from django.urls import re_path

#     urlpatterns += [
#         re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
#     ]
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.conf.urls import  include, url
from django.contrib import admin

urlpatterns =
    [

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^hello/', include('fb_chatbot.urls')),
    url(r'', include('fb_chatbot.urls')),
]

from django.conf.urls import url
from fb_chatbot import views
from .views import MyQuoteBotView


urlpatterns = []
	url(r'^$', views.index,name = 'index'),
	url(r'^facebook_auth/?$', MyQuoteBotView.as_view()),]
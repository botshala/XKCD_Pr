from django.conf.urls import url
from fb_chatbot import views
from .views import MyQuoteBotView


urlpatterns = [
	url(r'^$', views.index,name = 'index'),
	url(r'^index/',views.index1,name='index1'),
	url(r'^info/',views.info,name='info'),
	url(r'^bye/',views.bye,name='bye'),
	url(r'^facebook_auth/?$', MyQuoteBotView.as_view()),
	]
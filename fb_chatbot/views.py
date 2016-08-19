import json, requests, random, re
from pprint import pprint
import os
from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


PAGE_ACCESS_TOKEN = 'EAAPcJptvRT0BABtxXhx7tKL6mfhCZAskXcfxqU9C4vrbJ3YZAf0urignhG7IHjnRqqGLIg1VZCjUXX5UTeQc3HqlNK6PTxpnMkNeYRZBmR8k5DYA1YxeVpiGpFizdewCIpE1ardG9gXYEwmM1zCZBqfEdRDZCep30VtXmf6sEwcQZDZD'
VERIFY_TOKEN = '9871501397'


def xkcd_search(text):
    f=open(os.path.join(os.path.dirname(__file__)),"xkcd.txt")
    obj=json.loads(f.read())
    f.close()
    if text in obj:
        return obj[text]
    else:
        no=len(obj)/2
        return obj[str(random.randint(1,no))]

def post_facebook_message(fbid, message):
    type='text'
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
   
    try:
        if 'attachments' in message:
            type='attachments'
    except:
        pass

    reply_text='Yo'
    response_msg=''
    greeting=''
    try:
        user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
        user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
        user_details = requests.get(user_details_url, user_details_params).json() 
        reply_text=reply_text + user_details['first_name'] + user_details['last_name']
        
    except:
        reply_text=reply_text + 'Man'

    reply_text=reply_text + ' :) '
    
    if fbid in id_list:
        pass
    else:
        id_list.append(fbid)
        reply_text=reply_text + "\n This is a chatbot.You will get an XKCD comic strip based on your request"

    rep=json.dumps({"recipient":{"id":fbid},"message":{"text":reply_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=rep)

    img_url='https://upload.wikimedia.org/wikipedia/en/e/e0/Iron_Man_bleeding_edge.jpg'
    if type=='attachments':
        try:
            img_url=str(message["attachments"][0]["payload"]['url'])
        except:
            pass
        img_msg ={"attachment":{"type":"image","payload":{"url" : img_url}}}
        response_msg=json.dumps({"recipient":{"id":fbid},"message":img_msg})
        
        
    else:
        recevied_message=message['text']
        url=xkcd_search(recevied_message)
        img_msg={"attachment":{"type":"image","payload":{"url":url}}}
        response_msg=json.dumps({"recipient":{"id":fbid},"message":img_msg})
                   
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


class MyQuoteBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    post_facebook_message(message['sender']['id'], message['message'])   

        return HttpResponse()    



def return_random_quote():
    random.shuffle(quotes_arr)
    return quotes_arr[0]

def index(request):
    #print test()
    li=return_random_quote()
    stri=''
    for i in li:
            stri=stri + '\n' +str(i)
    return HttpResponse("Hello World"+' \n'+str(quote_search('Albert')))

def index1(request):
    return HttpResponse("<html><head><style>p{color:green;background-color:cyan;padding:20px;margin:30px;position:absolute;border-radius:10px;}</style><title>HELLO!</title></head><body>Hello World<p><b>Hey World</b></p></body></html>")

def  bye(request):
    return HttpResponse("<html><head><style> p {color:green;border-radius:5px;background-color:maroon;position:absolute;padding:20px;}</style><title>GOODBYE</title></head><body><p>Bye Bye World</p><body></html>")

def info(request):
    return HttpResponse("I AM A CHATBOT")
def test():
    post_facebook_message('PradyumnSinh.1','test message')




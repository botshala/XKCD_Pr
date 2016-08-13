import json, requests, random, re
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

PAGE_ACCESS_TOKEN = 'EAAPcJptvRT0BABtxXhx7tKL6mfhCZAskXcfxqU9C4vrbJ3YZAf0urignhG7IHjnRqqGLIg1VZCjUXX5UTeQc3HqlNK6PTxpnMkNeYRZBmR8k5DYA1YxeVpiGpFizdewCIpE1ardG9gXYEwmM1zCZBqfEdRDZCep30VtXmf6sEwcQZDZD'
VERIFY_TOKEN = '9871501397'

emoji_arr = [["😄", "Smiling Face with Open Mouth and Smiling Eyes"], ["😃", "Smiling Face with Open Mouth"], ["😀", "Grinning Face"], ["😊", "Smiling Face with Smiling Eyes"], ["☺️", "White Smiling Face"], ["😉", "Winking Face"], ["😍", "Smiling Face with Heart-Shaped Eyes"], ["😘", "Face Throwing a Kiss"], ["😚", "Kissing Face with Closed Eyes"], ["😗", "Kissing Face"], ["😙", "Kissing Face with Smiling Eyes"], ["😜", "Face with Stuck-Out Tongue and Winking Eye"], ["😝", "Face with Stuck-Out Tongue and Tightly-Closed Eyes"], ["😛", "Face with Stuck-Out Tongue"], ["😳", "Flushed Face"], ["😁", "Grinning Face with Smiling Eyes"], ["😔", "Pensive Face"], ["😌", "Relieved Face"], ["😒", "Unamused Face"], ["😞", "Disappointed Face"], ["😣", "Persevering Face"], ["😢", "Crying Face"], ["😂", "Face with Tears of Joy"], ["😭", "Loudly Crying Face"], ["😪", "Sleepy Face"], ["😥", "Disappointed but Relieved Face"], ["😰", "Face with Open Mouth and Cold Sweat"], ["😅", "Smiling Face with Open Mouth and Cold Sweat"], ["😓", "Face with Cold Sweat"], ["😩", "Weary Face"], ["😫", "Tired Face"], ["😨", "Fearful Face"], ["😱", "Face Screaming in Fear"], ["😠", "Angry Face"], ["😡", "Pouting Face"], ["😤", "Face with Look of Triumph"], ["😖", "Confounded Face"], ["😆", "Smiling Face with Open Mouth and Tightly-Closed Eyes"], ["😋", "Face Savouring Delicious Food"], ["😷", "Face with Medical Mask"], ["😎", "Smiling Face with Sunglasses"], ["😴", "Sleeping Face"], ["😵", "Dizzy Face"], ["😲", "Astonished Face"], ["🏠", "House Building"], ["🏡", "House with Garden"], ["🏫", "School"], ["🏢", "Office Building"], ["🏣", "Japanese Post Office"], ["🏥", "Hospital"], ["🏦", "Bank"], ["🏪", "Convenience Store"], ["🏩", "Love Hotel"], ["🏨", "Hotel"], ["💒", "Wedding"], ["⛪️", "Church"], ["🏬", "Department Store"], ["🏤", "European Post Office"], ["🌇", "Sunset over Buildings"], ["🌆", "Cityscape at Dusk"], ["🏯", "Japanese Castle"], ["🏰", "European Castle"], ["⛺️", "Tent"], ["🏭", "Factory"], ["🗼", "Tokyo Tower"], ["🗾", "Silhouette of Japan"], ["🗻", "Mount Fuji"], ["🌄", "Sunrise over Mountains"], ["🌅", "Sunrise"], ["🌃", "Night with Stars"], ["🗽", "Statue of Liberty"], ["🌉", "Bridge at Night"], ["🎠", "Carousel Horse"], ["🎡", "Ferris Wheel"], ["⛲️", "Fountain"], ["🎢", "Roller Coaster"], ["🚢", "Ship"], ["⛵️", "Sailboat"], ["🚤", "Speedboat"], ["🚣", "Rowboat"], ["⚓️", "Anchor"], ["🚀", "Rocket"], ["✈️", "Airplane"], ["💺", "Seat"], ["🚁", "Helicopter"], ["🚂", "Steam Locomotive"], ["🚊", "Tram"], ["🚉", "Station"], ["🐶", "Dog Face"], ["🐺", "Wolf Face"], ["🐱", "Cat Face"], ["🐭", "Mouse Face"], ["🐹", "Hamster Face"], ["🐰", "Rabbit Face"], ["🐸", "Frog Face"], ["🐯", "Tiger Face"], ["🐨", "Koala"], ["🐻", "Bear Face"], ["🐷", "Pig Face"], ["🐽", "Pig Nose"], ["🐮", "Cow Face"], ["🐗", "Boar"], ["🐵", "Monkey Face"], ["🐒", "Monkey"], ["🐴", "Horse Face"], ["🐑", "Sheep"], ["🐘", "Elephant"], ["🐼", "Panda Face"], ["🐧", "Penguin"], ["🐦", "Bird"], ["🐤", "Baby Chick"], ["🐥", "Front-Facing Baby Chick"], ["🐣", "Hatching Chick"], ["🐔", "Chicken"], ["🐍", "Snake"], ["🐢", "Turtle"], ["🐛", "Bug"], ["🐝", "Honeybee"], ["🐜", "Ant"], ["🐞", "Lady Beetle"], ["🐌", "Snail"], ["🐙", "Octopus"], ["🐚", "Spiral Shell"], ["🐠", "Tropical Fish"], ["🐟", "Fish"], ["🐬", "Dolphin"], ["🐳", "Spouting Whale"], ["🐋", "Whale"], ["🐄", "Cow"], ["🐏", "Ram"], ["🐀", "Rat"], ["🐃", "Water Buffalo"], ["🎍", "Pine Decoration"], ["💝", "Heart with Ribbon"], ["🎎", "Japanese Dolls"], ["🎒", "School Satchel"], ["🎓", "Graduation Cap"], ["🎏", "Carp Streamer"], ["🎆", "Fireworks"], ["🎇", "Firework Sparkler"], ["🎐", "Wind Chime"], ["🎑", "Moon Viewing Ceremony"], ["🎃", "Jack-o-lantern"], ["👻", "Ghost"], ["🎅", "Father Christmas"], ["🎄", "Christmas Tree"], ["🎁", "Wrapped Present"], ["🎋", "Tanabata Tree"], ["🎉", "Party Popper"], ["🎊", "Confetti Ball"], ["🎈", "Balloon"], ["🎌", "Crossed Flags"], ["🔮", "Crystal Ball"], ["🎥", "Movie Camera"], ["📷", "Camera"], ["📹", "Video Camera"], ["📼", "Videocassette"], ["💿", "Optical Disc"], ["📀", "DVD"], ["💽", "Minidisc"], ["💾", "Floppy Disk"], ["💻", "Personal Computer"], ["📱", "Mobile Phone"], ["☎️", "Black Telephone"], ["📞", "Telephone Receiver"], ["📟", "Pager"], ["📠", "Fax Machine"], ["📡", "Satellite Antenna"], ["📺", "Television"], ["📻", "Radio"], ["🔊", "Speaker with Three Sound Waves"], ["🔉", "Speaker with One Sound Wave"], ["🔈", "Speaker"], ["🔇", "Speaker with Cancellation Stroke"], ["🔔", "Bell"], ["🔕", "Bell with Cancellation Stroke"], ["1⃣", "Keycap 1"], ["2⃣", "Keycap 2"], ["3⃣", "Keycap 3"], ["4⃣", "Keycap 4"], ["5⃣", "Keycap 5"], ["6⃣", "Keycap 6"], ["7⃣", "Keycap 7"], ["8⃣", "Keycap 8"], ["9⃣", "Keycap 9"], ["0⃣", "Keycap 0"], ["🔟", "Keycap Ten"], ["🔢", "Input Symbol for Numbers"], ["#⃣", "Hash Key"], ["🔣", "Input Symbol for Symbols"], ["⬆️", "Upwards Black Arrow"], ["⬇️", "Downwards Black Arrow"], ["⬅️", "Leftwards Black Arrow"], ["➡️", "Black Rightwards Arrow"], ["🔠", "Input Symbol for Latin Capital Letters"], ["🔡", "Input Symbol for Latin Small Letters"], ["🔤", "Input Symbol for Latin Letters"], ["↗️", "North East Arrow"], ["↖️", "North West Arrow"], ["↘️", "South East Arrow"], ["↙️", "South West Arrow"], ["↔️", "Left Right Arrow"], ["↕️", "Up Down Arrow"], ["🔄", "Anticlockwise Downwards and Upwards Open Circle Arrows"], ["◀️", "Black Left-Pointing Triangle"], ["▶️", "Black Right-Pointing Triangle"], ["🔼", "Up-Pointing Small Red Triangle"], ["🔽", "Down-Pointing Small Red Triangle"], ["↩️", "Leftwards Arrow with Hook"], ["↪️", "Rightwards Arrow with Hook"], ["ℹ️", "Information Source"], ["⏪", "Black Left-Pointing Double Triangle"], ["⏩", "Black Right-Pointing Double Triangle"], ["⏫", "Black Up-Pointing Double Triangle"], ["⏬", "Black Down-Pointing Double Triangle"], ["⤵️", "Arrow Pointing Rightwards Then Curving Downwards "], ["⤴️", "Arrow Pointing Rightwards Then Curving Upwards"], ["🆗", "Squared OK"], ["🔀", "Twisted Rightwards Arrows"], ["🔁", "Clockwise Rightwards and Leftwards Open Circle Arrows"], ["🌡", "Thermometer"], ["🌢", "Black Droplet"], ["🌣", "White Sun"], ["🌤", "White Sun with Small Cloud"], ["🌥", "White Sun Behind Cloud"], ["🌦", "White Sun Behind Cloud with Rain"], ["🌧", "Cloud with Rain"], ["🌨", "Cloud with Snow"], ["🌩", "Cloud with Lightning"], ["🌪", "Cloud with Tornado"], ["🌫", "Fog"], ["🌬", "Wind Blowing Face"], ["🌶", "Hot Pepper"], ["🍽", "Fork and Knife with Plate"], ["🎔", "Heart with Tip on The Left"], ["🎕", "Bouquet of Flowers"], ["🎖", "Military Medal"], ["🎗", "Reminder Ribbon"], ["🎘", "Musical Keyboard with Jacks"], ["🎙", "Studio Microphone"], ["🎚", "Level Slider"], ["🎛", "Control Knobs"], ["🎜", "Beamed Ascending Musical Notes"], ["🎝", "Beamed Descending Musical Notes"], ["🎞", "Film Frames"], ["🎟", "Admission Tickets"], ["🏅", "Sports Medal"], ["🏋", "Weight Lifter"], ["🏌", "Golfer"], ["🏍", "Racing Motorcycle"], ["🏎", "Racing Car"], ["🏔", "Snow Capped Mountain"], ["🏕", "Camping"], ["🏖", "Beach with Umbrella"], ["🏗", "Building Construction"], ["🏘", "House Buildings"], ["🏙", "Cityscape"], ["🏚", "Derelict House Building"], ["🏛", "Classical Building"], ["🏜", "Desert"], ["🏝", "Desert Island"], ["🏞", "National Park"], ["🏟", "Stadium"], ["🏱", "White Pennant"], ["☝🏻", "White White Up Pointing Index"], ["☝🏼", "Light Brown White Up Pointing Index"], ["☝🏽", "Olive Toned White Up Pointing Index"], ["☝🏾", "Deeper Brown White Up Pointing Index"], ["☝🏿", "Black White Up Pointing Index"], ["✊🏻", "White Raised Fist"], ["✊🏼", "Light Brown Raised Fist"], ["✊🏽", "Olive Toned Raised Fist"], ["✊🏾", "Deeper Brown Raised Fist"], ["✊🏿", "Black Raised Fist"], ["✋🏻", "White Raised Hand"], ["✋🏼", "Light Brown Raised Hand"], ["✋🏽", "Olive Toned Raised Hand"], ["✋🏾", "Deeper Brown Raised Hand"], ["✋🏿", "Black Raised Hand"], ["✌🏻", "White Victory Hand"], ["✌🏼", "Light Brown Victory Hand"], ["✌🏽", "Olive Toned Victory Hand"], ["✌🏾", "Deeper Brown Victory Hand"], ["✌🏿", "Black Victory Hand"], ["🎅🏻", "White Father Christmas"], ["🎅🏼", "Light Brown Father Christmas"], ["🎅🏽", "Olive Toned Father Christmas"], ["🎅🏾", "Deeper Brown Father Christmas"], ["🎅🏿", "Black Father Christmas"], ["🏃🏻", "White Runner"], ["🏃🏼", "Light Brown Runner"], ["🏃🏽", "Olive Toned Runner"], ["🏃🏾", "Deeper Brown Runner"], ["🏃🏿", "Black Runner"], ["🏄🏻", "White Surfer"], ["🏄🏼", "Light Brown Surfer"], ["🏄🏽", "Olive Toned Surfer"], ["🏄🏾", "Deeper Brown Surfer"], ["🏄🏿", "Black Surfer"], ["🏇🏻", "White Horse Racing"], ["🏇🏼", "Light Brown Horse Racing"], ["🏇🏽", "Olive Toned Horse Racing"], ["🏇🏾", "Deeper Brown Horse Racing"], ["🏇🏿", "Black Horse Racing"], ["🏊🏻", "White Swimmer"], ["🏊🏼", "Light Brown Swimmer"], ["🏊🏽", "Olive Toned Swimmer"], ["🏊🏾", "Deeper Brown Swimmer"]]


id_list=[]


quotes_arr = [["Life isn’t about getting and having, it’s about giving and being.", "Kevin Kruse"],
["Whatever the mind of man can conceive and believe, it can achieve.", "Napoleon Hill"],
["Work Hard","Albert Einstein"],
["Strive not to be a success, but rather to be of value.", "Albert Einstein"],
["Two roads diverged in a wood, and I—I took the one less traveled by, And that has made all the difference.", "Robert Frost"],
["I attribute my success to this: I never gave or took any excuse.", "Florence Nightingale"],
["You miss 100% of the shots you don’t take.", "Wayne Gretzky"],
["I’ve missed more than 9000 shots in my career. I’ve lost almost 300 games. 26 times I’ve been trusted to take the game winning shot and missed. I’ve failed over and over and over again in my life. And that is why I succeed.", "Michael Jordan"],
["The most difficult thing is the decision to act, the rest is merely tenacity.", "Amelia Earhart"],
["Every strike brings me closer to the next home run.", "Babe Ruth"],
["Definiteness of purpose is the starting point of all achievement.", "W. Clement Stone"],
["We must balance conspicuous consumption with conscious capitalism.", "Kevin Kruse"],
["Life is what happens to you while you’re busy making other plans.", "John Lennon"],
["We become what we think about.", "Earl Nightingale"],
["Twenty years from now you will be more disappointed by the things that you didn’t do than by the ones you did do, so throw off the bowlines, sail away from safe harbor, catch the trade winds in your sails.  Explore, Dream, Discover.", "Mark Twain"],
["Life is 10% what happens to me and 90% of how I react to it.", "Charles Swindoll"],
["The most common way people give up their power is by thinking they don’t have any.", "Alice Walker"],
["The mind is everything. What you think you become.", "Buddha"],
["The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"],
["An unexamined life is not worth living.", "Socrates"],
["Eighty percent of success is showing up.", "Woody Allen"],
["Your time is limited, so don’t waste it living someone else’s life.", "Steve Jobs"],
["Winning isn’t everything, but wanting to win is.", "Vince Lombardi"],
["I am not a product of my circumstances. I am a product of my decisions.", "Stephen Covey"],
["Every child is an artist.  The problem is how to remain an artist once he grows up.", "Pablo Picasso"]]

img_url='https://upload.wikimedia.org/wikipedia/en/e/e0/Iron_Man_bleeding_edge.jpg'

def quote_search(string):
    string=string.lower()
    random.shuffle(quotes_arr)
    for text,author in quotes_arr:
        if string in author.lower():
            return text
    return str(quotes_arr[0][0])

def emoji_search(search_string):
    if not search_string:
        return 'Emoji not found :('

    if search_string in '*,random,anything'.split(','):
        random.shuffle(emoji_arr)
        return emoji_arr[0][0] + ' : '+emoji_arr[0][1]

    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',search_string).lower().split()
    print (tokens)

    result_arr = []

    for token in tokens:
        for emoji,emoji_text in emoji_arr:
            if token in emoji_text.lower():
                result_arr.append(emoji)
            
    
    if not result_arr:
        return 'Emoji not found :('
    else:
        random.shuffle(result_arr)
        return " ".join(result_arr[:5])

def post_facebook_message(fbid, message):


   
        
    type='text'
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
   
    try:
        if 'attachments' in message:
            type='attachments'
    except:
        pass
    
    #
    #reply_text = recevied_message + '  :)'
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
        id_list=id_list+[fbid]
        reply_text=reply_text + "Hey man! This is a chatbot.Tell us how you are feeling and we will respond the appropriate emoji.Also,you can enter the name of famous thinker and get a quoatation"
    rep=json.dumps({"recipient":{"id":fbid},"message":{"text":reply_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=rep)

    if type=='attachments':
        try:
            #print("                    ATTACHMENTS            \n"+"-------------------\n"+str(message["attachments"])+'\n\n')

            #print('\n\n\n\n\n\n\n\n\n\n'+' URL DERIVED FROM ATTAHCMENTS '+'\n')
            #print('\n'+str(message["attachments"][0]["payload"]['url'])+'\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

            img_url=str(message["attachments"][0]["payload"]['url'])
           # print("DERIVED IMG URL  \n" + img_url)
        except:
            pass
        img_msg ={"attachment":{"type":"image","payload":{"url" : img_url}}}
        try: 
            response_msg=json.dumps({"recipient":{"id":fbid},"message":img_msg})
            res=json.dumps({"recipient":{"id":fbid},"message":{"text":"Woh Thats an Attachment"}})
            #print("\n\n\n\n\n\n\n\n\n\n\n COMPLETED")
            status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=res)
        except:
            response_msg=json.dumps({"recipient":{"id":fbid},"message":{"text":"IMAGE SENDING FAILED"}})
        
    else:
        recevied_message=message['text']
        split_list=recevied_message.split('*')
        query=''
        if(split_list[0]==''):
            query=query+split_list[1]
        else:
            query=query+split_list[0]
        li=quote_search(query)
        joke_text = '\n' + li
        joke_text=joke_text + emoji_search(recevied_message)
        response_msg=json.dumps({"recipient":{"id":fbid},"message":{"text":joke_text}})
        print(response_msg)
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
   
   # response_msg2 =json.dumps({"recipient":{"id":fbid},"message":img_msg})
    #response_msg = json.dumps({"recipient":{"id":fbid}, "message":msg})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    #status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg2)
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

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        #Try to check request
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        #print('\n\n\n\n\n\n\n\n\n\n\n\n\\'+str(incoming_message)+'\n\n\n\n\n\n\n\n\n\n\n\n')
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    #print(str(message["message"]))    
                   # msg=message["message"]

                    #status = requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN, headers={"Content-Type": "application/json"},data=json.dumps({"recipient":{"id":message['sender']['id']}, "message":{"text":str(message)}}))
                    #return HttpResponse(str(message))
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly. 
                    post_facebook_message(message['sender']['id'], message['message'])    
                   ##########IMP IMP #if text in message[0]['message'] and if attachments in

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




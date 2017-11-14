import random

import microgear.client as microgear
import logging
import time
import json

from pyfirebase import Firebase
import time
import json
import re
firebase = Firebase('https://iotapplication-7cf10.firebaseio.com/')

ref = firebase.ref('CustomerInfo')

itemlist = []

itemlist_key = []

appid = 'SmartFridge'
gearkey = 'YpZmMdcaemYKQLb'
gearsecret =  'I10EsM0ZTaI4PbDVHAWm3j96G'

microgear.create(gearkey,gearsecret,appid,{'debugmode': True})
itemRef = ref.child('-KqsdeuVyyatxKELuMs4').child('Item').get()
def RetreiveData():
    # Get the contents from the reference

    #itemRef = ref.child('-KqsdeuVyyatxKELuMs4').child('Item').get()
    """"""
    # add only values inside itemlist
    a = []
    b= []
    #[a.append(p.values()) for p in itemRef.values()]

    for i in itemRef.values():
        #arrayString = i.split(",")
        #print json.dumps(i)
        #a.append(json.dumps(i))
        a.append(i)

    print a
    # add only keys inside itemlist_key
    [b.append(p) for p in itemRef.keys()]

    """
   for i in itemlist_key:
        print i
      
    for i in itemlist:
        print i.name
        print i.price
    """
    return  a,b

def connection():
    logging.info("Now I am connected with netpie")

def subscription(topic,message):
    logging.info(topic+" "+message)

def disconnect():
    logging.debug("disconnect is work")

if __name__ == "__main__":
    microgear.setalias("MyRaspberryPI")
    microgear.on_connect = connection
    microgear.on_message = subscription
    microgear.on_disconnect = disconnect
    microgear.subscribe("/mails")
    microgear.connect(False)

    if (microgear.connected):

        itemlist, itemlist_key = RetreiveData()


        #print type(itemlist)
        #microgear.chat("outdoor/temp", '{"name":"Pocky"}')
        #microgear.chat("outdoor/temp", json.dumps(itemlist))
        microgear.chat("outdoor/temp", json.dumps(itemlist))
        print ("sud song leaw na")
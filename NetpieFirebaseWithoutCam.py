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
gearsecret = 'I10EsM0ZTaI4PbDVHAWm3j96G'

microgear.create(gearkey, gearsecret, appid, {'debugmode': True})
itemRef = ref.child('-KqsdeuVyyatxKELuMs4').child('Item').get()


def RetreiveData():
    # Get the contents from the reference

    # itemRef = ref.child('-KqsdeuVyyatxKELuMs4').child('Item').get()
    """"""
    # add only values inside itemlist
    a = []
    b = []
    # [a.append(p.values()) for p in itemRef.values()]

    for i in itemRef.values():
        # arrayString = i.split(",")
        # print json.dumps(i)
        # a.append(json.dumps(i))
        a.append(i)
        """
        if i =={'price': 30, 'name': 'Pepsi'}:
            print 'same'
    a.append({'price': 170, 'name': 'Pocky'})"""

    # add only keys inside itemlist_key
    [b.append(p) for p in itemRef.keys()]

    """
   for i in itemlist_key:
        print i

    for i in itemlist:
        print i.name
        print i.price
    """
    return a, b


def ActivateCamera():
    #getFromScan = 'Kitkat:P4:8/11/2018:3'
    getFromScan = 'Coke:P4:8/11/2018:3'
    splitString = getFromScan.split(":")
    checkProductName = splitString[0]
    checkExpirydate = splitString[2]
    itemCode = splitString[3]
    # data = {"name": getFromScan}
    data = {'price': 30, 'Code': splitString[3], 'name': splitString[0], 'expiryDate': splitString[2]}
    checkDuplicate = False
    counter = 0
    """"""
    # 1.1
    for i in itemlist:

        # 2.1 same product name
        if i['name'] == checkProductName:
            print "have same product name"
            checkDuplicate = True
            # 3.1 same expiryDate
            if i['expiryDate'] == checkExpirydate:
                print "have same expiryDate"
                """
                print i['Code'] + ' is the old item code'
                i['Code'] += ',' + itemCode
                print i['Code'] + ' is the new item code' """

                # 4.1 itemCode(itemID) is duplicate
                if i['Code'] == itemCode:

                    # 5.1 array of Code is equal 1
                    if len(i['Code']) == 1:
                        # remove statement
                        print 'remove'
                    # 5.2 array of Code is greater than 1
                    else:
                        # delete item code from dict and update
                        # update statement
                        print 'update'

                # 4.2 itemCode(itemID) is not duplicate
                else:
                    # update statement with append new itemCode into existing dict
                    print 'update'

            # 3.2 expiry date is not duplicate
            else:
                # add statement
                print 'adsf'
        counter += 1

    # 1.2 if checkDuplicate == false it will add the new one
    if checkDuplicate == False:
        # add statement
        print 'add new item'
        foraddNewitemRef = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')

        NewItemKey = foraddNewitemRef.push(data)
        print("Successful for adding new item")
        abcd = json.dumps(NewItemKey.values())
        pkpk = re.sub('[^a-zA-Z_0-9-]+', '', abcd)
        itemlist.append(data)
        itemlist_key.append(pkpk)
        """
        print abcd
        print data
        print pkpk"""
        time.sleep(5)


def connection():
    logging.info("Now I am connected with netpie")


def subscription(topic, message):
    logging.info(topic + " " + message)


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

        # print type(itemlist)
        # microgear.chat("outdoor/temp", '{"name":"Pocky"}')
        # microgear.chat("outdoor/temp", json.dumps(itemlist))
        # print ("sud song leaw na")""""""
        # while True:
        ActivateCamera()

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
    # getFromScan = 'Kitkat:P4:8/11/2018:3'
    # add new/remove product
    getFromScan = 'Coke:P4:8/10/2018:6'

    splitString = getFromScan.split(":")
    checkProductName = splitString[0]
    checkExpirydate = splitString[2]
    itemCode = splitString[3]
    # data = {"name": getFromScan}
    data = {'price': 30, 'Code': splitString[3], 'name': splitString[0], 'expiryDate': splitString[2]}
    checkDuplicate = False
    counterOuter = 0
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
                print i['Code']
                CodeString = json.dumps(i['Code'])
                cleanCodeString = CodeString.replace('"', '')
                listOfCode = cleanCodeString.split(',')
                counterInner = 0
                for itemID in listOfCode:

                    print 'U r in the new for loop'
                    # 4.1 itemCode(itemID) is duplicate
                    print 'itemID is ' + itemID
                    print 'itemCode is ' + itemCode
                    if itemID == itemCode:

                        # 5.1 array of Code is equal 1
                        if len(listOfCode) == 1:
                            # remove statement

                            print 'U are in the code is duplicate condition'

                            checkDuplicate = True
                            removeItemKey = itemlist_key[counterOuter]
                            print removeItemKey
                            forRemoveDupCode = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                            forRemoveDupCode.child(removeItemKey).delete()
                            # ref.child(removeItemKey).delete()
                            itemlist.pop(counterOuter)
                            itemlist_key.pop(counterOuter)
                            #
                            """   
                                    #
                            """
                            print ("Successful for removing item" + getFromScan)

                            time.sleep(5)
                            break
                        # 5.2 array of Code is greater than 1
                        else:
                            # delete item code from dict and update
                            # update statement

                            print 'Code  duplicate but length is greater than 1 condition'

                            checkDuplicate = True
                            removeItemKey = itemlist_key[counterOuter]
                            print removeItemKey

                            # for update duplicate product name and expirydate but itemCode(itemID)

                            # i['Code'] += ',' + itemCode

                            print counterInner
                            del listOfCode[counterInner]
                            newCode = json.dumps(listOfCode)
                            newCode1 = newCode.replace('"', '')
                            newCode2 = newCode1.replace('/', '')
                            newCode3 = newCode2.replace('[', '')
                            newCode4 = newCode3.replace(']', '')
                            newCode5 = newCode4.replace(' ', '')
                            forRemoveExCode = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                            forRemoveExCode.child(removeItemKey).child('Code').set(newCode5)

                            """   
                                    #
                            """
                            print ("Successful for removing item Code")

                            time.sleep(5)
                            break
                    counterInner += 1
                # 4.2 itemCode(itemID) is not duplicate
                else:
                    # update statement with append new itemCode into existing dict
                    print 'update'
                    checkDuplicate = True
                    removeItemKey = itemlist_key[counterOuter]
                    listOfCode.append(itemCode)
                    newCode = json.dumps(listOfCode)
                    newCode1 = newCode.replace('"', '')
                    newCode2 = newCode1.replace('/', '')
                    newCode3 = newCode2.replace('[', '')
                    newCode4 = newCode3.replace(']', '')
                    newCode5 = newCode4.replace(' ', '')
                    forupdateNewCode = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                    forupdateNewCode.child(removeItemKey).child('Code').set(newCode5)


            # 3.2 expiry date is not duplicate
            else:
                # add statement

                foraddnewDate = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')

                NewItemKey = foraddnewDate.push(data)
                print("Successful for adding new date")
                abcd = json.dumps(NewItemKey.values())
                pkpk = re.sub('[^a-zA-Z_0-9-]+', '', abcd)
                itemlist.append(data)
                itemlist_key.append(pkpk)
                time.sleep(5)
                break
        counterOuter += 1

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

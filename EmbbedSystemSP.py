import random

import microgear.client as microgear
import logging
from pyfirebase import Firebase
import time
import json
import re
import zbar
import cv2.cv as cv

firebase = Firebase('https://iotapplication-7cf10.firebaseio.com/')
appid = 'SmartFridge'
gearkey = 'YpZmMdcaemYKQLb'
gearsecret = 'I10EsM0ZTaI4PbDVHAWm3j96G'

microgear.create(gearkey, gearsecret, appid, {'debugmode': True})
# setup
# Create a Firebase reference
ref = firebase.ref('CustomerInfo')

itemlist = []

itemlist_key = []

# this line for get the data in firebase
itemRef = ref.child('-KqsdeuVyyatxKELuMs4').child('Item').get()

def RetreiveData():

    # create list for receive two sub lists
    a = []
    b = []

    # add only values inside itemlist
    [a.append(p.values()) for p in itemRef.values()]

    # add only keys inside itemlist_key
    [b.append(p) for p in itemRef.keys()]


    return  a,b


def ActivateCamera():
    capture = cv.CaptureFromCAM(0)

    # decalre the zbar_setter as zbar scanner
    zbar_scanner = zbar.ImageScanner()
    checkScan = False;
    while (checkScan == False):
        # create the variable as a frame of camera
        img = cv.QueryFrame(capture)
        height = int(img.height)
        width = int(img.width)

        SubRect = cv.GetSubRect(img, (1, 1, width - 1, height - 1))

        # cv.Rectangle(img,(0,0),(width,height),(255,0,0))

        # to create the image
        set_image = cv.CreateImage((SubRect.width, SubRect.height), cv.IPL_DEPTH_8U, 1)

        cv.ConvertImage(SubRect, set_image)

        image = zbar.Image(set_image.width, set_image.height, 'Y800', set_image.tostring())

        zbar_scanner.scan(image)

        for item in image:

            getFromScan = item.data

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

                        for itemID in listOfCode:
                            counterInner = 0
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
                                    microgear.chat("outdoor/temp", json.dumps(itemlist))
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
                                    microgear.chat("outdoor/temp", json.dumps(itemlist))
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
                            microgear.chat("outdoor/temp", json.dumps(itemlist))
                            time.sleep(5)
                            break


                    # 3.2 expiry date is not duplicate
                    else:
                        # add statement
                        checkDuplicate = True
                        foraddnewDate = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')

                        NewItemKey = foraddnewDate.push(data)
                        print("Successful for adding new date")
                        abcd = json.dumps(NewItemKey.values())
                        pkpk = re.sub('[^a-zA-Z_0-9-]+', '', abcd)
                        itemlist.append(data)
                        itemlist_key.append(pkpk)
                        microgear.chat("outdoor/temp", json.dumps(itemlist))
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
                microgear.chat("outdoor/temp", json.dumps(itemlist))
                """
                print abcd
                print data
                print pkpk"""
                time.sleep(5)
                break

        #cv.ShowImage("ISR Scanner", img)

        # less for fast video rendering
        cv.WaitKey(1)

# main function
# when this file are not running as module
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
        while True:
            ActivateCamera()

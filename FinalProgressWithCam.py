
import microgear.client as microgear
import logging

from pyfirebase import Firebase
import time
import json
import re

from datetime import  datetime
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

    # Get the contents from the reference

    # itemRef = ref.child('-KqsdeuVyyatxKELuMs4').child('Item').get()
    """"""
    # add only values inside itemlist
    a = []
    b = []
    # [a.append(p.values()) for p in itemRef.values()]

    for i in itemRef.values():
       
        a.append(i)
       
    [b.append(p) for p in itemRef.keys()]

   
    return a, b

def CreateArrayOfKeyDict(dictparam):

    cleanString = dictparam.replace('"','')
    listOfValues = cleanString.split(',')
    return  listOfValues

def ReplaceValuesInDict(listparam):
    Code1 = listparam.replace('"', '')
    Code2 = Code1.replace('/', '')
    Code3 = Code2.replace('[', '')
    Code4 = Code3.replace(']', '')
    Code5 = Code4.replace(' ', '')
    return Code5

def UpdateNewValuesDictKey(a):
    counter = 0
    newValues = ''
    for idex in a:
        if counter == len(a) - 1:
            newValues += idex
        else:
            newValues += idex + ','
        counter += 1
    return newValues

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
            priceOfdata = splitString[1]
            checkExpirydate = splitString[2]
            itemCode = splitString[3]
            
            data = {'price': 30 , 'Code': splitString[3], 'name': splitString[0], 'expiryDate': splitString[2], 'Checkin': str(datetime.now())}
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
                       
                        print i['Code']
                        list_of_ItemCode = CreateArrayOfKeyDict(json.dumps(i['Code']))
                        list_of_Checkin = CreateArrayOfKeyDict(json.dumps(i['Checkin']))
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

                                    # create new data
                                    checkoutData = data = {'price': 30, 'Code': itemCode, 'name': checkProductName,
                                                           'expiryDate': checkExpirydate,
                                                           'Checkin': list_of_Checkin[counterInner],
                                                           'Checkout': str(datetime.now())}
                                    # add to usage database
                                    usageItem = firebase.ref('Usage')
                                    usageItem.push(checkoutData)

                                    itemlist.pop(counterOuter)
                                    itemlist_key.pop(counterOuter)

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

                                    # update item code
                                    list_of_ItemCode.remove(itemID)
                                    # getting new values to update data in firebase
                                    newCode5 = ReplaceValuesInDict(json.dumps(list_of_ItemCode))
                                    # update values in firebase
                                    forRemoveExCode = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                                    forRemoveExCode.child(removeItemKey).child('Code').set(newCode5)
                                    # update local database
                                    i['Code'] = UpdateNewValuesDictKey(list_of_ItemCode)

                                    # create new data
                                    checkoutData = data = {'price': 30, 'Code': itemCode, 'name': checkProductName,
                                                           'expiryDate': checkExpirydate, 'Checkin': list_of_Checkin[counterInner],
                                                           'Checkout': str(datetime.now())}
                                    # update check in
                                    list_of_Checkin.pop(counterInner)
                                    updateCheckinValues = ReplaceValuesInDict(json.dumps(list_of_Checkin))
                                    forupdateNewCheckin = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                                    forupdateNewCheckin.child(removeItemKey).child('Checkin').set(updateCheckinValues)

                                    i['Checkin'] = UpdateNewValuesDictKey(list_of_Checkin)

                                    # add to usage database

                                    usageItem = firebase.ref('Usage')
                                    usageItem.push(checkoutData)

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

                            # update item code
                            # add new code to list
                            list_of_ItemCode.append(itemCode)
                            # getting new values to update data in firebase
                            newCode5 = ReplaceValuesInDict(json.dumps(list_of_ItemCode))
                            # update values in firebase
                            forupdateNewCode = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                            forupdateNewCode.child(removeItemKey).child('Code').set(newCode5)
                            # update local database
                            i['Code'] = UpdateNewValuesDictKey(list_of_ItemCode)

                            # update check in
                            # add new check in time to list
                            list_of_Checkin.append(data['Checkin'])
                            # getting new values to update data in firebase
                            newCodeForCheckin = ReplaceValuesInDict(json.dumps(list_of_Checkin))
                            # update values in firebase
                            forupdateNewCheckin = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                            forupdateNewCheckin.child(removeItemKey).child('Checkin').set(newCodeForCheckin)
                            # update local database
                            i['Checkin'] = UpdateNewValuesDictKey(list_of_Checkin)

                            microgear.chat("outdoor/temp", json.dumps(itemlist))
                            time.sleep(5)
                            break


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
                time.sleep(5)
                break;

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
        microgear.chat("outdoor/temp", json.dumps(itemlist))
        
        while True:
            ActivateCamera()

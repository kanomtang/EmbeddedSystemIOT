import microgear.client as microgear
import logging
import io
import picamera
from PIL import Image
from pyfirebase import Firebase
import time
import json
import re

from datetime import datetime
import zbar
import cv2.cv as cv

firebase = Firebase('https://iotapplication-7cf10.firebaseio.com/')
itemlist = []
itemlist_key = []
ref = firebase.ref('CustomerInfo')
ref1 = firebase.ref('CustomerInfo')
itemRef = ref.child('-KqsdeuVyyatxKELuMs4').child('Item').get()
InfoRef = ref1.child('-KqsdeuVyyatxKELuMs4').get()
appid = 'SmartFridge'
gearkey = 'YpZmMdcaemYKQLb'
gearsecret = 'I10EsM0ZTaI4PbDVHAWm3j96G'

microgear.create(gearkey, gearsecret, appid, {'debugmode': True})

def connection():
    logging.info("Now I am connected with netpie")


def subscription(topic, message):
    logging.info(topic + " " + message)


def disconnect():
    logging.debug("disconnect is work")

def createArrayOfKeyDict(dictparam):
    cleanString = dictparam.replace('"', '')
    listOfValues = cleanString.split(',')
    return listOfValues


def replaceValuesInDict(listparam):
    Code1 = listparam.replace('"', '')
    Code2 = Code1.replace('/', '')
    Code3 = Code2.replace('[', '')
    Code4 = Code3.replace(']', '')
    Code5 = Code4.replace(' ', '')
    return Code5


def updateNewValuesDictKey(a):
    counter = 0
    newValues = ''
    for idex in a:
        if counter == len(a) - 1:
            newValues += idex
        else:
            newValues += idex + ','
        counter += 1
    return newValues


def RetreiveData():
    # Get the contents from the reference

    a = []
    b = []
    c = []
    CustomerInfo = ''
    # extract customer info city and province
    for i in InfoRef.values():
        c.append(i)
        # 0 = last name
        # 1 = item list
        # 2 = province
        # 3 = first name
        # 4 = City
    CustomerInfo = c[4] + ',' + c[2]
    # print CustomerInfo
    for i in itemRef.values():
        # arrayString = i.split(",")
        # print json.dumps(i)
        # a.append(json.dumps(i))
        a.append(i)
    # add only keys inside itemlist_key
    [b.append(p) for p in itemRef.keys()]
    return a, b, CustomerInfo


def ActivateCamera():
    # set camera
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.start_preview(fullscreen=False,window=(1500,50,480,480))
        time.sleep(2)
        camera.capture(stream, format='jpeg')
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    pil = Image.open(stream)
    # set scanner
    scanner = zbar.ImageScanner()

    # configure the reader
    scanner.parse_config('enable')

    pil = pil.convert('L')
    width, height = pil.size
    raw = pil.tostring()

    # wrap image data
    image = zbar.Image(width, height, 'Y800', raw)

    # scan the image for barcodes
    scanner.scan(image)
    # reading qr code from image => for item in image
    for symbol in image:
        getFromScan = symbol.data
        # split string
        splitString = getFromScan.split(":")
        # setting data
        checkProductName = splitString[0]
        priceOfdata = splitString[1]
        checkExpirydate = splitString[2]
        itemCode = splitString[3]
        data = {'price': splitString[1], 'Code': splitString[3], 'name': splitString[0], 'expiryDate': splitString[2],
                'Checkin': str(datetime.now())}
        checkDuplicate = False
        codeDuplicate = False
        counterOuter = 0

        # 1.1 for loop item list
        for item in itemlist:

            # 1.1 duplicate name
            if item['name'] == data['name']:
                checkDuplicate = True

                # 2.1 duplicate date
                if item['expiryDate'] == data['expiryDate']:

                    list_of_ItemCode = createArrayOfKeyDict(json.dumps(item['Code']))
                    list_of_Checkin = createArrayOfKeyDict(json.dumps(item['Checkin']))
                    counterInner = 0
                    for itemID in list_of_ItemCode:

                        # 3.1 duplicate code
                        if itemID == data['Code']:
                            codeDuplicate = True

                            # 4.1 len == 1
                            if len(list_of_ItemCode) == 1:

                                removeItemKey = itemlist_key[counterOuter]
                                print removeItemKey
                                forRemoveDupCode = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                                forRemoveDupCode.child(removeItemKey).delete()
                                checkoutData = {'price': splitString[1], 'Code': itemCode, 'name': checkProductName,
                                                'expiryDate': checkExpirydate,
                                                'Checkin': list_of_Checkin[counterInner],
                                                'Checkout': str(datetime.now()),
                                                'Province': 'Chiang Mai'}
                                usageItem = firebase.ref('Usage')
                                usageItem.push(checkoutData)

                                itemlist.pop(counterOuter)
                                itemlist_key.pop(counterOuter)
                                time.sleep(10)
                                return True
                            # 4.2 len > 1
                            else:
                                removeItemKey = itemlist_key[counterOuter]
                                print removeItemKey

                                # update item code
                                list_of_ItemCode.remove(itemID)
                                # getting new values to update data in firebase
                                newCode5 = replaceValuesInDict(json.dumps(list_of_ItemCode))
                                # update values in firebase
                                forRemoveExCode = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                                forRemoveExCode.child(removeItemKey).child('Code').set(newCode5)
                                # update local database
                                item['Code'] = updateNewValuesDictKey(list_of_ItemCode)

                                # create new data
                                checkoutData = {'price': splitString[1], 'Code': itemCode, 'name': checkProductName,
                                                'expiryDate': checkExpirydate,
                                                'Checkin': list_of_Checkin[counterInner],
                                                'Checkout': str(datetime.now()),
                                                'Province': 'Chiang Mai'}
                                # update check in
                                list_of_Checkin.pop(counterInner)
                                # updateCheckinValues = replaceValuesInDict(json.dumps(list_of_Checkin))
                                forupdateNewCheckin = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                                forupdateNewCheckin.child(removeItemKey).child('Checkin').set(updateCheckinValues)

                                item['Checkin'] = updateNewValuesDictKey(list_of_Checkin)

                                # add to usage database

                                usageItem = firebase.ref('Usage')
                                usageItem.push(checkoutData)
                                time.sleep(10)
                                return True
                        counterInner += 1
                    # 3.2 not duplicate code
                    if codeDuplicate == False:
                        removeItemKey = itemlist_key[counterOuter]

                        # update item code
                        # add new code to list
                        list_of_ItemCode.append(itemCode)
                        # getting new values to update data in firebase
                        newCode5 = replaceValuesInDict(json.dumps(list_of_ItemCode))
                        # update values in firebase
                        forupdateNewCode = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                        forupdateNewCode.child(removeItemKey).child('Code').set(newCode5)
                        # update local database
                        item['Code'] = updateNewValuesDictKey(list_of_ItemCode)

                        # update check in
                        # add new check in time to list
                        list_of_Checkin.append(data['Checkin'])
                        # getting new values to update data in firebase
                        newCodeForCheckin = replaceValuesInDict(json.dumps(list_of_Checkin))
                        # # update values in firebase
                        forupdateNewCheckin = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                        forupdateNewCheckin.child(removeItemKey).child('Checkin').set(newCodeForCheckin)
                        # update local database
                        item['Checkin'] = updateNewValuesDictKey(list_of_Checkin)
                        time.sleep(10)
                        return True
                else:
                    foraddnewDate = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')

                    NewItemKey = foraddnewDate.push(data)

                    abcd = json.dumps(NewItemKey.values())
                    pkpk = re.sub('[^a-zA-Z_0-9-]+', '', abcd)
                    itemlist.append(data)
                    itemlist_key.append(pkpk)

                    time.sleep(10)
                    return True
            counterOuter += 1

        if checkDuplicate == False:
            foraddNewitemRef = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')

            NewItemKey = foraddNewitemRef.push(data)

            abcd = json.dumps(NewItemKey.values())
            pkpk = re.sub('[^a-zA-Z_0-9-]+', '', abcd)
            itemlist.append(data)
            itemlist_key.append(pkpk)
            time.sleep(10)


if __name__ == "__main__":
    microgear.setalias("MyRaspberryPI")
    microgear.on_connect = connection
    microgear.on_message = subscription
    microgear.on_disconnect = disconnect
    microgear.subscribe("/mails")
    microgear.connect(False)

    if (microgear.connected):
        itemlist, itemlist_key, CustomerAddress = RetreiveData()
        microgear.chat("outdoor/temp", json.dumps(itemlist))

        itemlist, itemlist_key, CustomerAddress = RetreiveData()
        while True:
            ActivateCamera()

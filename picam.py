
#import microgear.client as microgear
import logging

from pyfirebase import Firebase
import time
import json
import re

from datetime import  datetime
#import zbar
#import cv2.cv as cv

firebase = Firebase('https://iotapplication-7cf10.firebaseio.com/')
itemlist = []
itemlist_key = []
ref = firebase.ref('CustomerInfo')
ref1 = firebase.ref('CustomerInfo')
itemRef = ref.child('-KqsdeuVyyatxKELuMs4').child('Item').get()
InfoRef = ref1.child('-KqsdeuVyyatxKELuMs4').get()


def createArrayOfKeyDict(dictparam):
    cleanString = dictparam.replace('"','')
    listOfValues = cleanString.split(',')
    return  listOfValues

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
    # set scanner

    # reading qr code from image => for item in image

    # In for
    getFromScan = "Coke:P4:8/10/2018:6:8"
    # split string
    splitString = getFromScan.split(":")
    # setting data
    checkProductName = splitString[0]
    priceOfdata = splitString[1]
    checkExpirydate = splitString[2]
    itemCode = splitString[3]
    data = {'price': splitString[1], 'Code': splitString[3], 'name': splitString[0], 'expiryDate': splitString[2], 'Checkin': str(datetime.now())}
    checkDuplicate = False
    codeDuplicate = False
    counterOuter = 0

    print itemlist
    print itemlist_key
    # 1.1 for loop item list
    for item in itemlist:
        print "item name is "
        print item
        # 1.1 duplicate name
        if item['name'] == data['name']:
            checkDuplicate = True
            print "duplicate name"
            # 2.1 duplicate date
            if item['expiryDate'] == data['expiryDate']:
                print "duplicate date"
                list_of_ItemCode = createArrayOfKeyDict(json.dumps(item['Code']))
                list_of_Checkin = createArrayOfKeyDict(json.dumps(item['Checkin']))
                counterInner = 0
                for itemID in list_of_ItemCode:

                    # 3.1 duplicate code
                    if itemID == data['Code']:
                        codeDuplicate = True
                        print "duplicate code"
                        # 4.1 len == 1
                        if len(list_of_ItemCode) == 1:
                            print "len  = 1 "
                            removeItemKey = itemlist_key[counterOuter]
                            print removeItemKey
                            # forRemoveDupCode = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                            # forRemoveDupCode.child(removeItemKey).delete()
                            checkoutData = data = {'price': splitString[1], 'Code': itemCode, 'name': checkProductName,
                                                   'expiryDate': checkExpirydate,
                                                   'Checkin': list_of_Checkin[counterInner],
                                                   'Checkout': str(datetime.now()),
                                                   'Province': 'Chiang Mai'}
                            # usageItem = firebase.ref('Usage')
                            # usageItem.push(checkoutData)

                            itemlist.pop(counterOuter)
                            itemlist_key.pop(counterOuter)

                            print ("Successful for removing item" + getFromScan)
                            break
                        # 4.2 len > 1
                        else:
                            print "len > 1 "
                            removeItemKey = itemlist_key[counterOuter]
                            print removeItemKey

                            # update item code
                            list_of_ItemCode.remove(itemID)
                            # getting new values to update data in firebase
                            newCode5 = replaceValuesInDict(json.dumps(list_of_ItemCode))
                            # update values in firebase
                            # forRemoveExCode = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                            # forRemoveExCode.child(removeItemKey).child('Code').set(newCode5)
                            # update local database
                            item['Code'] = updateNewValuesDictKey(list_of_ItemCode)

                            # create new data
                            checkoutData = data = {'price': splitString[1], 'Code': itemCode, 'name': checkProductName,
                                                   'expiryDate': checkExpirydate,
                                                   'Checkin': list_of_Checkin[counterInner],
                                                   'Checkout': str(datetime.now()),
                                                   'Province': 'Chiang Mai'}
                            # update check in
                            list_of_Checkin.pop(counterInner)
                            # updateCheckinValues = replaceValuesInDict(json.dumps(list_of_Checkin))
                            # forupdateNewCheckin = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                            # forupdateNewCheckin.child(removeItemKey).child('Checkin').set(updateCheckinValues)

                            item['Checkin'] = updateNewValuesDictKey(list_of_Checkin)

                            # add to usage database

                            # usageItem = firebase.ref('Usage')
                            # usageItem.push(checkoutData)

                            print ("Successful for removing item Code")

                            break
                    counterInner += 1
                # 3.2 not duplicate code
                if codeDuplicate == False:
                    print "not duplicate code"
                    removeItemKey = itemlist_key[counterOuter]

                    # update item code
                    # add new code to list
                    list_of_ItemCode.append(itemCode)
                    # getting new values to update data in firebase
                    # newCode5 = replaceValuesInDict(json.dumps(list_of_ItemCode))
                    # update values in firebase
                    # forupdateNewCode = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                    # forupdateNewCode.child(removeItemKey).child('Code').set(newCode5)
                    # update local database
                    item['Code'] = updateNewValuesDictKey(list_of_ItemCode)

                    # update check in
                    # add new check in time to list
                    list_of_Checkin.append(data['Checkin'])
                    # getting new values to update data in firebase
                    # newCodeForCheckin = replaceValuesInDict(json.dumps(list_of_Checkin))
                    # # update values in firebase
                    # forupdateNewCheckin = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                    # forupdateNewCheckin.child(removeItemKey).child('Checkin').set(newCodeForCheckin)
                    # update local database
                    item['Checkin'] = updateNewValuesDictKey(list_of_Checkin)
                    break
            else:
                print "not duplicate date"
                # foraddnewDate = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                #
                # NewItemKey = foraddnewDate.push(data)

                # abcd = json.dumps(NewItemKey.values())
                # pkpk = re.sub('[^a-zA-Z_0-9-]+', '', abcd)
                itemlist.append(data)
                # itemlist_key.append(pkpk)
                itemlist_key.append("just test")
                print("Successful for adding new date")
                break
        counterOuter += 1

    if checkDuplicate == False:
        print "new item Hola!!!"
        # foraddNewitemRef = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
        #
        # NewItemKey = foraddNewitemRef.push(data)

        abcd = json.dumps(NewItemKey.values())
        pkpk = re.sub('[^a-zA-Z_0-9-]+', '', abcd)
        itemlist.append(data)
        itemlist_key.append(pkpk)
        print("Successful for adding new item")
    time.sleep(10)


if __name__ == "__main__":
    # microgear.setalias("MyRaspberryPI")
    # microgear.on_connect = connection
    # microgear.on_message = subscription
    # microgear.on_disconnect = disconnect
    # microgear.subscribe("/mails")
    # microgear.connect(False)

    # if (microgear.connected):
    #     itemlist, itemlist_key, CustomerAddress = RetreiveData()
    #     microgear.chat("outdoor/temp", json.dumps(itemlist))
        
    #     while True:

    itemlist, itemlist_key, CustomerAddress = RetreiveData()
    while True:

        ActivateCamera()
    # print itemlist
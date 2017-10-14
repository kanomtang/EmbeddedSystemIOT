from pyfirebase import Firebase
import time
import json
import re
firebase = Firebase('https://iotapplication-7cf10.firebaseio.com/')

# setup
# Create a Firebase reference
ref = firebase.ref('CustomerInfo')

itemlist = []

itemlist_key = []


# this method for get the data in firebase




itemRef = ref.child('-KqsdeuVyyatxKELuMs4').child('Item').get()

def RetreiveData():
    # Get the contents from the reference

    #itemRef = ref.child('-KqsdeuVyyatxKELuMs4').child('Item').get()
    """"""
    # add only values inside itemlist
    a = []
    b= []
    [a.append(p.values()) for p in itemRef.values()]

    # add only keys inside itemlist_key
    [b.append(p) for p in itemRef.keys()]

    """
   for i in itemlist_key:
        print i
    for i in itemlist:
        print i
"""
    return  a,b


def ActivateCamera():
    print 'key values in local list'
    for i in itemlist_key:

        print i
    print 'values in local list'
    for i in itemlist:

        print i
    getFromScan = '1805461'
    checkExisting = [getFromScan]
    data = {"name": getFromScan}
    checkDuplicate = False
    counter = 0
    """"""

    for i in itemlist:
        print 'now is on the for loop'
        print (i)

        if checkExisting == i:
            print 'U are in the duplicate condition'
            print checkExisting
            checkDuplicate = True
            removeItemKey = itemlist_key[counter]
            print removeItemKey
            forremove = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
            forremove.child(removeItemKey).delete()
            #ref.child(removeItemKey).delete()
            itemlist.pop(counter)
            itemlist_key.pop(counter)
            #
            """   

                    #
            """
            print ("Successful for removing item" + getFromScan)

            time.sleep(5)
            break

        counter += 1

    if checkDuplicate == False:
        foraddNewitemRef = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
        #NewItemKey = ref.push(data)
        NewItemKey = foraddNewitemRef.push(data)
        print("Successful for adding new item" )
        abcd = json.dumps(NewItemKey.values())

        #pkpk = re.sub('[^a-zA-Z_0-9]+', '', abcd)
        pkpk = re.sub('[^a-zA-Z_0-9-]+', '', abcd)
        itemlist.append(checkExisting)
        #itemlist_key.append('-'+pkpk)
        itemlist_key.append(pkpk)
        print abcd
        print checkExisting
        print pkpk
        time.sleep(5)




# main function
# when this file are not running as module
if __name__ == "__main__":
    # to define the name of window and adjust the window with autosize


    print ('Welcome to ISR')
    itemlist, itemlist_key = RetreiveData()
    while True:
        ActivateCamera()

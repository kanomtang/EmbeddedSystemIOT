from pyfirebase import Firebase
import time
import json
import re
import zbar
import cv2.cv as cv

firebase = Firebase('https://iotapplication-7cf10.firebaseio.com/')

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
            checkExisting = [getFromScan]
            data = {"name": getFromScan}
            checkDuplicate = False
            counter = 0


            for i in itemlist:


                if checkExisting == i:

                    checkDuplicate = True
                    removeItemKey = itemlist_key[counter]
                    print removeItemKey
                    forremove = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')
                    forremove.child(removeItemKey).delete()

                    itemlist.pop(counter)
                    itemlist_key.pop(counter)

                    print ("Successful for removing item" + getFromScan)

                    time.sleep(3)
                    return False

                counter += 1

            if checkDuplicate == False:
                foraddNewitemRef = firebase.ref('CustomerInfo/-KqsdeuVyyatxKELuMs4/Item')

                NewItemKey = foraddNewitemRef.push(data)
                print("Successful for adding new item" )
                abcd = json.dumps(NewItemKey.values())


                pkpk = re.sub('[^a-zA-Z_0-9-]+', '', abcd)
                itemlist.append(checkExisting)

                itemlist_key.append(pkpk)

                time.sleep(3)
                return True

        cv.ShowImage("ISR Scanner", img)

        # less for fast video rendering
        cv.WaitKey(1)

# main function
# when this file are not running as module
if __name__ == "__main__":
    # to define the name of window and adjust the window with autosize


    print ('Welcome to ISR')
    itemlist, itemlist_key = RetreiveData()
    while True:
        ActivateCamera()

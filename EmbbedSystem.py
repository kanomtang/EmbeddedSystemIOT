import zbar
import cv2.cv as cv
import time
from pyrebase import pyrebase

config = {
  "apiKey": "AIzaSyCFXny8pflQwLu9AyQu8ve9xI6qA9KR7PM",
  "authDomain": "iotapplication-7cf10.firebaseapp.com",
  "databaseURL": "https://iotapplication-7cf10.firebaseio.com",
  "storageBucket": "iotapplication-7cf10.appspot.com"

}
#setup configuration
firebase = pyrebase.initialize_app(config)
db = firebase.database()
itemlist = []


def RetreiveData():
    itemlistInFirebase = db.child("CustomerInfo").child("-KqsdeuVyyatxKELuMs4").child("Item").get()

    if itemlistInFirebase:
        for item in itemlistInFirebase.each():

          itemlist.append(item.val())
        return  True
    else:
        return False


def ActivateCamera():
    capture = cv.CaptureFromCAM(0)

    # decalre the zbar_setter as zbar scanner
    zbar_scanner = zbar.ImageScanner()

    while True:

        checkDuplicate = False


     # create the variable as a frame of camera
        img = cv.QueryFrame(capture)

        height = int(img.height)
        width = int(img.width)

        SubRect = cv.GetSubRect(img, (1, 1, width - 1, height - 1))

        cv.Rectangle(img, (0, 0), (width, height), (255, 0, 0))

        # to create the image
        set_image = cv.CreateImage((SubRect.width, SubRect.height), cv.IPL_DEPTH_8U, 1)

        cv.ConvertImage(SubRect, set_image)

        image = zbar.Image(set_image.width, set_image.height, 'Y800', set_image.tostring())

        zbar_scanner.scan(image)


        for item in image:

            data = {"name": item.data}
            justchecking = item.data

            for i in itemlist:
                print(i.values())
                # checking if the item is on the itemlist it will remove it
                if justchecking in i.values():
                    checkDuplicate = True

                return False
            # checking if the item doesn't exist the itemlist it will append it
            if checkDuplicate == False:
                db.child("CustomerInfo").child("-KqsdeuVyyatxKELuMs4").child("Item").push(data)

                return True
            #itemlist.append(item.data)

            # cv.ShowImage("ISR Scanner", img)

        # less for fast video rendering
        cv.WaitKey(1)
        time.sleep(2)


if __name__ == "__main__":
    RetreiveData()
    ActivateCamera()

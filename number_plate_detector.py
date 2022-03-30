import cv2
import pytesseract as pytes
# Read images videos and webcam
#use 0 to use default webcam


#Number plate detector project


################## Parameters

pytes.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
OutputWidth = 640   #Window properties
OutputHeight = 480
minArea =  1000
numberplateText = "none"

textColor = (255, 0, 255)
#cascade of the image
numberPlateCascade = cv2.CascadeClassifier("../Recources/haarcascade_russian_plate_number.xml")
####################

#define camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, OutputWidth)
cap.set(10, OutputHeight)
count = 0

while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = numberPlateCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        area = w*h
        if area>minArea:
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            cv2.putText(img, str(numberplateText), (x,y-5),
                        cv2.FONT_HERSHEY_COMPLEX,1 , textColor, 2)
            #cropping the image
            imgRoi = img[y:y+h, x:x+w]
            numberplateText = (pytes.image_to_string(imgRoi,
                                                     config=f'--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))
        cv2.imshow("Video", img)



    cv2.imshow("Video", img)



    #press f to break the loop
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("Recources/Scanned/NoPlate_"+str(count)+".jpg", imgRoi)
        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img,"Scan Saved", (150, 265), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 2)
        cv2.imshow("Result", img)
        cv2.waitKey(500)
        count +=1

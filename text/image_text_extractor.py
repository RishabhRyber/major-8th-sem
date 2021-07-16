
import pytesseract
from PIL import Image
from imutils import contours
from imutils.perspective import four_point_transform
import numpy as np
import imutils
from skimage.filters import threshold_local
import cv2 
import os
import traceback


for file in os.listdir("/home/dell/Text-Extraction-From-Image/img_folder"):
    if file.endswith(".jpg"):
        path_of_file = "/home/dell/Text-Extraction-From-Image/img_folder/" + str(file)
      
        pic = cv2.imread(path_of_file)
        
        original_pic = pic.copy()

        
        grey = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(grey, (5,5) ,0)
        edged = cv2.Canny(grey, 75, 200)

        thresh = cv2.threshold(grey, 225, 255, cv2.THRESH_BINARY_INV)[1]

        (_, counts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
        cv2.drawContours(pic, counts, -1, (240, 0, 159), 3)

        H,W = pic.shape[:2]
        for cnt in counts:
            x,y,w,h = cv2.boundingRect(cnt)
            if cv2.contourArea(cnt) > 100 and (0.7 < w/h < 1.3) and (W/4 < x + w//2 < W*3/4) and (H/4 < y + h//2 < H*3/4):
                break

        
        mask = np.zeros(pic.shape[:2],np.uint8)
        cv2.drawContours(mask, [cnt],-1, 255, -1)
        dst = cv2.bitwise_and(pic, pic, mask=mask)

        grey = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        grey = cv2.medianBlur(grey, 3)
        grey = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        text_form_name = "/home/dell/Text-Extraction-From-Image/img_folder/" + str(file[:-4]) + "-text_form.png" 
        cv2.imwrite(text_form_name, dst)
      
        text = pytesseract.image_to_string(Image.open(text_form_name))
        text_file_name = "/home/dell/Text-Extraction-From-Image/img_folder/" + str(file[:-4]) + "-text_form.txt" 
        with open(text_file_name, "a") as f:
            f.write(text + "\n")
       

import numpy as np
import cv2


class MedicineColorDetection:

    def __init__(self):
        self.boundries={'blue':[np.array([100,150,0],np.uint8),np.array([140,255,255],np.uint8)]}

    @staticmethod
    def calcPercentage(msk):
        height, width = msk.shape[:2]
        num_pixels = height * width
        count_white = cv2.countNonZero(msk)
        percent_white = (count_white/num_pixels) * 100
        percent_white = round(percent_white,2)
        return percent_white

    def createMask(self,img):
        image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image, self.boundries['blue'][0], self.boundries['blue'][1])
        return mask

    def detectMedecineCategorie(self,img):
        mask=self.createMask(img)
        blue_pourcentage=MedicineColorDetection.calcPercentage(mask)
        return "500mg" if blue_pourcentage > 2 else "1g"
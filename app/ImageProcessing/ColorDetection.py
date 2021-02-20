import cv2
import operator

class MedicineColorDetection:

    def __init__(self):
        self.boundries = {
            'aspegic': {
                "500mg": [(90, 50, 70), (128, 255, 255)],
                "1g": [(159, 50, 70), (180, 255, 255)]
            }
        }

        self.pourcentages = {
            'aspegic': {
                "500mg": 50.93,
                "1g": 47.63
            }
        }

    @staticmethod
    def calcule_white_surface(msk):
        height, width = msk.shape[:2]
        num_pixels = height * width
        count_white = cv2.countNonZero(msk)
        percent_white = (count_white/num_pixels) * 100
        percent_white = round(percent_white,2)
        return percent_white

    @staticmethod
    def calculate_categories_pourcentage(msk, pourcentage):
        percent_white = MedicineColorDetection.calcule_white_surface(msk)
        pourcentage_color = (percent_white * 100) / pourcentage
        return pourcentage_color

    def get_categorie(self,image, medicine):
        pourcentage_categories = {}
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        for dosage, color_boundary in self.boundries[medicine].items():
            mask = cv2.inRange(image, color_boundary[0], color_boundary[1])
            pourcentage_categories[dosage] = MedicineColorDetection.calculate_categories_pourcentage(mask, self.pourcentages[medicine][dosage])
        return max(pourcentage_categories.items(), key=operator.itemgetter(1))[0]

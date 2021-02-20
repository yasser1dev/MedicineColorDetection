import shutil
from pathlib import Path
import uvicorn
from fastapi import FastAPI, File, UploadFile
from ImageProcessing import  ColorDetection
import cv2 as cv
import os
UPLOAD_FOLDER="Images/"
EXTENSIONS=set(['png', 'jpg', 'jpeg'])

app = FastAPI()

@app.post("/uploadImg/{medicine_name}")
def upload_img(medicine_name,uploadedfile: UploadFile = File(...)):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if(uploadedfile.filename.split('.')[1].lower() in EXTENSIONS):
        uploadedfile.file.seek(0)
        destination = Path(UPLOAD_FOLDER + uploadedfile.filename)
        try:
            with destination.open("wb") as buffer:
                shutil.copyfileobj(uploadedfile.file, buffer)
        finally:
            uploadedfile.file.close()
            imgName = UPLOAD_FOLDER + uploadedfile.filename
            pp=ColorDetection.MedicineColorDetection()
            img=cv.imread(imgName)
            return pp.get_categorie(img,medicine_name)
    else :
        return 'extension not allowed'
if __name__ == '__main__':
    uvicorn.run( "main:app", host="0.0.0.0", port=8000, reload=True, access_log=False, forwarded_allow_ips="*")



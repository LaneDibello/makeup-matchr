from msilib.schema import Error
import cv2
from PIL import Image
import os, sys

sys.path.insert(1, '../../WB_sRGB/WB_sRGB_Python/')

from classes import WBsRGB as wb_srgb

UPGRADED_MODEL : int  = 1;
GAMUT_MAPPIGN : int = 2;
IMG_SHOW : int = 0;

def correctImage(in_image : Image):
    try:
        wbModel = wb_srgb.WBsRGB(gamut_mapping=GAMUT_MAPPIGN,upgraded=UPGRADED_MODEL);
        Img = cv2.imread(in_image); # image read conver from PIL to cv2
        outImg = wbModel.correctImage(Img);
        return outImg;
    except:
        print("Error: Could not correct given image");
        return in_image;



if __name__ == '__main__':
    print("pass");
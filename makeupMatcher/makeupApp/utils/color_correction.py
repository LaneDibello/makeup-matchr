import cv2
from PIL import Image
import os, sys

import numpy
from makeupApp.utils.classes import WBsRGB as wb_srgb

UPGRADED_MODEL : int  = 1;
GAMUT_MAPPIGN : int = 2;
IMG_SHOW : int = 0;

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
  (h, w) = image.shape[:2]

  if width is None and height is None:
    return image
  if width is None:
    r = height / float(h)
    dim = (int(w * r), height)
  else:
    r = width / float(w)
    dim = (width, int(h * r))

  return cv2.resize(image, dim, interpolation=inter)

'''@param: img PIL Image '''
'''@return: outImg  OpenCV or None'''
def CorrectImage(basedir, url) -> str:
    I = cv2.imread(basedir + url);
    wbModel = wb_srgb.WBsRGB(gamut_mapping=GAMUT_MAPPIGN,upgraded=UPGRADED_MODEL)
    outImg =  wbModel.correctImage(I)
    file_url = f'{url[1:]}_result.jpg'
    cv2.imwrite(file_url, outImg * 255)
    return file_url


# input and options
in_img = 'figure3.jpg'  # input image filename

imshow = 1  # show input/output image

if __name__ == '__main__':
  os.makedirs('.', exist_ok=True)
  pill_image = Image.open(in_img);
  outImg = CorrectImage(pill_image);
  cv2.imwrite('./' + 'result.jpg', outImg * 255);

  if IMG_SHOW:
    cv2.imshow('our result', ResizeWithAspectRatio(outImg, width=800))
    cv2.waitKey()
    cv2.destroyAllWindows()
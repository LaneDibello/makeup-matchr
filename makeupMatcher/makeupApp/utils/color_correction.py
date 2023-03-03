import cv2
from PIL import Image
import os, sys

import numpy
from classes import WBsRGB as wb_srgb

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

def CorrectImage(img : Image):
  try:
    wbModel = wb_srgb.WBsRGB(gamut_mapping=GAMUT_MAPPIGN, upgraded=UPGRADED_MODEL);
    # transform PIL to openCV
    open_cv_img = numpy.array(img);
    open_cv_img = open_cv_img[:, :, ::-1].copy();
    outImg = wbModel.correctImage(open_cv_img); # pass the opencv convertion
    return outImg;
  except:
    print("Error: Image could not be proccessed");
    return None;


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
import cv2
from PIL import Image
import os, sys
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


# input and options
in_img = 'figure3.jpg'  # input image filename
out_dir = '.'  # output directory
# use upgraded_model= 1 to load our new model that is upgraded with new
# training examples.
upgraded_model = 1
# use gamut_mapping = 1 for scaling, 2 for clipping (our paper's results
# reported using clipping). If the image is over-saturated, scaling is
# recommended.
gamut_mapping = 2
imshow = 1  # show input/output image

# processing
# create an instance of the WB model
wbModel = wb_srgb.WBsRGB(gamut_mapping=gamut_mapping,
                         upgraded=upgraded_model)
os.makedirs(out_dir, exist_ok=True)
I = cv2.imread(in_img)  # read the image
outImg = wbModel.correctImage(I)  # white balance it
cv2.imwrite(out_dir + '/' + 'result.jpg', outImg * 255)  # save it

if imshow == 1:
  cv2.imshow('input', ResizeWithAspectRatio(I, width=800))
  cv2.imshow('our result', ResizeWithAspectRatio(outImg, width=800))
  cv2.waitKey()
  cv2.destroyAllWindows()
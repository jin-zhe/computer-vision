import cv2.cv as cv
import numpy as np
import math
import cv2
import os

""" read in image from input path into memory as a color image """
def read_color_image(path):
  return cv2.imread(path, cv2.CV_LOAD_IMAGE_COLOR)

""" read in image from input path into memory as a grayscale image """
def read_grayscale_image(path):
  return cv2.imread(path, cv2.CV_LOAD_IMAGE_GRAYSCALE)

""" read in video capture """
def read_video(path):
  return cv2.VideoCapture(path)

""" writes image to ouput path with given filename """
def write_image(path, image):
  cv2.imwrite(path, image)

""" displays image for checking """
def display_image(image):
  cv2.imshow('image',image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
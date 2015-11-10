from matplotlib import pyplot as plt
import cv2.cv as cv
import numpy as np
import cPickle
import time
import math
import cv2
import os

""" read in image from input path into memory as a color image """
def read_color_image(path):
  return cv2.imread(path, cv2.CV_LOAD_IMAGE_COLOR)

""" read in image from input path into memory as a grayscale image """
def read_grayscale_image(path):
  return cv2.imread(path, cv2.CV_LOAD_IMAGE_GRAYSCALE)

""" returns the grayscale image from a color image """
def get_grayscale(color_image):
  return cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

""" convert image to hsv colorspace """
def get_HSV(BGR_image):
  return cv2.cvtColor(BGR_image, cv2.COLOR_BGR2HSV) 

""" read in video capture """
def read_video(path):
  return cv2.VideoCapture(path)

""" writes image to ouput path with given filename """
def write_image(path, image):
  cv2.imwrite(path, image)

""" displays image for checking """
def show_image(image):
  cv2.imshow('image',image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

""" subtract image 1 from image 2 """
def image_subtraction(image_1, image_2):
  return cv2.convertScaleAbs(np.subtract(np.float32(image_1), np.float32(image_2)))

""" given image, return keypoints, descriptors using SURF """
def get_features(image, sift):
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
  return sift.detectAndCompute(image, None)

""" find the corresponding features coordinates bewteen the two given images and add them to the given correspondence lists """
def add_feature_correspondences(keypoints_1, descriptors_1, keypoints_2, descriptors_2, correspondence_1, correspondence_2):

  index_pairs = flann_matcher(descriptors_1, descriptors_2) # index pairs of matching descriptors
  for index_1, index_2 in index_pairs:
    correspondence_1.append(keypoints_1[index_1].pt)
    correspondence_2.append(keypoints_2[index_2].pt)

""" returns a list of top k matched descriptor index pairs """
def flann_matcher(desc1, desc2, r_threshold = 0.20):
  'Finds strong corresponding features in the two given vectors.'
  ## Adapted from http://stackoverflow.com/a/8311498/72470

  ## Build a kd-tree from the second feature vector.
  FLANN_INDEX_KDTREE = 1  # bug: flann enums are missing
  flann = cv2.flann_Index(desc2, {'algorithm': FLANN_INDEX_KDTREE, 'trees': 4})

  ## For each feature in desc1, find the two closest ones in desc2.
  (idx2, dist) = flann.knnSearch(desc1, 2, params={}) # bug: need empty {}

  ## Create a mask that indicates if the first-found item is sufficiently
  ## closer than the second-found, to check if the match is robust.
  mask = dist[:,0] / dist[:,1] < r_threshold

  ## Only return robust feature pairs.
  idx1  = np.arange(len(desc1))
  pairs = np.int32(zip(idx1, idx2[:,0]))
  return pairs[mask] # apply r_threshold mask
  # pairs = [list(pair) for pair in zipped_pairs]
  # pairs.sort(key=lambda x: abs(dist[x[0]][0] - dist[x[1]][1]))  # sort by closest distances

def bf_matcher(desc1, desc2, k = 2):
  bf = cv2.BFMatcher(cv2.NORM_L2)
  matches = bf.knnMatch(desc1, desc2, k)
  # Apply ratio test
  good = []
  for m,n in matches:
    if m.distance < 0.75*n.distance:
      good.append((m.queryIdx, m.trainIdx))
  return good

""" determine size and x offset of stitched panorama """
def calculate_size(size_l, size_m, size_r, l2m_hgy, r2m_hgy, offset_manual=0):
  h_l, w_l = size_m[:2]
  h_m, w_m = size_m[:2]
  h_r, w_r = size_r[:2]

  # determine panoramic width attributed by left frame
  l_tlc = getMapping((0,0), l2m_hgy)          # top left corner in left frame
  l_blc = getMapping((0,h_l-1), l2m_hgy)      # bottom left corner in left frame
  mapped_w_l = -max(l_tlc[0], l_blc[0])       # the width due to left frame after mapping
  
  # determine panoramic width attributed by right frame
  r_trc = getMapping((w_r-1,0), r2m_hgy)      # top left corner in left frame
  r_brc = getMapping((w_r-1,h_r-1), r2m_hgy)  # bottom left corner in left frame
  mapped_w_r = min(r_trc[0], r_brc[0]) - w_m  # the width due to right frame after mapping 
  
  width = mapped_w_l + w_m + mapped_w_r + offset_manual
  height = h_m
  
  return (width, height), mapped_w_l + offset_manual

""" stitch the images together into a panorama """
def stitch_images(img_l, img_m, img_r, l2m_hgy, r2m_hgy, size, x_offset):
  h_m, w_m = img_m.shape[:2]
  panorama = cv2.warpPerspective(img_l, l2m_hgy, size)  # fill left frame
  cv2.warpPerspective(img_r, r2m_hgy, size, panorama, borderMode=cv2.BORDER_TRANSPARENT)  # fill right frame
  panorama[:,x_offset:x_offset+w_m] = img_m   # fill the panorama view with middle frame
  return panorama

""" returns the mapped coordinates given a point and the homography matrix """
def getMapping(xy, hg):
  vect = np.matrix([[xy[0]],[xy[1]],[1]])  # vector in homogenous coordinates
  mapping = np.array(hg * vect)
  mapping /= mapping[2][0]  # divide by w
  return mapping.astype(int).flatten()[:2]

""" return the average HSV given the image """
def get_average_HSV(image):
  image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # convert image to hsv colorspace
  avgH = image[0][0][0]
  avgS = image[0][0][1]
  avgV = image[0][0][2]
  count = 1.0
  for i in range(image.shape[0]):
    for j in range(image.shape[1]):
      hsv = image[i][j]
      avgH = count/(count+1) * avgH + hsv[0]/(count+1)
      avgS = count/(count+1) * avgS + hsv[1]/(count+1)
      avgV = count/(count+1) * avgV + hsv[2]/(count+1)
      count += 1
  return avgH, avgS, avgV

""" return the average HSV given the image """
def get_average_BGR(image):
  avgB = image[0][0][0]
  avgG = image[0][0][1]
  avgR = image[0][0][2]
  count = 1.0
  for i in range(image.shape[0]):
    for j in range(image.shape[1]):
      bgr = image[i][j]
      avgB = count/(count+1) * avgB + bgr[0]/(count+1)
      avgG = count/(count+1) * avgG + bgr[1]/(count+1)
      avgR = count/(count+1) * avgR + bgr[2]/(count+1)
      count += 1
  return avgB, avgG, avgR

""" scale an image with the given HSV scaling mask """
def scale_HSV(image, scale_mask):
  cv2.cvtColor(image, cv2.COLOR_BGR2HSV, image) # convert image to hsv colorspace
  image *= scale_mask
  cv2.cvtColor(image, cv2.COLOR_HSV2BGR, image) # convert back to bgr colorspace

""" extract background of a video """
def extract_background(video_path, output_path):
  cap = read_video(video_path)
  frame_count = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
  avg_img = np.float32(cap.read()[1])                         # initialize using first frame
  for count in range(1, frame_count):                         # iterate through all frames
    _, img = cap.read()                                       # read frame as img
    factor = 1.0/(count + 1)                                  # incremental average factor
    avg_img = np.add(count * factor * avg_img, factor * img)  # update average
  cap.release()
  background = cv2.convertScaleAbs(avg_img) # convert into uint8 image
  write_image(output_path, background)

""" dump a pickle file to the given path """
def pickle_dump(obj, path):
  with open(path, 'w') as f:
      cPickle.dump(obj, f)

""" load a pickle file from the given path """
def pickle_load(path):
  obj = None
  with open(path) as f:
    obj = cPickle.load(f)
  return obj
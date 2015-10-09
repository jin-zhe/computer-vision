import cv2.cv as cv
import numpy as np
import cPickle
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
def show_image(image):
  cv2.imshow('image',image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

""" given image, return keypoints, descriptors using SURF """
def get_features(image, sift):
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
  return sift.detectAndCompute(image, None)

""" find the corresponding features coordinates bewteen the two given images and add them to the given correspondence lists """
def add_feature_correspondences(keypoints_1, descriptors_1, keypoints_2, descriptors_2, correspondence_1, correspondence_2):

  index_pairs = match_descriptors(descriptors_1, descriptors_2) # index pairs of matching descriptors
  for index_1, index_2 in index_pairs:
    correspondence_1.append(keypoints_1[index_1].pt)
    correspondence_2.append(keypoints_2[index_2].pt)

""" returns a list of top k matched descriptor index pairs """
def match_descriptors(desc1, desc2, r_threshold = 0.06):
  'Finds strong corresponding features in the two given vectors.'
  ## Adapted from <http://stackoverflow.com/a/8311498/72470>.

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

""" determine size and offset of stitched panorama """
def calculate_size(size_m, size_r, l2m_hgy, r2m_hgy):
  h_m, w_m = size_m[:2]
  h_r, w_r = size_r[:2]
  width = w_m  + 4000
  height = h_m
  
  return (width, height)

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
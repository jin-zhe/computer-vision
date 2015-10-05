from helpers import *

# code adapted from http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html

""" given image, return keypoints, descriptors using SIFT """
def get_features(image, hessian_threshold=1000):
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
  orb = cv2.ORB()
  return orb.detectAndCompute(image, None)

""" find the corresponding features coordinates bewteen the two given images """
def get_feature_correspondences(keypoints_1, descriptors_1, keypoints_2, descriptors_2):
  # list of feature coordinates which matches each other via index position in the list
  correspondence_1 = []
  correspondence_2 = []
  index_pairs = match_descriptors(descriptors_1, descriptors_2) # index pairs of matching descriptors
  for index_1, index_2 in index_pairs:
    correspondence_1.append(keypoints_1[index_1].pt)
    correspondence_2.append(keypoints_2[index_2].pt)

  return np.array(correspondence_1), np.array(correspondence_2)

""" determine size and offset of stitched panorama """
def calculate_size(image_size_1, image_size_2, homography):
  offset = abs((homography*(image_size_2[0]-1,image_size_2[1]-1,1))[0:2,2]) 
  print offset
  size = (image_size_1[1] + int(offset[0]), image_size_1[0] + int(offset[1]))
  if (homography*(0,0,1))[0][2] > 0:
      offset[0] = 0
  if (homography*(0,0,1))[1][2] > 0:
      offset[1] = 0
  
  # update the homography to shift by the offset
  homography[0:2,2] +=  offset

  return size, offset

""" stitch the images together into a panorama """
def stitch_images(image_1, image_2, homography, size, offset, keypoints):
  height_1, width_1 = image_1.shape[:2]
  
  # fill the panorama view
  panorama = cv2.warpPerspective(image_2, homography, size)
  for row in range(height_1):
    for col in range(width_1):
      panorama[row+offset[1]][col + offset[0]] = image_1[row][col]
  return panorama

""" returns a list of top k matched descriptor index pairs """
def match_descriptors(descriptors_1, descriptors_2, k=50):
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)     # create BFMatcher object
  matches = bf.match(descriptors_1, descriptors_2)          # Match descriptors
  matches = sorted(matches, key = lambda x:x.distance)[:k]  # Sort them in the order of their distance and get top k
  return [(m.queryIdx, m.trainIdx) for m in matches]

""" Connects corresponding features in the two images """
def draw_correspondences(image_1, image_2, correspondence_1, correspondence_2, line_color=(0, 255, 255)):
  # juxtapose images 1 and 2 as image
  (height_1, width_1) = image_1.shape[:2]
  (height_2, width_2) = image_2.shape[:2]
  image = np.zeros((max(height_1, height_2), width_1 + width_2, 3), np.uint8)
  image[:height_1, :width_1] = image_1
  image[:height_2, width_1:width_1+width_2] = image_2
  
  # draw lines connecting corresponding features
  for (x1, y1), (x2, y2) in zip(np.int32(correspondence_1), np.int32(correspondence_2)):
    cv2.line(image, (x1, y1), (x2+width_1, y2), line_color, lineType=cv2.CV_AA)

  return image

""" main method """
if __name__ == "__main__":

  # load images
  image_1 = read_color_image("images/Image_1.jpg")
  image_2 = read_color_image("images/Image_2.jpg")

  # detect features and compute descriptors
  keypoints_1, descriptors_1 = get_features(image_1)
  keypoints_2, descriptors_2 = get_features(image_2)
  print len(keypoints_1), "features detected in image_1"
  print len(keypoints_2), "features detected in image_2"
  
  # find corresponding features.
  correspondence_1, correspondence_2 = get_feature_correspondences(keypoints_1, descriptors_1, keypoints_2, descriptors_2)
  print len(correspondence_1), "features matched"

  # visualise corresponding features.
  correspondences = draw_correspondences(image_1, image_2, correspondence_1, correspondence_2)
  write_image("images/correspondences.jpg", correspondences)
  
  # find homography between the views.
  homography, _ = cv2.findHomography(correspondence_2, correspondence_1)
  
  # calculate size and offset of merged panorama.
  size, offset = calculate_size(image_1.shape, image_2.shape, homography)
  print "output size: %ix%i" % size
  
  # finally combine images into a panorama
  panorama = stitch_images(image_1, image_2, homography, size, offset, (correspondence_1, correspondence_2))
  write_image("images/panorama.jpg", panorama)
from helpers import *

# code adapted from http://richardt.name/teaching/supervisions/vision-2011/practical/

""" given image, return keypoints, descriptors using SIFT """
def get_features(image, hessian_threshold=1000):
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
  orb = cv2.ORB()
  return orb.detectAndCompute(image, None)

""" returns a list of top k matched descriptor index pairs """
def match_descriptors(descriptors_1, descriptors_2, k=10):
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)     # create BFMatcher object
  matches = bf.match(descriptors_1, descriptors_2)          # Match descriptors
  matches = sorted(matches, key = lambda x:x.distance)[:k]  # Sort them in the order of their distance and get top k
  return [(m.queryIdx, m.trainIdx) for m in matches]

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
def calculate_size(size_l, size_m, size_r, l2m_hgy, r2m_hgy):
  h_l, w_l = size_l[:2]
  h_m, w_m = size_m[:2]
  h_r, w_r = size_r[:2]

  offset = abs((r2m_hgy*(h_r-1,w_r-1,1))[0:2,2]) # offset of the middle image relative to the top-left corner of the stitched panorama
  print offset
  size = (w_m + int(offset[0]), h_m + int(offset[1]))
  if (r2m_hgy*(0,0,1))[0][2] > 0:
      offset[0] = 0
  if (r2m_hgy*(0,0,1))[1][2] > 0:
      offset[1] = 0
  
  r2m_hgy[0:2,2] +=  offset # update the homography to shift by the offset

  return size, offset

""" stitch the images together into a panorama """
def stitch_images(img_l, img_m, img_r, l2m_hgy, r2m_hgy, size, offset):
  h_l, w_l = img_l.shape[:2]
  h_m, w_m = img_m.shape[:2]
  h_r, w_r = img_r.shape[:2]
  
  panorama = cv2.warpPerspective(img_r, r2m_hgy, size)
  # fill the panorama view with middle image
  for row in range(h_m):
    for col in range(w_m):
      panorama[row+offset[1]][col + offset[0]] = img_m[row][col]
  return panorama

""" Connects corresponding features in the two images """
def draw_correspondences(img_l, img_m, img_r, lm_fc_l, lm_fc_m, mr_fc_m, mr_fc_r, line_color=(0, 255, 255)):
  # juxtapose images 1 and 2 as image
  h_l, w_l = img_l.shape[:2]
  h_m, w_m = img_m.shape[:2]
  h_r, w_r = img_r.shape[:2]
  height = max(h_l, h_m, h_r)
  width = w_l + w_m + w_r
  image = np.zeros((height, width, 3), np.uint8)
  image[:h_l, :w_l] = img_l
  image[:h_m, w_l:w_l+w_m] = img_m
  image[:h_r, w_l+w_m:width] = img_r
  
  # draw lines connecting corresponding features
  # between left and mid
  for (x1, y1), (x2, y2) in zip(np.int32(lm_fc_l), np.int32(lm_fc_m)):
    cv2.line(image, (x1, y1), (x2+w_l, y2), line_color, lineType=cv2.CV_AA)
  # between mid and right
  for (x1, y1), (x2, y2) in zip(np.int32(mr_fc_m), np.int32(mr_fc_r)):
    cv2.line(image, (x1, y1), (x2+w_l+w_m, y2), line_color, lineType=cv2.CV_AA)

  return image

""" get the panoramic image given 3 overlapping images """
def get_panorama(img_l, img_m, img_r):
  # get keypoints and descriptors
  kpts_l, descs_l = get_features(img_l)
  kpts_m, descs_m = get_features(img_m)
  kpts_r, descs_r = get_features(img_r)
  print len(kpts_l), "features detected in left"
  print len(kpts_m), "features detected in middle"
  print len(kpts_r), "features detected in right"
  
  # find feature correspondences between left and mid
  lm_fc_l, lm_fc_m = get_feature_correspondences(kpts_l, descs_l, kpts_m, descs_m)
  print len(lm_fc_l), "features matched between left and mid"

  # find feature correspondences between mid and right
  mr_fc_m, mr_fc_r = get_feature_correspondences(kpts_m, descs_m, kpts_r, descs_r)
  print len(mr_fc_m), "features matched between left and mid"

  # visualise corresponding features.
  correspondences = draw_correspondences(img_l, img_m, img_r, lm_fc_l, lm_fc_m, mr_fc_m, mr_fc_r)
  write_image("images/correspondences.jpg", correspondences)
  
  # find homography between the views
  l2m_hgy, _ = cv2.findHomography(lm_fc_l, lm_fc_m, cv2.RANSAC, 5.0)  # src: left, dest: mid
  r2m_hgy, _ = cv2.findHomography(mr_fc_r, mr_fc_m, cv2.RANSAC, 5.0)  # dec: right, dest: mid

  # calculate size and offset of merged panorama.
  size, offset = calculate_size(img_l.shape, img_m.shape, img_r.shape, l2m_hgy, r2m_hgy)
  print "output size: %ix%i" % size
  
  # finally combine images into a panorama
  return stitch_images(img_l, img_m, img_r, l2m_hgy, r2m_hgy, size, offset)

""" main method """
if __name__ == "__main__":
  # load images
  image_left = read_color_image("images/football_left_5.jpg")
  image_mid = read_color_image("images/football_mid_5.jpg")
  image_right = read_color_image("images/football_right_5.jpg")
  panorama = get_panorama(image_left, image_mid, image_right)
  write_image("images/panorama.jpg", panorama)

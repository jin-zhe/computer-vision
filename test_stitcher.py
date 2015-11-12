from helpers import *

""" Connects corresponding features in the two images """
def draw_correspondences(img_l, img_m, img_r, lm_fc_l, lm_fc_m, mr_fc_m, mr_fc_r):
  # juxtapose all 3 images
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
    cv2.line(image, (x1, y1), (x2+w_l, y2), (255, 0, 0), lineType=cv2.CV_AA)
  # between mid and right
  for (x1, y1), (x2, y2) in zip(np.int32(mr_fc_m), np.int32(mr_fc_r)):
    cv2.line(image, (x1+w_l, y1), (x2+w_l+w_m, y2), (0, 0, 255), lineType=cv2.CV_AA)

  return image

""" get the panoramic view given 3 overlapping images """
def get_panorama(img_l, img_m, img_r):
  sift = cv2.SIFT()
  # get keypoints and descriptors
  kpts_l, descs_l = get_features(img_l, sift)
  kpts_m, descs_m = get_features(img_m, sift)
  kpts_r, descs_r = get_features(img_r, sift)
  print len(kpts_l), "features detected in left"
  print len(kpts_m), "features detected in middle"
  print len(kpts_r), "features detected in right"
  
  # feature correspondence lists
  lm_fc_l = []
  lm_fc_m = []
  mr_fc_m = []
  mr_fc_r = []

  # populate feature correspondences between left and mid
  add_feature_correspondences(kpts_l, descs_l, kpts_m, descs_m, lm_fc_l, lm_fc_m)
  print len(lm_fc_l), "features matched between left and mid"

  # populate feature correspondences between mid and right
  add_feature_correspondences(kpts_m, descs_m, kpts_r, descs_r, mr_fc_m, mr_fc_r)
  print len(mr_fc_m), "features matched between mid and right"

  # visualise corresponding features.
  correspondences = draw_correspondences(img_l, img_m, img_r, lm_fc_l, lm_fc_m, mr_fc_m, mr_fc_r)
  write_image("images/correspondences.jpg", correspondences)
  
  # find homography between the views
  # l2m_hgy, _ = cv2.findHomography(lm_fc_l, lm_fc_m, cv2.RANSAC, 5.0)  # src: left, dest: mid
  # r2m_hgy, _ = cv2.findHomography(mr_fc_r, mr_fc_m, cv2.RANSAC, 5.0)  # dec: right, dest: mid
  l2m_hgy, _ = cv2.findHomography(np.array(lm_fc_l), np.array(lm_fc_m))  # src: left, dest: mid
  r2m_hgy, _ = cv2.findHomography(np.array(mr_fc_r), np.array(mr_fc_m))  # dec: right, dest: mid

  # calculate size and offset of merged panorama.
  size, x_offset = calculate_size(img_l.shape, img_m.shape, img_r.shape, l2m_hgy, r2m_hgy)
  print "output size: %ix%i" % size
  
  # update the homographies with x-translations so left image flushes against the left
  translation_mat = np.mat([[1,0,x_offset],[0,1,0],[0,0,1]]) # translation matrix due to left offset
  l2m_hgy = translation_mat * l2m_hgy
  r2m_hgy = translation_mat * r2m_hgy

  # finally combine images into a panorama
  return stitch_images(img_l, img_m, img_r, l2m_hgy, r2m_hgy, size, x_offset)

""" main method """
if __name__ == "__main__":
  # load images
  img_l = read_color_image("processed/images/backgrounds/frames/football_left_background.jpg")
  img_m = read_color_image("processed/images/backgrounds/frames/football_mid_background.jpg")
  img_r = read_color_image("processed/images/backgrounds/frames/football_right_background.jpg")
  panorama = get_panorama(img_l, img_m, img_r)
  write_image("processed/images/panorama.jpg", panorama)

from helpers import *
import time

INPUT_DIR = './videos/raw/'
OUTPUT_DIR = "./processed/panorama/"

# predetermined values
PANORAMA_SIZE = (8391, 1080) 
X_OFFSET = 2815

# predetermined HSV scaling masks
HSV_SCALE_L = [1, 1.04985722408, 0.940493226638]  # for left frame
HSV_SCALE_R = [1, 1.09283200062, 0.888862209337]  # for right frame

""" get the panoramic image given 3 overlapping images """
def get_panorama(img_l, img_m, img_r, l2m_hgy, r2m_hgy):
  h_m, w_m = img_m.shape[:2]
  # fill left frame
  panorama = cv2.warpPerspective(img_l, l2m_hgy, PANORAMA_SIZE)
  # fill right frame
  cv2.warpPerspective(img_r, r2m_hgy, PANORAMA_SIZE, panorama, borderMode=cv2.BORDER_TRANSPARENT)
  # fill the panorama view with middle frame
  panorama[:,X_OFFSET+4:X_OFFSET+w_m] = img_m[:,4:]
  return panorama

""" gets the panoramic video given the three captures and the number of frames to process """
def write_panoramic_video(path, cap_l, cap_m, cap_r, l2m_hgy, r2m_hgy, frames):
  out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'XVID'), 24.0, PANORAMA_SIZE)
  for i in range(frames):
    # extract frames
    _, img_l = cap_l.read()
    _, img_m = cap_m.read()
    _, img_r = cap_r.read()
    # apply respective masks on left and right frames
    scale_HSV(img_l, HSV_SCALE_L)
    scale_HSV(img_r, HSV_SCALE_R)
    panorama_frame = get_panorama(img_l, img_m, img_r, l2m_hgy, r2m_hgy)
    out.write(panorama_frame)
  out.release()

""" main method """
if __name__ == "__main__":
  # predetermined correspondences
  lm_fc_l = [(1621.0,350.0),  (1530.0,698.0), (1709.0,499.0), (1525.0,660.0), (1676.0,245.0), (1889.0, 786.0),  (1755.0,1038.0),  (1625.0,480.0), (1793.0,560.0), (1827.0,438.0), (1826.0,785.0), (1752.0,573.0), (1648.0,546.0), (1688.0,273.0)]
  lm_fc_m = [(110.0,296.0),   (96.0, 653.0),  (227.0,425.0),  (80.0,618.0),   (139.0,186.0),  (448.0, 647.0),   (386.0,903.0),    (143.0,422.0),  (323.0,462.0),  (324.0,348.0),  (396.0,661.0),  (283.0,486.0),  (177.0,478.0),  (158.0,213.0)]
  mr_fc_m = [(1485.0,989.0), (1613.0,991.0), (1613.0,880.0),  (1911.0,667.0), (1676.0,409.0), (1587.0,146.0), (1601.0,36.0),  (1818.0,157.0), (1726.0,1045.0),  (1724.0,580.0), (1907.0,335.0)]
  mr_fc_r = [(52.0,1026.0),   (192.0,992.0), (173.0,880.0),   (429.0,622.0),  (186.0,399.0),  (60.0,133.0),   (57.0,21.0),    (289.0,149.0),  (309.0,1012.0),   (253.0,563.0),  (390.0,316.0)]

  # compute homography between the frames
  # l2m_hgy, _ = cv2.findHomography(lm_fc_l, lm_fc_m, cv2.RANSAC, 5.0)  # src: left, dest: mid
  # r2m_hgy, _ = cv2.findHomography(mr_fc_r, mr_fc_m, cv2.RANSAC, 5.0)  # dec: right, dest: mid
  l2m_hgy, _ = cv2.findHomography(np.array(lm_fc_l), np.array(lm_fc_m))  # src: left, dest: mid
  r2m_hgy, _ = cv2.findHomography(np.array(mr_fc_r), np.array(mr_fc_m))  # dec: right, dest: mid

  # update homographies with translation matrix due to left offset
  translation_mat = np.mat([[1,0,X_OFFSET],[0,1,0],[0,0,1]])
  l2m_hgy = translation_mat * l2m_hgy
  r2m_hgy = translation_mat * r2m_hgy

  # load captures
  cap_l = read_video(INPUT_DIR + "football_left.mp4")   # left capture
  cap_m = read_video(INPUT_DIR + "football_mid.mp4")    # mid capture
  cap_r = read_video(INPUT_DIR + "football_right.mp4")  # right capture
  
  # derive frame count to use (7200)
  fc_l = int(cap_l.get(cv.CV_CAP_PROP_FRAME_COUNT))
  fc_m = int(cap_m.get(cv.CV_CAP_PROP_FRAME_COUNT))
  fc_r = int(cap_r.get(cv.CV_CAP_PROP_FRAME_COUNT))
  frame_count = min(fc_l, fc_m, fc_r)

  # write output
  start_time = time.time()
  output_path = OUTPUT_DIR + 'panorama.avi'
  write_panoramic_video(output_path, cap_l, cap_m, cap_r, l2m_hgy, r2m_hgy, 48)
  print "Execution time(s): " + str(time.time() - start_time)
  
  # release captures
  cap_l.release()
  cap_m.release()
  cap_r.release()
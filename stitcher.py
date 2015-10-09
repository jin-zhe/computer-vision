from helpers import *

INPUT_DIR = './videos/raw/'
PROCESSED_DIR = "./processed/correspondences/"
OUTPUT_DIR = "./processed/panorama/"

""" get the panoramic image given 3 overlapping images """
def get_panorama(img_l, img_m, img_r, l2m_hgy, r2m_hgy, size):
  h_m, w_m = img_m.shape[:2]
  
  panorama = cv2.warpPerspective(img_l, l2m_hgy, size)
  cv2.warpPerspective(img_r, r2m_hgy, size, panorama, borderMode=cv2.BORDER_TRANSPARENT)
  # fill the panorama view with middle image
  for row in range(h_m):
    for col in range(w_m):
      panorama[row][col] = img_m[row][col]
  return panorama

""" gets the panoramic video given the three captures and the number of frames to process """
def write_panoramic_video(path, cap_l, cap_m, cap_r, l2m_hgy, r2m_hgy, frames, size):
  fourcc = cv.CV_FOURCC(*'XVID')
  out = cv2.VideoWriter(path,fourcc, 24.0, size)
  for frame in range(frames):
    _, img_l = cap_l.read()
    _, img_m = cap_m.read()
    _, img_r = cap_r.read()
    panorama = get_panorama(img_l, img_m, img_r, l2m_hgy, r2m_hgy, size)
    out.write(panorama)
  out.release()

""" main method """
if __name__ == "__main__":
  # load feature correspondeces
  lm_fc_l = pickle_load(PROCESSED_DIR + "lm_fc_l.pkl")
  lm_fc_m = pickle_load(PROCESSED_DIR + "lm_fc_m.pkl")
  mr_fc_m = pickle_load(PROCESSED_DIR + "mr_fc_m.pkl")
  mr_fc_r = pickle_load(PROCESSED_DIR + "mr_fc_r.pkl")

  # calculate homography between the frames
  # l2m_hgy, _ = cv2.findHomography(lm_fc_l, lm_fc_m, cv2.RANSAC, 5.0)  # src: left, dest: mid
  # r2m_hgy, _ = cv2.findHomography(mr_fc_r, mr_fc_m, cv2.RANSAC, 5.0)  # dec: right, dest: mid
  l2m_hgy, _ = cv2.findHomography(np.array(lm_fc_l), np.array(lm_fc_m))  # src: left, dest: mid
  r2m_hgy, _ = cv2.findHomography(np.array(mr_fc_r), np.array(mr_fc_m))  # dec: right, dest: mid
  
  # load captures
  cap_l = read_video(INPUT_DIR + "football_left.mp4")   # left capture
  cap_m = read_video(INPUT_DIR + "football_mid.mp4")    # mid capture
  cap_r = read_video(INPUT_DIR + "football_right.mp4")  # right capture
  
  # derive frame count to use
  fc_l = int(cap_l.get(cv.CV_CAP_PROP_FRAME_COUNT))
  fc_m = int(cap_m.get(cv.CV_CAP_PROP_FRAME_COUNT))
  fc_r = int(cap_r.get(cv.CV_CAP_PROP_FRAME_COUNT))
  frame_count = min(fc_l, fc_m, fc_r)

  # TODO: get size of panoramic output
  frame_width = int(cap_l.get(cv.CV_CAP_PROP_FRAME_WIDTH))
  frame_height = int(cap_l.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
  size = (frame_width * 3, frame_height)

  # write output
  write_panoramic_video(OUTPUT_DIR + 'panorama.avi', cap_l, cap_m, cap_r, l2m_hgy, r2m_hgy, 5*24, size)

  # release captures
  cap_l.release()
  cap_m.release()
  cap_r.release()
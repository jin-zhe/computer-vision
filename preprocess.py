""" outputs the extracted background of each clip """
from helpers import *

INPUT_DIR = './videos/raw/'
OUTPUT_DIR = './processed/correspondences/'

""" extracts the specific frame from video and writes it to disk """
def process_frame(frame_number=0):
  for video in os.listdir(INPUT_DIR):
    if video.endswith("mp4"):
      cap = read_video(INPUT_DIR + video)
      frame_image = extract_frame(cap, frame_number)
      cap.release()
      write_image(OUTPUT_DIR + video[:-4] + "_" + str(frame_number) + '.jpg', frame_image)

""" extracts specific frame from a capture """   
def extract_frame(cap, frame_number):
  for frame in range(frame_number):
    cap.read()
  return cap.read()[1]

""" process background images and write to disk """
def process_backgrounds():
  for video in os.listdir(INPUT_DIR):
    cap = read_video(INPUT_DIR + video)
    background_image = extract_background(cap)
    cap.release()
    write_image(OUTPUT_DIR + video[:-4] + '_background.jpg', background_image)

""" background extraction from capture """
def extract_background(cap):
  frame_count = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
  avg_img = np.float32(cap.read()[1]) # initialize using first frame
  for count in range(1, frame_count):
    _, img = cap.read()
    factor = 1.0/(count + 1)  # incremental average factor
    avg_img = np.add(count * factor * avg_img, factor * img) # update average
  return cv2.convertScaleAbs(avg_img)

""" preprocess routine """
def preprocess(target_corr = 4):
  sift = cv2.SIFT()
  
  # get captures
  cap_l = read_video(INPUT_DIR + "football_left.mp4")   # left capture
  cap_m = read_video(INPUT_DIR + "football_mid.mp4")    # mid capture
  cap_r = read_video(INPUT_DIR + "football_right.mp4")  # right capture
  
  # derive frame count to use
  fc_l = int(cap_l.get(cv.CV_CAP_PROP_FRAME_COUNT))
  fc_m = int(cap_m.get(cv.CV_CAP_PROP_FRAME_COUNT))
  fc_r = int(cap_r.get(cv.CV_CAP_PROP_FRAME_COUNT))
  frame_count = min(fc_l, fc_m, fc_r)
  print str(frame_count) + " frames"

  # feature correspondence lists
  lm_fc_l = []  # left frame coordinate feature correspondences between left and mid 
  lm_fc_m = []  # mid frame coordinate feature correspondences between left and mid 
  mr_fc_m = []  # mid frame coordinate feature correspondences between mid and right
  mr_fc_r = []  # right frame coordinate feature correspondences between mid and right
  
  # loop through frames
  for frame in range(0, frame_count):
    # skip every 10s
    if frame % (24*10) != 0:
      continue
    _, img_l = cap_l.read()
    _, img_m = cap_m.read()
    _, img_r = cap_r.read()
    
    # get keypoints and descriptors
    kpts_l, descs_l = get_features(img_l, sift)
    kpts_m, descs_m = get_features(img_m, sift)
    kpts_r, descs_r = get_features(img_r, sift)

    # populate feature correspondences for each frame pairs
    add_feature_correspondences(kpts_l, descs_l, kpts_m, descs_m, lm_fc_l, lm_fc_m)
    add_feature_correspondences(kpts_m, descs_m, kpts_r, descs_r, mr_fc_m, mr_fc_r)

    print len(lm_fc_l), len(mr_fc_m)

  cap_l.release()
  cap_m.release()
  cap_r.release()

  # write correspondences
  pickle_dump(lm_fc_l, OUTPUT_DIR + "lm_fc_l.pkl")
  pickle_dump(lm_fc_m, OUTPUT_DIR + "lm_fc_m.pkl")
  pickle_dump(mr_fc_m, OUTPUT_DIR + "mr_fc_m.pkl")
  pickle_dump(mr_fc_r, OUTPUT_DIR + "mr_fc_r.pkl")

def manual_correspondence():
  lm_fc_l = [(1621.0,350.0),  (1530.0,698.0), (1709.0,499.0), (1525.0,660.0), (1676.0,245.0), (1889.0, 786.0),  (1755.0,1038.0),  (1625.0,480.0), (1793.0,560.0), (1827.0,438.0), (1826.0,785.0), (1752.0,573.0), (1648.0,546.0), (1688.0,273.0)]
  lm_fc_m = [(110.0,296.0),   (96.0, 653.0),  (227.0,425.0),  (80.0,618.0),   (139.0,186.0),  (448.0, 647.0),   (386.0,903.0),    (143.0,422.0),  (323.0,462.0),  (324.0,348.0),  (396.0,661.0),  (283.0,486.0),  (177.0,478.0),  (158.0,213.0)]
  mr_fc_m = [(1485.0,989.0), (1613.0,991.0), (1613.0,880.0),  (1911.0,667.0), (1676.0,409.0), (1587.0,146.0), (1601.0,36.0),  (1818.0,157.0), (1726.0,1045.0),  (1724.0,580.0), (1907.0,335.0)]
  mr_fc_r = [(52.0,1026.0),   (192.0,992.0), (173.0,880.0),   (429.0,622.0),  (186.0,399.0),  (60.0,133.0),   (57.0,21.0),    (289.0,149.0),  (309.0,1012.0),   (253.0,563.0),  (390.0,316.0)]

  pickle_dump(lm_fc_l, OUTPUT_DIR + "lm_fc_l.pkl")
  pickle_dump(lm_fc_m, OUTPUT_DIR + "lm_fc_m.pkl")
  pickle_dump(mr_fc_m, OUTPUT_DIR + "mr_fc_m.pkl")
  pickle_dump(mr_fc_r, OUTPUT_DIR + "mr_fc_r.pkl")

""" main method """
if __name__ == "__main__":
  # process_backgrounds()
  # process_frame((1*60+6)*24 + 10)
  # preprocess()
  # manual_correspondence()
  fourcc = cv.CV_FOURCC(*'XVID')
  path = "./processed/panorama/test.avi"
  out = cv2.VideoWriter(path, fourcc, 24.0, (8391, 1080))
  frame = read_color_image("./processed/panorama.jpg")
  for i in range(100):
    out.write(frame)
  out.release()
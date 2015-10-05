""" outputs the extracted background of each clip """
from helpers import *

INPUT_DIR = 'videos/raw/'
OUTPUT_DIR = 'images/'

""" background extraction from capture """
def extract_background(path):
  cap = read_video(path)
  frame_count = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
  avg_img = np.float32(cap.read()[1]) # initialize using first frame
  for count in range(1, frame_count):
    _, img = cap.read()
    factor = 1.0/(count + 1)  # incremental average factor
    avg_img = np.add(count * factor * avg_img, factor * img) # update average
  cap.release()
  return cv2.convertScaleAbs(avg_img)

""" main method """
if __name__ == "__main__":
  for video in os.listdir(INPUT_DIR):
    background_image = extract_background(INPUT_DIR + video)
    write_image(OUTPUT_DIR + video[:-4] + '_background.jpg', background_image)
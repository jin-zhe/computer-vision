""" outputs the extracted background of each clip """
from helpers import *

INPUT_DIR = 'videos/raw/'
OUTPUT_DIR = 'images/'

""" extracts the specific frame from video and writes it to disk """
def process_frame(frame_number=0):
  for video in os.listdir(INPUT_DIR):
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

""" main method """
if __name__ == "__main__":
  # process_backgrounds()
  process_frame(5)
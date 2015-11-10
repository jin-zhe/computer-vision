from helpers import *
THRESHOLD = 5
BACKGROUND = read_color_image("images/topdown_bg.png")

cap = read_video("processed/panorama/topdown.avi")
out = cv2.VideoWriter("processed/topdown_bg_removed.avi", cv.CV_FOURCC(*'MPEG'), 24.0, (int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))))
frame_count = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
for i in range(frame_count):
  ret,frame = cap.read()
  out.write(image_subtraction(frame, BACKGROUND))
cap.release()
out.release()
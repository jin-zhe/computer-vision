from helpers import *
# extract_background("processed/panorama/topdown.avi", "images/topdown_bg.png")
BACKGROUND = read_color_image("images/topdown_bg.png")
def read_first_frame():
  cap = read_video("processed/panorama/topdown.avi")
  _, img = cap.read()
  cap.release()
  return img

frame = read_first_frame()
frame = image_subtraction(frame, BACKGROUND)
gray = get_grayscale(frame)
ret,thresh5 = cv2.threshold(gray,5,255,cv2.THRESH_BINARY)
ret,thresh25 = cv2.threshold(gray,25,255,cv2.THRESH_BINARY)
img = thresh5 - cv2.dilate(thresh25,np.ones((3,3),np.uint8),iterations = 1)
# img = cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))  # erosion followed by dilation
img = cv2.medianBlur(img,5)
img = cv2.medianBlur(img,5)
# img = cv2.medianBlur(img,5)
# median = cv2.dilate(median,np.ones((3,3),np.uint8),iterations = 1) # dilation
# surf = cv2.SURF(50000)
# kp, des = surf.detectAndCompute(median,None)
# sift = cv2.SIFT()
# kp, des = sift.detectAndCompute(median,None)
# img = cv2.drawKeypoints(median,kp,None,(0,0,255),2)
write_image("images/out.png", img)
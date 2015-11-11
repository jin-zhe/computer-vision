from helpers import *

OUTPUT_PATH = "./processed/"

""" preprocess player information """
def preprocess_players(first_frame):
  # hardcoded information
  win_lt, hist_lt = get_trackable(first_frame, (0,706),(35,696), (8,704),(10,700))
  win_lb, hist_lb = get_trackable(first_frame, (879,1206),(910,1152), (893,1178),(896,1168))
  win_ref, hist_ref = get_trackable(first_frame, (321,998),(412,959), (331,991),(339,990))
  win_rk, hist_rk = get_trackable(first_frame, (352,349),(455,319), (382,320),(391,325))
  win_bk, hist_bk = get_trackable(first_frame, (365,1400),(441,1327), (414,1361),(416,1358))
  win_r1, hist_r1 = get_trackable(first_frame, (310,755), (414,743), (365,751), (374,747))
  win_r2, hist_r2 = get_trackable(first_frame, (50,863),(200,838), (97,853),(164,842))
  win_r3, hist_r3 = get_trackable(first_frame, (590,893),(670,861), (638,877),(654,870))
  win_r4, hist_r4 = get_trackable(first_frame, (329,966),(428,924), (350,957),(385,944))
  win_r5, hist_r5 = get_trackable(first_frame, (190,967),(301,932), (257,949),(254,951))
  win_r6, hist_r6 = get_trackable(first_frame, (228,1086),(341,1026), (239,1082),(287,1057))
  win_r7, hist_r7 = get_trackable(first_frame, (97,1183),(205,1126), (110,1173),(152,1153))
  win_r8, hist_r8 = get_trackable(first_frame, (536,1183),(599,1129), (539,1182),(568,1159))
  win_b1, hist_b1 = get_trackable(first_frame, (377,779),(464,761), (417,773),(402,774))
  win_b2, hist_b2 = get_trackable(first_frame, (477,900),(556,869), (503,891),(545,874))
  win_b3, hist_b3 = get_trackable(first_frame, (161,1062),(269,1016), (175,1055),(195,1047))
  win_b4, hist_b4 = get_trackable(first_frame, (281,1067),(368,1025), (315,1052),(325,1047))
  win_b5, hist_b5 = get_trackable(first_frame, (240,1122),(343,1066), (300,1092),(283,1100))
  win_b6, hist_b6 = get_trackable(first_frame, (305,1113),(392,1064), (339,1096),(354,1087))
  win_b7, hist_b7 = get_trackable(first_frame, (177,1180),(287,1120), (223,1156),(212,1160))
  win_b8, hist_b8 = get_trackable(first_frame, (289,1191),(384,1130), (336,1162),(343,1159))
  win_b9, hist_b9 = get_trackable(first_frame, (354,1201),(454,1131), (365,1195), (398,1173))
  win_b10, hist_b10 = get_trackable(first_frame, (480,1215),(558,1152), (518,1185),(509,1193))

  players = {
   "linesman_top": {"window": win_lt, "histogram": hist_lt, "positions":[]}, "linesman_bottom": {"window": win_lb, "histogram": hist_lb, "positions":[]}, "referee": {"window": win_ref, "histogram": hist_ref, "positions":[]}, "red_keeper": {"window": win_rk, "histogram": hist_rk, "positions":[]}, "blue_keeper": {"window": win_bk, "histogram": hist_bk, "positions":[]},
   "red_1": {"window": win_r1, "histogram": hist_r1, "positions":[]}, "red_2": {"window": win_r2, "histogram": hist_r2, "positions":[]}, "red_3": {"window": win_r3, "histogram": hist_r3, "positions":[]}, "red_4": {"window": win_r4, "histogram": hist_r4, "positions":[]}, "red_5": {"window": win_r5, "histogram": hist_r5, "positions":[]}, "red_6": {"window": win_r6, "histogram": hist_r6, "positions":[]}, "red_7": {"window": win_r7, "histogram": hist_r7, "positions":[]}, "red_8": {"window": win_r8, "histogram": hist_r8, "positions":[]},
   "blue_1": {"window": win_b1, "histogram": hist_b1, "positions":[]},"blue_2": {"window": win_b2, "histogram": hist_b2, "positions":[]},"blue_3": {"window": win_b3, "histogram": hist_b3, "positions":[]},"blue_4": {"window": win_b4, "histogram": hist_b4, "positions":[]},"blue_5": {"window": win_b5, "histogram": hist_b5, "positions":[]},"blue_6": {"window": win_b6, "histogram": hist_b6, "positions":[]},"blue_7": {"window": win_b7, "histogram": hist_b7, "positions":[]},"blue_8": {"window": win_b8, "histogram": hist_b8, "positions":[]},"blue_9": {"window": win_b9, "histogram": hist_b9, "positions":[]},"blue_10": {"window": win_b10, "histogram": hist_b10, "positions":[]}
  }

  return players

""" returns the hsv range from two points """
def get_hsv_range(frame, pt1, pt2):
  hsv_1 = frame[pt1[0]][pt1[1]]
  hsv_2 = frame[pt2[0]][pt2[1]]
  min_h = float(min(hsv_1[0],hsv_2[0]));
  min_s = float(min(hsv_1[1],hsv_2[1]));
  min_v = float(min(hsv_1[2],hsv_2[2]));
  max_h = float(max(hsv_1[0],hsv_2[0]));
  max_s = float(max(hsv_1[1],hsv_2[1]));
  max_v = float(max(hsv_1[2],hsv_2[2]));
  return np.array((min_h,min_s,min_v)), np.array((max_h,max_s,max_v))

""" returns the track window and region of interest histogram for mean shift """
def get_trackable(frame, top_right, bottom_left, pt1, pt2):
  c,r,w,h = get_window(top_right, bottom_left) # initial location of window
  roi = frame[r:r+h, c:c+w]  # region of image
  hsv_min, hsv_max = get_hsv_range(frame, pt1, pt2)
  mask = cv2.inRange(roi, hsv_min, hsv_max)     # mask = (within range)? 255: 0
  roi_hist = cv2.calcHist([roi],[0],mask,[360],[0,360]) # histogram of hue values
  cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
  track_window = (c,r,w,h)
  return track_window, roi_hist

""" augment frame with shapes """
def draw_shapes(frame, track_window):
  position = get_position(track_window)
  cv2.circle(frame, position, 5, (0,0,255))
  x,y,w,h = track_window
  cv2.rectangle(frame, (x,y), (x+w,y+h), 255,1)

""" returns (column,row,width,height) given top right and bottom left corners """
def get_window(top_right, bottom_left):
  row = top_right[0]
  height = bottom_left[0] - row
  column = bottom_left[1]
  width = top_right[1] - column
  return column,row,width,height

""" get player's position on the ground given its tracking window """
def get_position(window):
  c,r,w,h = window
  isLeft = (c + w/2) <= 706
  if isLeft:
    return (c+w,r+h) # take bottom right corner of window
  else:
    return (c,r+h)   # take bottom left corner of windor

""" main procedure """
def main(input_path):
  cap = cv2.VideoCapture(input_path)
  out = cv2.VideoWriter(OUTPUT_PATH + "videos/augmented.avi", cv.CV_FOURCC(*'MPEG'), 24.0, (int(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)), int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))))
  frame_count = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
  first_frame = BGR_to_HSV(cap.read()[1]) # first frame of the video in HSV
  
  players = preprocess_players(first_frame) # player information

  # process first frame using hardcoded windows
  first_frame = HSV_to_BGR(first_frame)
  for _, player in players.items():
    track_window = player["window"]
    player["positions"].append(get_position(track_window))
    draw_shapes(first_frame, track_window)
  out.write(first_frame)

  # process remaining frames using mean shift
  # Setup the termination criteria, either 10 iteration or move by at least 1 px
  term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
  for i in range(frame_count-1):
    ret,frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    for p in players:
      player = players[p]
      hist = player["histogram"]
      track_window = player["window"]
      dst = cv2.calcBackProject([hsv],[0],hist,[0,360],1)
      # apply meanshift to get the new location
      ret, track_window = cv2.meanShift(dst, track_window, term_crit)
      position = get_position(track_window)

      # update actions
      player["window"] = track_window
      player["positions"].append(position)
      
      # draw shapes on frame
      draw_shapes(frame, track_window)
    
    out.write(frame)

  cv2.destroyAllWindows()
  cap.release()
  out.release()

  pickle_dump(players, OUTPUT_PATH + "players/players.pkl") 

if __name__ == "__main__":
  start_time = time.time()
  main('processed/videos/topdown/topdown.avi')
  print "Execution time(s): " + str(time.time() - start_time)
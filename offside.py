from helpers import *

MINIMAP_PATH = "./processed/images/field_color.png"
PLAYERS_PATH = "./processed/players/players.pkl"
OUTPUT_PATH = "./processed/"

def mark_offside(frame, position, color):
  cv2.line(frame, (position, 0), (position, int(frameHeight)), color)

def mark_player(frame, position, tag, color):
  cv2.circle(frame, position, 12, (0,255,255), -1) # yellow outline
  cv2.circle(frame, position, 10, color, -1)
  cv2.putText(frame, tag, (position[0]+12,position[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,255), 2)

if __name__ == "__main__":
  # minimap = read_color_image(MINIMAP_PATH)
  players = pickle_load(PLAYERS_PATH)
  # height, width, dim = minimap.shape
  # for each frame

  #superimpose on topdown video
  incomingVideoFeed = cv2.VideoCapture("topdown.avi")

  frameWidth = int(incomingVideoFeed.get(cv.CV_CAP_PROP_FRAME_WIDTH))
  frameHeight = int(incomingVideoFeed.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
  fps = int(incomingVideoFeed.get(cv.CV_CAP_PROP_FPS))
  frameCount = int(incomingVideoFeed.get(cv.CV_CAP_PROP_FRAME_COUNT))


  out = cv2.VideoWriter(OUTPUT_PATH + "videos/offside.avi", cv.CV_FOURCC(*'MPEG'), 24.0, (int(frameWidth), int(frameHeight)))


  for currentFrameIndex in xrange(frameCount):
    _, frame = incomingVideoFeed.read()
    blue_offside = int(width)
    blue_offside_check = int(width)
    red_offside = 0
    red_offside_check = 0
    # for each player
    for p in players:
      player = players[p]
      position = player["positions"][currentFrameIndex]

      # if linesman
      if p.startswith("linesman"):
        # if top linesman
        if p.endswith("top"):
            player_colour = (0, 0, 0)
        # if bottom linesman
        else:
            player_colour = (85,185,164)
      # if referee
      elif p == "referee":
        player_colour = (102,234,206)
      # if red team
      elif p.startswith("red"):
        # if keeper
        if p.endswith("keeper"):
            player_colour = (212,231,235)

        # if player
        else:
            player_colour = (0,0,255)
            if position[0] > red_offside:
                red_offside = position[0]
            if position[0] < blue_offside_check:
                blue_offside_check = position[0]

      # if blue team
      else:
        # if keeper
        if p.endswith("keeper"):
            player_colour = (56,104,85)
        # if player
        else:
            player_colour = (255,0,0)
            if position[0] < blue_offside:
                blue_offside = position[0]
            if position[0] > red_offside_check:
                red_offside_check = position[0]
				
      # mark_player(frame, position, p, player_colour)
    if blue_offside > blue_offside_check:  
        mark_offside(frame, blue_offside, (255,0,0))
    else:
        mark_offside(frame, blue_offside, (0,0,0))
    if red_offside < red_offside_check:  
        mark_offside(frame, red_offside, (0,0,255))
    else:
        mark_offside(frame, red_offside, (0,0,0))
    out.write(frame)
  out.release()

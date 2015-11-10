from helpers import *

MINIMAP_PATH = "./processed/images/field_color.png"
PLAYERS_PATH = "./processed/players/players.pkl"

if __name__ == "__main__":
  minimap = read_color_image(MINIMAP_PATH)
  players = pickle_load(PLAYERS_PATH)
  # for each frame
  # Note: each players has 7199 positions, one for each frame). 1 frame short due to mean_shift implementation but it's okay
  for i in range(7199):
    # for each player
    for p in players:
      player = players[p]
      position = player["position"][i]
      
      # if linesman
      if p == "linesman":
        # do something
      
      # if referee
      elif p == "referee":
        # do something
      
      # if red team
      elif p.startswith("red"):
        # if keeper
        if p.endswith("keeper"):
          # do something
        # if player
        else:
          # do something

      # if blue team
      else:
        # if keeper
        if p.endswith("keeper"):
          # do something
        # if player
        else:
          # do something
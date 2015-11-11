from helpers import *

PLAYERS_PATH = "./processed/players/players.pkl"

if __name__ == "__main__":
  players = pickle_load(PLAYERS_PATH)
  
  # TODO declare pyplots for all players on the field, i.e. each player have their own pyplot

  # plot for each player
  for p in players:
    player = players[p]
    positions = player["positions"]
    # TODO: plot using player positions

  # TODO show pyplot and distance
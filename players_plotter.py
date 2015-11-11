from helpers import *

MINIMAP_PATH = "./processed/images/field_color.png"
PLAYERS_PATH = "./processed/players/players.pkl"

SKIP = 1
SKIP_LENGTH = 24
FIELD_WIDTH=73
FIELD_HEIGHT=110
minimap = read_color_image(MINIMAP_PATH)
height, width, dim = minimap.shape

def calculate_distance(oldPos, newPos):
  dist = math.hypot((oldPos[0] - newPos[0])/width*FIELD_WIDTH, (oldPos[1] - newPos[1])/height*FIELD_HEIGHT)
  return dist

if __name__ == "__main__":
	players = pickle_load(PLAYERS_PATH)

	# TODO declare pyplots for all players on the field, i.e. each player have their own pyplot

	# plot for each player
	for p in players:
		player = players[p]
		positions = player["positions"]
		distance = 0
		oldPos = (0, 0)
		current_skip = 0
		# TODO: plot using player positions
		for pos in positions:
			if SKIP:
				if current_skip != SKIP_LENGTH:
					current_skip = current_skip + 1
					continue
				else:
					current_skip = 0
					
			if oldPos == (0, 0):
				oldPos = pos
				
			else:
				distance += calculate_distance(oldPos, pos)
				
		x,y = zip(*positions)
		plt.figure()
		plt.title(p)
		plt.imshow(minimap)
		plt.axis('off')
		plt.hold(True)
		plt.scatter(x, y, marker='s', color='red', alpha=0.5)
		plt.show()
				
		print p, distance/1000, "km"
		# TODO show pyplot and distance
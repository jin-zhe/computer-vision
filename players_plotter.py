from helpers import *

MINIMAP_PATH = "./processed/images/field_color.png"
PLAYERS_PATH = "./processed/players/players.pkl"
OUTPUT_PATH = "./processed/images/plots/"

SKIP_LENGTH = 24	# number of frames to skip for reading of positions
PIXEL_TO_M = 120./1330.
PIXEL_ADJUSTMENT = 10

""" returns the euclidean distance between 2 points """
def get_distance(pt1, pt2):
  return math.hypot(pt1[0] - pt2[0], pt1[1] - pt2[1])

if __name__ == "__main__":
	players = pickle_load(PLAYERS_PATH)
	minimap = read_color_image(MINIMAP_PATH)
	# plot for each player
	for p in players:
		player = players[p]
		positions = player["positions"]
		
		# accumulate player distance
		total_distance = 0
		old_pos = positions[0]
		for pos in positions[::SKIP_LENGTH]:
			curr_pos = pos
			total_distance += get_distance(old_pos, pos)
			old_pos = curr_pos
		
		total_distance *= PIXEL_TO_M # scale total distance to metric units

		# get plot and writes to disk
		x,y = zip(*positions[::SKIP_LENGTH])
		title = "Player " + p + "\nTotal distance ran: " + "%.2f" % total_distance + " m"
		plt.clf()
		plt.title(title, fontsize=18, fontweight='bold')
		plt.imshow(minimap)
		plt.axis('off')
		plt.plot(x, y, marker='s', color='red', alpha=0.5)
		plt.savefig(OUTPUT_PATH + p + ".png")
		print p, "%.2f" % total_distance, "m"
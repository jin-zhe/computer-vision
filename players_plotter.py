from helpers import *

MINIMAP_PATH = "./processed/images/field_color.png"
PLAYERS_PATH = "./processed/players/players.pkl"
OUTPUT_PATH = "./processed/"


def drawWindow(x, y, colour):
    for i in range(x - 7, x + 7):
        if i >= 0 and i < width:
            for j in range(y - 7, y + 7):
                if j >= 0 and j < height:
                    image[j, i] = colour
                    ##image[y-1,x-1] = image[y, x-1] = image[y+1,x-1] = image[y-1,x] = image[y+1,x]
                    ##  = image[y-1,x+1] = image[y,x+1] = image[y+1,x+1] = colour


if __name__ == "__main__":
    minimap = read_color_image(MINIMAP_PATH)
    players = pickle_load(PLAYERS_PATH)
    height, width, dim = minimap.shape
    out = cv2.VideoWriter(OUTPUT_PATH + "videos/minimap.avi", cv.CV_FOURCC(*'MPEG'), 24.0, (int(width), int(height)))
    # for each frame
    # Note: each players has 7199 positions, one for each frame). 1 frame short due to mean_shift implementation but it's okay
    for i in range(7199):
        image = read_color_image(MINIMAP_PATH)
        # for each player
        for p in players:
            player = players[p]
            position = player["positions"][i]

            # if linesman
            if p == "linesman":
                player_colour = [0, 0, 0]
            # if referee
            elif p == "referee":
                player_colour = [0, 51, 0]
            # if red team
            elif p.startswith("red"):
                # if keeper
                if p.endswith("keeper"):
                    player_colour = [127, 0, 255]

                # if player
                else:
                    player_colour = [0, 0, 255]

            # if blue team
            else:
                # if keeper
                if p.endswith("keeper"):
                    player_colour = [255, 128, 0]
                # if player
                else:
                    player_colour = [255, 0, 0]
            drawWindow(position[0], position[1], player_colour)
        out.write(image)
    out.release()

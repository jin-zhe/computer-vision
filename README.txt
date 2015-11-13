################################################################################
                                CS4243 Project
################################################################################
Group 1:
• JIN ZHE
• LAW TAO RUI JERROLD
• AMITKUMAR GAMANE
• ZHANG YANQING

#####################
        Notes
#####################
• Every python script in this repository are run without arguments
• Videos in the repository are not included in this zipped file but are found
  in the one for results. Some videos are used as inputs for codes. Hence when
  running them, please ensure that the videos are placed in the correct
  directory paths as indicated in the directoy structure section

#####################
        Code
#####################

helpers.py :
  • Provides necessary library imports, useful helper functions and also a
    generalized API for common OpenCV functions

stitcher.py :
  • Stitch the 3 camera footages from ./videos/raw/ using homographies derived
    from manual features correspondences. As each stitched panoramic frame is
    derived, apply another homography using manual features correspondences to
    also derive the topdown view.
  • Outputs panoramic video at ./processed/videos/panorama/panorama.avi
  • Outputs topdown video at ./processed/videos/topdown/topdown.avi

mean_shift.py :
  • Uses mean shift method on topdown video to track the positions of players at
    every frame
  • Outputs player positions at ./processed/players.pkl
  • Outputs topdown video augmented with player tracking windows and their
    ground poistion markers at ./processed/videos/augmented.avi

minimap_generator.py :
  • Using player positional values from ./processed/players.pkl, generates a
    topdown video of players represented as moving pins 
  • Outputs topdown graphic video at ./processed/videos/minimap.avi

offside.py :
  • Using player positional values from ./processed/players.pkl, mark the
    offside players in the topdown video
  • Outputs topdown video that draws the vertical lines for offside players at
    ./processed/videos/offside.avi

players_plotter.py :
  • Using player positional values from ./processed/players.pkl, generate a plot
    for each player based on their field positions at 24 frame intervals
  • Outputs player movement plots into folder ./processed/images/plots/  

topdown_bg_subtraction.py :
  • Subtracts topdown video from its background
  • Outputs "/processed/videos/topdown/topdown_bg_removed.avi"

#####################
     Unused code
#####################

preprocess.py :
  • Processed background frames for each camera at ./videos/raw/ and also
    collect feature correspondences between frames using SIFT/SURF techniques
  • Outputs extracted background frames at ./processed/images/backgrounds/frames/
  • Outputs feature correspondences between frames at ./processed/correspondences/

test_stitcher.py :
  • conducts feature extraction, correspondence and use their consequent
  homographies to warp and stitch 3 images together to form a larger panoramic
  scene

threshold_test.py :
  • performs binary thresholding for the first frame of the topdown video with
  differing threshold values in order to isolate players' "x-shaped" shadows
  • Options to further perform feature detection on resulting image included
  • Outputs to ./processed/images/threshold_results/

#####################
 Directory structure
#####################

./
├── processed/
│   ├── images/
│   │   ├── backgrounds/
│   │   │   ├── frames/
│   │   │   │   ├── football_left_background.jpg      # background image of left camera footage (outputs from preprocess.py)
│   │   │   │   ├── football_mid_background.jpg       # background image of middle camera footage (outputs from preprocess.py)
│   │   │   │   ├── football_right_background.jpg     # background image of right camera footage (outputs from preprocess.py)
│   │   │   ├── panorama.jpg                        # background image of panorama scene video
│   │   │   ├── topdown_bg.png                      # background image of topdown video
│   │   ├── plots/                                # positional plots for every player on the field (outputs from player_plotter.py)
│   │   │   ├── ...
│   │   ├── threshold_results/                    # results from thresholding experiments (outputs from threshold_test.py)
│   │   │   ├── ...
│   │   ├── correspondences.jpg                   # image indicating the feature correspondences used for panoramic stitching
│   │   ├── field_color.png                       # artificial image made for topdown view (field lines overlays exactly with topdown video)
│   │   ├── first.png                             # first frame of topdown video
│   │   ├── first_bg_removed.png                  # first frame of topdown video with background subtracted
│   ├── players/
│   │   ├── players.pkl                         # cpickle file containing player positions for every frame (output from means_shift.py)
│   ├── videos/
│   │   ├── panorama/
│   │   │   ├── panorama.avi                    # stitched panorama video (output from stitcher.py)
│   │   ├── topdown/
│   │   │   ├── topdown.avi                     # topdown video (output from stitcher.py)
│   │   │   ├── topdown_bg_removed.avi          # topdown video with background removed (output from topdown_bg_subtraction.py)
│   │   ├── augmented.avi                     # topdown video augmented with player tracking windows and ground positions (output from mean_shift.py)
│   │   ├── minimap.avi                       # topdown video of players represented as moving pins on field_color.png (output from minimap_generator.py)
│   │   ├── offside.avi                       # actual video graphical overlay of a line to show whether a player was offside (output from offside.py)
├── raw/
│   ├── football_left.mp4                   # original footage from left camera
│   ├── football_mid.mp4                    # original footage from middle camera
│   ├── football_right.mp4                  # original footage from right camera
├── helpers.py
├── mean_shift.py
├── minimap_generator.py
├── offside.py
├── players_plotter.py
├── preprocess.py
├── stitcher.py
├── test_stitcher.py
├── threshold_test.py
└── topdown_bg_subtraction.py
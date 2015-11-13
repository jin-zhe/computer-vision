# CS4243 Project (Group 1)

###Files included

* helpers.py :            provides a generalized API for common cv2 functions and also helps to import the needed packages  
* mean_shift.py :         TODO by JZ
* minimap_generator.py :  TODO
* offside.py:             TODO
* players_plotter.py:     TODO
* preprocess.py :         extract background frames for each video in `videos/raw/` and places them in `pictures/`. As this is a computationally expensive operation, the extracted backgrounds has been included in the repo.  
* stitcher.py:            TODO by JZ
* test_stitcher.py :      a stitcher that does feature extraction and correspondence to warp and stitch 3 images together to form a larger panoramic scene
* threshold_test.py:      TODO by JZ
* topdown_bg_subtraction.py : Subtracts topdown video from its background

Directory structure:
```
computer-vision/
  ├── processed/
  │   ├── images/
  │   │   ├── backgrounds/
  │   │   │   ├── frames/
  │   │   │   │   ├── football_left_background.jpg
  │   │   │   │   ├── football_mid_background.jpg
  │   │   │   │   ├── football_right_background.jpg
  │   │   │   ├── panorama.jpg
  │   │   │   ├── topdown_bg.png
  │   │   ├── plots/
  │   │   │   ├── ... # distance plots for every player on the field
  │   │   ├── threshold_results/
  │   │   │   ├── ... # results from thresholding experiments
  │   │   ├── correspondences.jpg
  │   │   ├── field_color.png
  │   │   ├── first.png
  │   │   ├── first_bg_removed.png
  │   ├── players/
  │   │   ├── players.pkl
  │   ├── videos/
  │   │   ├── panorama/
  │   │   │   ├── panorama.avi
  │   │   ├── topdown/
  │   │   │   ├── topdown.avi
  │   │   │   ├── topdown_bg_removed.avi
  │   │   ├── augmented.avi
  │   │   ├── minimap.avi
  │   │   ├── offside.avi
  ├── raw/
  │   ├── football_left.mp4
  │   ├── football_left.mp4
  │   ├── football_left.mp4
  ├── helpers.py
  ├── mean_shift.py
  ├── minimap_generator.py
  ├── offside.py
  ├── players_plotter.py
  ├── preprocess.py
  ├── stitcher.py
  ├── test_stitcher.py
  ├── threshold_test.py
  ├── topdown_bg_subtraction.py
```

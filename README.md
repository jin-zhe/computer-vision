# computer-vision

## Useful Resources
[pyimagesearch](http://www.pyimagesearch.com/2014/04/21/building-pokedex-python-finding-game-boy-screen-step-4-6/)  
[Practical exercises on OpenCV](http://richardt.name/teaching/supervisions/vision-2011/practical/)  
[Panorama Stitching](http://www1.inf.tu-dresden.de/~ds24/lehre/cv1_ws_2013/cv1ex3_ws_2013.pdf)

## Setting up
Please download the footages [here](https://download2.nus.edu.sg/index.php/s/ZZpYAtqvAR6Sjm7) and place `football_left.mp4`, `football_mid.mp4` and `football_right.mp4` into `videos/raw/`  

## Code functions
`helpers.py` : provides a generalized API for common cv2 functions and also helps to import the needed packages  
`process_frames.py` : extract background frames for each video in `videos/raw/` and places them in `pictures/`. As this is a computationally expensive operation, the extracted backgrounds has been included in the repo.  
`test_stitcher.py` : a stitcher that does feature extraction and correspondence to warp and stitch 2 images together to form a larger panoramic scene

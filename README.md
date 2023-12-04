# Picture Manipulation Tool

<div style="display: flex; justify-content: space-between;">
    <img src="https://github.com/clarencechau/picture-manipulation/blob/main/extras/dog.png?raw=true" width="200" height="200" />
    <img src="https://github.com/clarencechau/picture-manipulation/blob/main/extras/dognormal.png?raw=true" width="200" height="200" />
    <img src="https://github.com/clarencechau/picture-manipulation/blob/main/extras/doglosslevel.png?raw=true" width="200" height="200" />
    <img src="https://github.com/clarencechau/picture-manipulation/blob/main/extras/dogmirrored.png?raw=true" width="200" height="200" />

</div>

## Application Description

This was one of the first computer science projects I did at the University of Toronto when I was in first year. The point of this project was to recreate some of the basic features Photoshop provides, 
such as mirroring photos, changing saturation, and manipulating the loss level of the picture after the transformation has been done. Specific to this project, the application takes in a BMP file, and converts it into a 
QDT file. Then, an algorithm is run to configure and rearrange the RGBA values and pixel formations, finally returning a BMP file of the final transformation.

## Instructions

* Clone project locally
* Upload a BMP file into the root directory alongside the other BMP files
* At the bottom of a2main.py, in the main block of code, you may:
  * Change the file name to the picture you want to manipulate, original file is "toronto.bpm" for demonstration purposes
  * Change the loss level to an integer between 0 to 255, inclusive
* At the top of a2main.py, you may:
  * Change the boolean value of MIRROR_IMG, to choose if you want your image to be mirrored after the manipulation
* Run a2main.py
* After it has ran, there should be a new BMP.QDT file, and a BMP.QDT.BMP file.
  * The new BMP.QDT file is a QDT version of the original image
  * The new BMP.QDT.BMP file is the final result of the picture after the manipulation of the image chosen.

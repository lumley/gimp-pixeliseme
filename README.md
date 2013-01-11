# Gimp plugin - Pixelise me

This script will transform any selected region (or active layer) into a set of big pixels, depending on the specified pixel size. It does not calculate an average value between pixels, it only calculates the most common pixel inside the given pixel size, if no color is repeated, a random pixel will be picked up to fill the whole area (most probable, the upper left pixel).

The plugin has been created only for learning purposes, and has been tested in Gimp2.8.

## Requirements
This plugin requires the following:
 * [`The Gimp GNU Image Manipulation Program`][URI_TheGimp] The GIMP program (Available on Linux, Windows and Mac)
 * Python GIMP-extension (usually installed by default)

## Installation
Installation of this plugin goes like any other Python-fu plugin. Just download the file and move it to your GIMP plug-ins folder (by default, "%USERPROFILE%\\.gimp-2.8\plug-ins\" in Windows and "~/.gimp-2.8/plug-ins/" in Linux).

## Collaborate
Want to make your own plugins or improve this one? You can find some information on how to start on the next link:
 * [`Frederic Jaume - Python-Fu introduction`][URI_GimpTutorial1]


[URI_TheGimp]: http://www.gimp.org/
[URI_GimpTutorial1]: http://www.exp-media.com/content/extending-gimp-python-python-fu-plugins-part-1
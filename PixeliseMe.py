#!/usr/bin/env python

# =================== LICENSE =================
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#
# Sergio R. Lumley
# 2013/01/10
# lumley256@gmail.com
# =================== LICENSE =================

# ========= What does this Script do?? =========
# This script will transform any selected region (or active layer)
# into a set of big pixels, depending on the specified pixel size.
# It does not calculate an average value between pixels, it only
# calculates the most common pixel inside the given pixel size,
# if no color is repeated, a random pixel will be picked up to fill
# the whole area (most probable, the upper left pixel)

# This tells Python to load the Gimp module 
from gimpfu import *

def get_average_pixel_value(pDrawable, pOffsetX, pOffsetY, pRegionWidth, pRegionHeight):
    pixelValues = {}
    for pixel in range(pRegionWidth*pRegionHeight):    
        pixelValue = []
        result = gimp.pdb.gimp_drawable_get_pixel(pDrawable, pOffsetX, pOffsetY)
        for channel in range(result[0]):
            pixelValue.append(result[1][channel])
        pixelTuple = tuple(pixelValue)
        if pixelTuple in pixelValues:
            pixelValues[pixelTuple] = pixelValues[pixelTuple]+1
        else:
            pixelValues[pixelTuple] = 1

    mostRepeatedPixelTuple = (0, 0, 0, 0)
    mostRepeatedPixelValue = 0
    for mapValue in pixelValues.viewitems():
        if mapValue[1] > mostRepeatedPixelValue:
            mostRepeatedPixelValue = mapValue[1]
            mostRepeatedPixelTuple = mapValue[0]
    return mostRepeatedPixelTuple

# This is the function that will perform actual actions
def transform_to_pixels_size(pImage, pDrawable, pPixelWidth, pPixelHeight):
    # We group undoing so the history will show only one operation
    gimp.pdb.gimp_image_undo_group_start(pImage)
    gimp.pdb.gimp_progress_init("Pixelising, please wait", None)

    # Calculate image bounds (if there was a selection, then it will
    # be probably smaller than the current pDrawable size
    thereIsSelection, x1, y1, x2, y2 = gimp.pdb.gimp_drawable_mask_bounds(pDrawable)

    width = x2 - x1
    height = y2 - y1

    numColumns = width/pPixelWidth
    numRows = height/pPixelHeight

    # We will create a working layer to allow us to undo these changes,
    # this is because changing a pixel region does not add any entry
    # in the history tracking
    workingLayer = gimp.pdb.gimp_layer_new(pImage,
                                           pDrawable.width,
                                           pDrawable.height,
                                           RGBA_IMAGE,
                                           pDrawable.name,
                                           100,
                                           NORMAL_MODE)

    # Change working values and backup them to leave everything as it was
    currentForegroundColorBackup = gimp.pdb.gimp_context_get_foreground()
    for column in range(numColumns):
        for row in range (numRows):
            averageValue = get_average_pixel_value(pDrawable,
                                                   x1+column*pPixelWidth,
                                                   y1+row*pPixelHeight,
                                                   pPixelWidth,
                                                   pPixelHeight)
            averageValueString = ""
            for i in range(len(averageValue)):
                averageValueString += chr(averageValue[i])

            pixelRegion = workingLayer.get_pixel_rgn(x1+column*pPixelWidth,
                                                 y1+row*pPixelHeight,
                                                 pPixelWidth,
                                                 pPixelHeight)

            # It would be way faster to apply column by column and not
            # pixel by pixel... future improvement!
            for i in range(pPixelWidth):
                for j in range(pPixelHeight):
                    pixelRegion[x1+column*pPixelWidth+i,
                                y1+row*pPixelHeight+j] = averageValueString
            
            
        gimp.pdb.gimp_progress_update(column/float(numColumns))
            
                                                   
    #Now we finish grouping these changes
    gimp.pdb.gimp_context_set_foreground(currentForegroundColorBackup)
    gimp.pdb.gimp_image_insert_layer(pImage, workingLayer, None, -1)
    gimp.pdb.gimp_edit_clear(pDrawable) # We clear the whole drawable, or the selected region
    pDrawable = gimp.pdb.gimp_image_merge_down(pImage, workingLayer, EXPAND_AS_NECESSARY)
    
    pDrawable.update(x1, y1, width, height)
    pDrawable.flush()
    gimp.displays_flush()
    gimp.pdb.gimp_image_undo_group_end(pImage)
    
    return

# This is the plugin registration function
# I have written each of its parameters on a different line 
register(
    "transform_to_pixels_by_size", # Plugin's function name
    "Divide an image into tiles", # Plugin's documentation name
    "This script will divide the current image into a set of tiled. Each tile has one pixel margin and a black line that separates each tile.", # Plugin's description
    "Sergio R. Lumley", # Author of the plugin
    "You are free to use, distribute and sell this plugin under license GPLv3", # Copyright information
    "10 January 2013", # Date of plugin
    "<Image>/Filters/Conversion/Pixelise me", 
    "*", 
    [(PF_INT16, "tiles_x", "Width of pixel", 4, None),
     (PF_INT16, "tiles_y", "Height of pixel", 4, None),], 
    [],
    transform_to_pixels_size
    )

main()

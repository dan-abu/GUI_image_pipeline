# Image Pipeline
----------------------------------------------------------------

## Summary

This package will allow you to create a GUI for processing
images.

**GUI**
The GUI allows the user to provide inputs in a more
user-friendly way for those less comfortable using the
command line.

The GUI script can be found in `src/main.py`.

The inputs are `image_filename`, `cropped_image_width(pixels)`
and `cropped_image_height(pixels)`. Once provided, the user
will then be able to transform the image they provide.

Example images can be found in `assets`. Be aware that
`assets/tsp_scissors.png` is used as the application logo
when it opens.

**Image Processor**
The image processor executes the following transformations:
greyscale conversion, cropping source image into three images
based on the dimensions provided by the user and rotating the
image by 180 degrees.

Once complete, you will get pop-ups of the images and they will
be saved in `data/cropped_image_{image_count}.jpg`.

----------------------------------------------------------------

## Method

`src/main.py` uses the `Tkinter` library to create a GUI.
Once the necessary inputs are provided, the user can click the
`Click to crop image` button to crop the image and execute the
other transformations.

`src/img_processor.py` contains two classes: `Metadata` and
`Pipeline`.

`Metadata`, as you'd expect, contains all the metadata about
the image: its filename, width, height and other attributes.
It also contains the methods used for generating the
coordinates for cropping an image (the image-processing library, 
`Pillow`, requires them). You will find more details explaining
how the methods work within the script.

`Pipeline`'s key attributes are the images to be transformed
and the list of transformations to be applied before and after
images are cropped.

This class's methods contain the image transformations mentioned
above, as well as bundling an image and its data into an element
in `Pipeline.images`'s list.

----------------------------------------------------------------

## Requirements

We are using `Poetry` to manage dependencies. You will find more
information about the dependencies in `pyproject.toml`.

If you don't have `Poetry` installed, you can install it
following these instructions: `https://python-poetry.org/docs/`.

Once the repo's cloned and `Poetry`'s installed, run
`poetry install` in the CLI to install all the dependencies.

`poetry run python3 src/main.py` will create the GUI and allow
you to start processing images.

----------------------------------------------------------------
## Watch outs

Be mindful of attempting to generate cropped images larger than
the original. Also keep in mind that when transforming multiple
images, the dimensions you provide will apply to all images.

**HAPPY IMAGE EDITING**
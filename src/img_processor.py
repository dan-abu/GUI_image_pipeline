import random
import sys
from PIL import Image
from multiprocessing import Pool
from typing import List, Callable

class Metadata:
    """Class representing metadata for images being transformed in the pipeline"""

    def __init__(self, fn: str, width: int, height: int, crop_width: int, crop_height: int):
        """Initialising image metadata"""
        self.name = fn
        self.crop_boxes = []
        self.width = width
        self.height = height
        self.crop_width = crop_width
        self.crop_height = crop_height

    def check_overlap(self, crop1: tuple, crop2: tuple) -> bool:
        """Checks to see if the coordinates of the proposed cropped images overlap. If the coordinates don't overlap, it will return False."""
        x1, y1, x2, y2 = crop1
        a1, b1, a2, b2 = crop2
        return not (x2 <= a1 or x1 >= a2 or y2 <= b1 or y1 >= b2)  # compares shape edges

    def generate_crops(self, num_crops: int) -> list:
        """Generates cropped images from a source image. Confirms that the cropped images don't overlap."""
        attempts = 0
        max_attempts = 1000  # Prevents infinite loops

        while len(self.crop_boxes) < num_crops and attempts < max_attempts:
            # Setting the coords for the proposed cropped image
            attempts += 1
            x1 = random.randint(0, self.width - self.crop_width)
            y1 = random.randint(0, self.height - self.crop_height)
            x2 = x1 + self.crop_width
            y2 = y1 + self.crop_height

            new_crop = (x1, y1, x2, y2)

            # Check if this crop overlaps with any existing crop
            if not any(self.check_overlap(new_crop, crop) for crop in self.crop_boxes):
                self.crop_boxes.append(new_crop)

        if len(self.crop_boxes) < num_crops:
            raise ValueError("Could not find enough non-overlapping crops within the number of attempts.")

        return self.crop_boxes

class Pipeline:
    """Class representing the image processing pipeline"""

    def __init__(self) -> None:
        """Initialising the list of image filenames and images"""
        self.images = []
        self.pre_crop_transformations = []
        self.post_crop_transformations = []

    def bundle_image_metadata(self, im_fns: str, c_width: int, c_height: int):
        """Bundle image and metadata"""
        for im_fn in im_fns:
            image = Image.open(im_fn)
            metadata = Metadata(fn=im_fn, width=image.size[0], height=image.size[1], crop_width=c_width, crop_height=c_height)
            bundle = (image, metadata)
            self.images.append(bundle)

    def apply_transformations_to_iterables(self, transformations: List[Callable]) -> Image:
        """Applies transformations to iterables"""
        transformed_images = []
        for transform in transformations:
            for image in self.images:
                new_image = transform(image[0])
                new_bundle = (new_image, image[1])
                transformed_images.append(new_bundle)
        self.images = transformed_images
        return self.images
    
    @staticmethod
    def apply_transformations(image: Image, transformations: list) -> Image:
        """Applies transformations to image"""
        for transform in transformations:
            image = transform(image)
        return image

    @staticmethod
    def convert_to_greyscale(image: Image) -> Image:
        """Converts the image to greyscale"""
        return image.convert("L")

    @staticmethod
    def rotate_image(image: Image, angle=180) -> Image:
        """Rotates image by 180 degrees."""
        return image.rotate(angle)

    def process_image(self, bundle):
        """Processes a single image bundle (image and metadata)"""
        image, metadata = bundle

        image = self.apply_transformations(image, self.pre_crop_transformations)

        try:
            metadata.generate_crops(3)
        except ValueError as e:
            print(f"Error processing image {bundle[0].filename}: {e}")
            return

        cropped_images = []
        for box in metadata.crop_boxes:
            cropped_image = image.crop(box)
            cropped_image = self.apply_transformations(cropped_image, self.post_crop_transformations)
            cropped_images.append(cropped_image)

        return cropped_images

    def crop_and_transform(self):
        """Crops the image, applies transformations, and saves the result."""

        # Use multiprocessing pool to process images in parallel
        with Pool() as pool:
            results = pool.starmap

def main(filenames: List[str], c_width: int, c_height: int) -> None:
    """Programme entry point"""
    pipeline = Pipeline()  # instantiating pipeline

    # loading image files and gathering metadata
    pipeline.bundle_image_metadata(im_fns=filenames, c_width=c_width, c_height=c_height)

    pipeline.pre_crop_transformations = [pipeline.convert_to_greyscale]  # Define any transformations you want before the cropping

    pipeline.apply_transformations_to_iterables(pipeline.pre_crop_transformations)  # Applying pre-crop transformations

    # generating coords for cropping
    try:
        for image in pipeline.images:
            image[1].generate_crops(3)
    except ValueError as e:
        print(e)
        sys.exit()

    pipeline.post_crop_transformations = [pipeline.rotate_image]

    # Use multiprocessing pool to process images in parallel
    with Pool() as pool:
        results = pool.map(pipeline.process_image, pipeline.images)

    # Flatten the results and save cropped images
    image_count = 0
    for images in results:
        if images:
            for image in images:
                image.save(f"data/cropped_image_{image_count}.jpg")
                image.show()
                image_count += 1
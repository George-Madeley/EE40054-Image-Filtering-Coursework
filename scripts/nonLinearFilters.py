import numpy as np
import matplotlib.pyplot as plt
import math

class NonLinearFilters:
    def apply_filter(self, image, kernel_type='median', kernel_size=3, padding='constant'):
        """
        Performs a 2D convolution on an image using a kernel.

        :param image: The image to be convolved
        :param kernel_type: The type of kernel to convolve the image with
        :param kernel_size: The size of the kernel
        :param padding: The type of padding to use

        :return: The convolved image
        """

        # Get the height and width of the image
        height, width = image.shape

        # Calculate how much the image needs to be padded
        padding_size = int((kernel_size - 1) / 2)

        # Create a padded image with zeros
        padded_image = np.pad(image, padding_size, mode=padding)

        # Create an empty output image
        convolved_image = np.zeros_like(image)

        # Iterate over each pixel in the image
        for i in range(height):
            for j in range(width):
                # Get the region of interest (ROI) from the padded image
                roi = padded_image[i:i+kernel_size, j:j+kernel_size]

                # Apply the desired kernel type
                if kernel_type == 'median':
                    convolved_image[i, j] = self.apply_median_filter(roi)
                else:
                    raise Exception('Invalid kernel type.')
                
        return convolved_image
    
    def apply_median_filter(image_section):
        """
        Performs median filtering on an image section.
        
        :param image_section: The image section to be filtered
        
        :return: The filtered image section
        """

        median = np.median(image_section)
        return median
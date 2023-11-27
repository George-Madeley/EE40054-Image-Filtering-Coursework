import numpy as np

class NonLinearFilters:
    def applyFilter(self, image, kernel_type='median', kernel_size=3, padding='constant'):
        """
        Performs a 2D convolution on an image using a kernel.

        :param image: The image to be convolved
        :param kernel_type: The type of kernel to convolve the image with. Possible values:
            - 'median',
            - 'min',
            - 'max',
        :param kernel_size: The size of the kernel
        :param padding: The type of padding to use. Possible values:
            - 'constant',
            - 'edge',
            - 'linear_ramp',

        :return: The convolved image

        :raises ValueError: If the kernel size is even
        :raises ValueError: If the padding type is invalid
        :raises ValueError: If the kernel size is less than 1
        """

        # Check that the kernel size is odd. If the kernel size is even, raise an exception.
        if kernel_size % 2 == 0:
            raise ValueError('Kernel size must be odd.')
        
        # Check that the padding type is valid. If the padding type is invalid, raise an exception.
        if padding not in ['constant', 'edge', 'linear_ramp']:
            raise ValueError('Invalid padding type.')
        
        # Check that the kernel size is greater than 0. If the kernel size is less than 1, raise an exception.
        if kernel_size < 1:
            raise ValueError('Kernel size must be greater than 0.')

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
                convolved_value = self.calculateConvolvedValue(kernel_type, roi)
                convolved_image[i, j] = convolved_value
                
        return convolved_image

    def calculateConvolvedValue(self, kernel_type, roi):
        """
        Applies the desired filter to the region of interest (ROI).
        
        :param kernel_type: The type of kernel to convolve the image with. Possible values:
            - 'median',
            - 'min',
            - 'max',
        :param roi: The region of interest

        :return: The calculated value

        :raises Exception: If the kernel type is invalid
        """
        if kernel_type == 'median':
            return self.applyMedianFilter(roi)
        elif kernel_type == 'min':
            return self.applyMinFilter(roi)
        elif kernel_type == 'max':
            return self.applyMaxFilter(roi)
        else:
            raise Exception('Invalid kernel type.')
    
    def applyMedianFilter(self, image_section):
        """
        Performs median filtering on an image section.
        
        :param image_section: The image section to be filtered
        
        :return: The filtered image section
        """

        median = np.median(image_section)
        return median
    
    def applyMinFilter(self, image_section):
        """
        Performs min filtering on an image section.
        
        :param image_section: The image section to be filtered
        
        :return: The filtered image section
        """

        min_value = np.min(image_section)
        return min_value
    
    def applyMaxFilter(self, image_section):
        """
        Performs max filtering on an image section.
        
        :param image_section: The image section to be filtered
        
        :return: The filtered image section
        """

        max_value = np.max(image_section)
        return max_value
    
    
NLF = NonLinearFilters()
import numpy as np

class NonLinearFilters:
    def applyFilter(self, image, kernel_type='median', kernel_size=3, padding='constant'):
        """
        Performs a 2D convolution on an image using a kernel.

        :param image: The image to be convolved
        :param kernel_type: The type of kernel to convolve the image with. Possible values:
            - 'median',
            - 'adaptive_weighted_median',
            - 'truncated_median',
            - 'min',
            - 'max',
            - 'midpoint',
            - 'alpha_trimmed_mean',
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
            - 'adaptive_weighted_median',
            - 'truncated_median',
            - 'min',
            - 'max',
            - 'midpoint',
            - 'alpha_trimmed_mean',
        :param roi: The region of interest

        :return: The calculated value

        :raises Exception: If the kernel type is invalid
        """
        if kernel_type == 'median':
            return self.applyMedianFilter(roi)
        elif kernel_type == 'adaptive_weighted_median':
            return self.applyAdaptiveWeightedMedianFilter(roi)
        elif kernel_type == 'truncated_median':
            return self.applyTruncatedMedianFilter(roi)
        elif kernel_type == 'min':
            return self.applyMinFilter(roi)
        elif kernel_type == 'max':
            return self.applyMaxFilter(roi)
        elif kernel_type == 'midpoint':
            return self.applyMidpointFilter(roi)
        elif kernel_type == 'alpha_trimmed_mean':
            return self.applyAlphaTrimmedMeanFilter(roi)
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
    
    def applyAdaptiveWeightedMedianFilter(self, image_section, central_value=100, constant=10):
        """
        Performs adaptive weighted median filtering on an image section.
        
        :param image_section: The image section to be filtered
        :param central_value: The central value of the weights
        :param constant: The constant
        
        :return: The filtered image section
        """

        # Get the height and width of the image section
        height, width = image_section.shape

        weights = np.zeros((height, width))

        # Set the center of the weights to the central value
        weights[int(height / 2), int(width / 2)] = central_value

        # Get array of distances from the center
        distances = np.zeros((height, width))
        for i in range(height):
            for j in range(width):
                distances[i, j] = np.sqrt((i - int(height / 2)) ** 2 + (j - int(width / 2)) ** 2)

        # Flatten the image
        flattened_image_section = image_section.flatten()

        # Sort the pixels
        flattened_image_section.sort()

        # Calculate the standard deviation
        standard_deviation = np.std(flattened_image_section)
        # Calculate the mean
        mean = np.mean(flattened_image_section)
        # Calculate the weight
        if mean == 0:
            # If the mean is 0, then the weights are equal to the central value
            weights = central_value
        else:
            weights = central_value - (constant * distances * standard_deviation / mean)

        # floor the weights and convert them to integers
        weights = np.floor(weights).astype(int).flatten()

        # check if any of the weights are less than 0
        if np.any(weights < 0):
            # If any of the weights are less than 0, then set them to 0
            weights[weights < 0] = 0

        # Repeat the pixels according to their weights
        repeated_pixels = np.repeat(flattened_image_section, weights)

        # Calculate the weighted median
        weighted_median = np.median(repeated_pixels)

        return weighted_median
    
    def applyTruncatedMedianFilter(self, image_section):
        """
        Performs truncated median filtering on an image section.
        
        :param image_section: The image section to be filtered
        
        :return: The filtered image section
        """
        # Force all warnings to be errors
        np.seterr(all='raise')

        # Flatten the image
        flattened_image_section = image_section.flatten()

        # Sort the pixels
        flattened_image_section.sort()

        # Get the minimum and maximum values
        min_value = np.min(flattened_image_section)
        max_value = np.max(flattened_image_section)

        # Get the median value
        median_value = np.median(flattened_image_section)

        # Calculate the difference between the median and the minimum value
        difference_median_min = np.abs(median_value - min_value)

        # Calculate the difference between the median and the maximum value
        difference_median_max = np.abs(median_value - max_value)

        if difference_median_min > difference_median_max:
            # Calculate the lower threshold
            lower_threshold = median_value - difference_median_max
            
            # Get the pixels that are greater than the lower threshold
            truncated_image = flattened_image_section[flattened_image_section >= lower_threshold]
        elif difference_median_min < difference_median_max:
            # Calculate the upper threshold
            upper_threshold = median_value + difference_median_min
            
            # Get the pixels that are less than the upper threshold
            truncated_image = flattened_image_section[flattened_image_section <= upper_threshold]
        else:
            # If the difference between the median and the minimum value is equal
            # to the difference between the median and the maximum value, then
            # the median is eqaul to the mode
            truncated_image = flattened_image_section

        # Calculate the truncated median
        truncated_median = np.median(truncated_image)

        return truncated_median

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
    
    def applyMidpointFilter(self, image_section):
        """
        Performs midpoint filtering on an image section.
        
        :param image_section: The image section to be filtered
        
        :return: The filtered image section
        """

        min_value = np.min(image_section)
        max_value = np.max(image_section)
        midpoint = (min_value + max_value) / 2
        return midpoint
    
    def applyAlphaTrimmedMeanFilter(self, image_section, d=2):
        """
        Performs alpha-trimmed mean filtering on an image section.
        
        :param image_section: The image section to be filtered
        :param d: The number of pixels to be trimmed
        
        :return: The filtered image section
        """

        # Get the height and width of the image section
        height, width = image_section.shape

        # Get the number of pixels to be trimmed
        num_pixels_to_be_trimmed = int(d // 2)

        # Get the total number of pixels
        total_pixels = height * width

        flattened_image_section = image_section.flatten()

        # Sort the pixels
        flattened_image_section.sort()

        # Trim the pixels
        trimmed_pixels = flattened_image_section[num_pixels_to_be_trimmed:total_pixels - num_pixels_to_be_trimmed]

        # Calculate the alpha-trimmed mean
        alpha_trimmed_mean = (1 / (width * height - d)) * np.mean(trimmed_pixels)

        return alpha_trimmed_mean
    
    
NLF = NonLinearFilters()
import numpy as np

from iSpatialFilters import ISpatialFilters

class NonLinearFilters(ISpatialFilters):
    def applyFilter(self, image, filter_name, kernel_size, **kwargs):
        """
        Applies a non-linear filter to an image

        :param image: The image to be convolved
        :param filter_name: The type of kernel to convolve the image with. Possible values:
            - 'median',
            - 'adaptive_weighted_median',
            - 'truncated_median',
            - 'min',
            - 'max',
            - 'midpoint',
            - 'alpha_trimmed_mean',
        :param kernel_size: The size of the kernel
        :param kwargs: The arguments for the filter. Possible values:
            - 'central_value': The central value of the weights (for adaptive weighted median filter)
            - 'constant': The constant (for adaptive weighted median filter)
            - 'd': The number of pixels to be trimmed (for alpha-trimmed mean filter)
            - 'padding': The type of padding to use. Possible values:

        :return: The filtered image
        """

        # Check for errors in the parameters
        self.checkErrors(kernel_size, 'constant', **kwargs)

        # Get the padding type
        padding = kwargs.get('padding', 'constant')
        
        # The filter function is the equation to apply to the region of interest when convolving the image. The filter
        # function is determined by the filter name.
        if filter_name == 'median':
            # The median filter function is the median of the region of interest
            filter_function = lambda roi : self.applyMedianFilter(roi)
        elif filter_name == 'adaptive_weighted_median':
            # The adaptive weighted median filter function is the weighted median of the region of interest. The filter
            # function requires two parameters: the central value and the constant. These parameters are got from the
            # kwargs dictionary.
            central_value = kwargs.get('central_value', 100)
            constant = kwargs.get('constant', 10)
            filter_function = lambda roi : self.applyAdaptiveWeightedMedianFilter(roi, central_value, constant)
        elif filter_name == 'truncated_median':
            # The truncated median filter function is the truncated median of the region of interest
            filter_function = lambda roi : self.applyTruncatedMedianFilter(roi)
        elif filter_name == 'min':
            # The min filter function is the minimum value of the region of interest
            filter_function = lambda roi : self.applyMinFilter(roi)
        elif filter_name == 'max':
            # The max filter function is the maximum value of the region of interest
            filter_function = lambda roi : self.applyMaxFilter(roi)
        elif filter_name == 'midpoint':
            # The midpoint filter function is the midpoint of the region of interest
            filter_function = lambda roi : self.applyMidpointFilter(roi)
        elif filter_name == 'alpha_trimmed_mean':
            # The alpha-trimmed mean filter function is the alpha-trimmed mean of the region of interest. The filter
            # function requires one parameter: d. This parameter is got from the kwargs dictionary.
            d = kwargs.get('d', 2)
            filter_function = lambda roi : self.applyAlphaTrimmedMeanFilter(roi, d)
        else:
            # If the filter name is not recognized, raise an error.
            raise Exception('Invalid filter name.')
        
        # Apply the filter
        return self.calculateSpatialDomainConvolution(image, kernel_size, filter_function, padding)
    
    def calculateSpatialDomainConvolution(self, image, kernel_size, filter_function, padding='constant'):
        """
        Performs a convolution on an image using a kernel using the spatial domain algorithm.
        
        :param image: The image to be convolved
        :param kernel_size: The size of the kernel
        :param filter_function: The filter function to be applied
        :param padding: The type of padding to use. Possible values:
        
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
                convolved_value = filter_function(roi)
                convolved_image[i, j] = convolved_value
                
        return convolved_image
    
    def applyMedianFilter(self, image_section):
        """
        Performs median filtering on an image section.
        
        :param image_section: The image section to be filtered
        
        :return: The filtered image section
        """

        # Calculate the median
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

        # Create a matrix of weights with zeros
        weights = np.zeros((height, width))

        # Set the center of the weights to the central value
        weights[int(height / 2), int(width / 2)] = central_value

        # Calculates the distances from the center by creating a vector of values from -center to center and squaring
        # them and then creating a matrix of distances from the center by adding the vector to its transpose and
        # taking the square root of the result
        center = (width - 1) / 2
        vector = np.linspace(-center, center, width)
        vector = vector ** 2
        distances = np.sqrt(np.add.outer(vector, vector))

        # Flatten the image
        flattened_image_section = image_section.flatten()

        # Calculate the standard deviation
        standard_deviation = np.std(flattened_image_section)
        # Calculate the mean
        mean = np.mean(flattened_image_section)
        
        # If the mean is 0, then the weights are equal to the central value. else the weights are calculated using the
        # formula: weights = central_value - (constant * distances * standard_deviation / mean)
        if mean == 0:
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
        
        # Sort the repeated pixels
        repeated_pixels.sort()

        # Calculate the weighted median
        weighted_median = np.median(repeated_pixels)

        return weighted_median
    
    def applyTruncatedMedianFilter(self, image_section):
        """
        Performs truncated median filtering on an image section.
        
        :param image_section: The image section to be filtered
        
        :return: The filtered image section
        """

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
        
        # Calculate the minimum
        min_value = np.min(image_section)
        return min_value
    
    def applyMaxFilter(self, image_section):
        """
        Performs max filtering on an image section.
        
        :param image_section: The image section to be filtered
        
        :return: The filtered image section
        """

        # Calculate the maximum
        max_value = np.max(image_section)
        return max_value
    
    def applyMidpointFilter(self, image_section):
        """
        Performs midpoint filtering on an image section.
        
        :param image_section: The image section to be filtered
        
        :return: The filtered image section
        """
        # Calculate the midpoint by calculating the average of the minimum and maximum values.
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

        # Flatten the image
        flattened_image_section = image_section.flatten()

        # Sort the pixels
        flattened_image_section.sort()

        # Trim the pixels
        trimmed_pixels = flattened_image_section[num_pixels_to_be_trimmed:total_pixels - num_pixels_to_be_trimmed]

        # Calculate the alpha-trimmed mean
        alpha_trimmed_mean = (1 / (width * height - d)) * np.mean(trimmed_pixels)

        return alpha_trimmed_mean
    
    def checkErrors(self, kernel_size, padding, **kwargs):
        """
        Checks for errors in the LinearFilters class

        :param kernel_size: The size of the kernel
        :param padding: The type of padding to use
        :param kwargs: The arguments for the filter

        :raises TypeError: If the kernel size is not an integer

        :raises ValueError: If the kernel size is even
        :raises ValueError: If the padding type is invalid
        :raises ValueError: If the kernel size is less than 1
        :raises ValueError: If the cutoff frequency is less than 0
        """

        # Check of errors related to the kernel size.
        # Check if the kernel size is an integer
        if isinstance(kernel_size, int):
            # Check if the kernel size is even
            if kernel_size % 2 == 0:
                raise ValueError('Kernel size must be odd.')
            # Check if the kernel size is less than 1
            elif kernel_size < 1:
                raise ValueError('Kernel size must be greater than 0.')
        # If the kernel size is not an integer, raise an error.
        elif kernel_size is not None:
            raise TypeError('Kernel size must be an integer.')
        
        # Check that the central_value is a key in kwargs
        if 'central_value' in kwargs:
            # Get the central_value
            central_value = kwargs.get('central_value')
            # Check that the central_value is a float
            if not isinstance(central_value, float) and central_value is not None:
                raise TypeError('central_value must be a float.')
        
        # Check that constant is a key in kwargs
        if 'constant' in kwargs:
            # Get the constant
            constant = kwargs.get('constant')
            # Check if the constant is a float
            if isinstance(constant, float):
                # Check if the constant is less than 0
                if constant < 0:
                    raise ValueError('constant must be greater than 0.')
            # If the constant is not a float, raise an error.
            elif constant is not None:
                raise TypeError('constant must be a float.')
            
        # Check that d is a key in kwargs
        if 'd' in kwargs:
            # Get d
            d = kwargs.get('d')
            # Check if d is an integer
            if isinstance(d, int):
                # Check if d is less than 0
                if d < 0:
                    raise ValueError('d must be greater than 0.')
            # If d is not an integer, raise an error.
            elif d is not None:
                raise TypeError('d must be an integer.')
        
        # Check for errors related to the padding type.
        if padding not in ['constant', 'edge', 'linear_ramp']:
            raise ValueError('Invalid padding type. Possible values are: constant, edge, linear_ramp.')


NLF = NonLinearFilters()
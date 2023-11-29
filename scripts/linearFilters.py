import numpy as np
import math

from iFrequencyFilters import IFrequencyFilters
from iSpatialFilters import ISpatialFilters

class LinearFilters(IFrequencyFilters, ISpatialFilters):
    """
    Class for applying linear filters to an image
    """

    def applyFilter(self, image, filter_name, kernel_size, **kwargs):
        """
        Applies a linear filter to an image
        
        :param image: The image to be filtered
        :param filter_name: The name of the filter. Possible values are
            - 'gaussian',
            - 'box',
            - 'butterworth_low_pass',
            - 'low_pass'
            - 'geometric_mean',
            - 'harmonic_mean',
            - 'contra_harmonic_mean'
        :param kernel_size: The size of the kernel
        :param kwargs: The arguments for the filter. Possible values are:
            - 'order': The order of the filter. Required for 'butterworth_low_pass' and 'contra_harmonic_mean'
            - 'cutoff': The cutoff frequency. Required for 'butterworth_low_pass' and 'low_pass'
        
        :return: The filtered image
        """

        # Check for errors in the parameters
        self.checkErrors(kernel_size, 'constant', **kwargs)

        # get the kernel
        if filter_name == 'gaussian':
            kernel = self.getGaussianKernel(kernel_size)
            return self.calculateFrequencyDomainConvolution(image, kernel)
        elif filter_name == 'box':
            kernel = self.getBoxKernel(kernel_size)
            return self.calculateFrequencyDomainConvolution(image, kernel)
        elif filter_name == 'butterworth_low_pass':
            order = kwargs.get('order', 2)
            cutoff = kwargs.get('cutoff', 50.0)
            kernel = self.getButterworthLowPassFilter(kernel_size, cutoff, order)
            return self.calculateFrequencyDomainConvolution(image, kernel)
        elif filter_name == 'low_pass':
            cutoff = kwargs.get('cutoff', 50.0)
            kernel = self.getLowPassFilter(kernel_size, cutoff)
            return self.calculateFrequencyDomainConvolution(image, kernel)
        elif filter_name == 'geometric_mean':
            filter_function = lambda roi: self.applyGeometricMeanFilter(roi)
            return self.calculateSpatialDomainConvolution(image, kernel_size, filter_function)
        elif filter_name == 'harmonic_mean':
            filter_function = lambda roi: self.applyHarmonicMeanFilter(roi)
            return self.calculateSpatialDomainConvolution(image, kernel_size, filter_function)
        elif filter_name == 'contra_harmonic_mean':
            order = kwargs.get('order', 2)
            filter_function = lambda roi: self.applyContraHarmonicMeanFilter(roi, order)
            filtered_image =  self.calculateSpatialDomainConvolution(image, kernel_size, filter_function)
            filter_function = lambda roi: self.applyContraHarmonicMeanFilter(roi, -order)
            return self.calculateSpatialDomainConvolution(filtered_image, kernel_size, filter_function)
        else:
            raise Exception('Invalid filter name.')

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

    def calculateFrequencyDomainConvolution(self, image, kernel):
        """
        Performs a convolution on an image using a kernel using the Fast Fourier Transform
        algorithm.

        :param image: The image to be convolved
        :param kernel: The kernel to convolve the image with

        :return: The convolved image
        """

        # Creates tuple for size of padded image and kernel
        new_size = (image.shape[0] + kernel.shape[0] - 1, image.shape[1] + kernel.shape[1] - 1)
        convolved_image = np.zeros(shape=new_size, dtype=image.dtype)

        # Calculates half the size of the image and kernel respectfully in both dimensions
        half_image = ((image.shape[0] - 1) / 2, (image.shape[1] - 1) / 2)
        half_kernal = ((kernel.shape[0] - 1) / 2, (kernel.shape[1] - 1) / 2)

        # Pads the image with duplicate values and the kernel with 0s
        pad_image = np.pad(image, pad_width=(
            (math.floor(half_kernal[0]), math.ceil(half_kernal[0])),
            (math.floor(half_kernal[1]), math.ceil(half_kernal[1]))
        ), mode='edge')


        pad_kernel = np.zeros(shape=new_size)
        pad_kernel[0 : kernel.shape[0], 0 : kernel.shape[1]] = kernel

        # Calculates the Fourier transforms for the image and kernel
        fft_image = np.fft.fft2(pad_image)
        fft_kernel = np.fft.fft2(pad_kernel)

        # Performs the convolutions, inverses the fourier transforms and extracts
        # the real part of each element
        convolved_image = np.real(np.fft.ifft2(fft_image * fft_kernel))
        
        # Function to calculate the padding of the convoluted image
        bounds = lambda axis: kernel.shape[axis] - 1

        # Removes the padding from the convoluted image
        convolved_image = convolved_image[bounds(0) : new_size[0], bounds(1) : new_size[1]]
        
        return convolved_image

    def getGaussianKernel(self, size):
        """
        Creates a Gaussian kernel of size (size x size) with standard deviation sigma

        :param size: The size of the kernel

        :return: The Gaussian kernel
        """
        # Check for errors in the parameters
        self.checkErrors(size, 'constant')

        # Calculates the standard deviation
        stdiv = (size - 1) / 6

        # Creates a kernel of zeros
        kernel = np.zeros(shape=(size, size))
        # Calculates the center of the kernel
        center = (size - 1) / 2
        # Creates a vector of values from -center to center
        vector = np.linspace(-center, center, size)
        vector = vector ** 2
        # Create a matrix of distances from the center
        distances = np.sqrt(np.add.outer(vector, vector))
        # Calculates the constant for the Gaussian function
        constant = 1 / (2 * math.pi * stdiv ** 2)
        # Calculates the Gaussian filter
        kernel = constant * np.exp(-0.5 * distances ** 2 / stdiv ** 2)
        # Normalizes the kernel
        kernel /= np.sum(kernel)
        return kernel

    def getBoxKernel(self, size):
        """
        Creates a box kernel of size (size x size)

        :param size: The size of the kernel

        :return: The box kernel
        """
        # Check for errors in the parameters
        self.checkErrors(size, 'constant')

        # Creates a kernel of ones
        kernel = np.ones(shape=(size, size))
        # Normalizes the kernel
        kernel /= np.sum(kernel)
        return kernel
    
    def getButterworthLowPassFilter(self, size, cutoff, order):
        """
        Creates a Butterworth low pass filter of size (size x size) with cutoff frequency cutoff
        and order order
        
        :param size: The size of the filter
        :param cutoff: The cutoff frequency
        :param order: The order of the filter
        
        :return: The Butterworth low pass filter
        """
        # Check for errors in the parameters
        self.checkErrors(size, 'constant', order=order, cutoff=cutoff)

        # Creates a kernel of zeros
        kernel = np.zeros(shape=(size, size))
        # Calculates the center of the kernel
        center = (size - 1) / 2
        # Creates a vector of values from -center to center
        vector = np.linspace(-center, center, size)
        vector = vector ** 2
        # Create a matrix of distances from the center
        distances = np.sqrt(np.add.outer(vector, vector))
        # Calculates the Butterworth low pass filter
        kernel = 1 / (1 + (distances / cutoff) ** (2 * order))
        # Normalizes the kernel
        kernel /= np.sum(kernel)
        return kernel
    
    def getLowPassFilter(self, size, cutoff):
        """
        Creates a low pass filter of size (size x size) with cutoff frequency cutoff
        
        :param size: The size of the filter
        :param cutoff: The cutoff frequency
        
        :return: The low pass filter
        """
        # Check for errors in the parameters
        self.checkErrors(size, 'constant', cutoff=cutoff)

        # Creates a kernel of zeros
        kernel = np.zeros(shape=(size, size))
        # Calculates the center of the kernel
        center = (size - 1) / 2
        # Creates a vector of values from -center to center
        vector = np.linspace(-center, center, size)
        # Calculates the low pass filter
        low_pass_filter = np.where(np.abs(vector) <= cutoff, 1, 0)
        # Creates the low pass filter
        kernel = np.outer(low_pass_filter, low_pass_filter)
        return kernel
        
    def applyGeometricMeanFilter(self, image_section):
        """
        Performs geometic mean filtering on an image section.
        
        :param image_section: The image section to be filtered
        
        :return: The filtered image section
        """
        product = np.product(image_section)
        geometric_median = product ** (1 / image_section.size)

        return geometric_median
    
    def applyHarmonicMeanFilter(self, image_section):
        """
        Performs harmonic mean filtering on an image section.
        
        :param image_section: The image section to be filtered
        
        :return: The filtered image section
        """
        # Reciprocal of the image section. Return 0 if divide by 0.
        reciprocal = np.divide(1, image_section, out=np.zeros_like(image_section), where=image_section!=0)
        
        reciprocal_sum = np.sum(reciprocal)
        if reciprocal_sum == 0:
            return 0
        
        harmonic_mean = image_section.size / np.sum(reciprocal)
        return harmonic_mean
    
    def applyContraHarmonicMeanFilter(self, image_section, order):
        """
        Performs contra-harmonic mean filtering on an image section.
        
        :param image_section: The image section to be filtered
        :param order: The order of the filter
        
        :return: The filtered image section

        :raises ValueError: If the order is less than or equal to 0
        """
        # set numpy error to raise
        np.seterr('raise')

        # If order + 1 is 0, then the power is 1. Else, calculate the power.
        if order + 1 == 0:
            power = np.ones_like(image_section)
        else:
            power = np.power(image_section, order + 1, out=np.zeros_like(image_section), where=image_section!=0.0)
        numerator = np.sum(power, initial=0)
        
        # If order is 0, then the power is 1. Else, calculate the power.
        if order == 0:
            power = np.ones_like(image_section)
        else:
            power = np.power(image_section, order, out=np.zeros_like(image_section), where=image_section!=0.0)
        denominator = np.sum(power, initial=0)

        if denominator == 0:
            return 0
        contra_harmonic_mean = numerator / denominator

        return contra_harmonic_mean

    def checkErrors(self, kernel_size, padding, **kwargs):
        """
        Checks for errors in the LinearFilters class

        :param kernel_size: The size of the kernel
        :param padding: The type of padding to use
        :param kwargs: The arguments for the filter

        :raises TypeError: If the kernel size is not an integer
        :raises TypeError: If the order is not an integer
        :raises TypeError: If the cutoff frequency is not a float

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
        
        # Check for errors related to the order.
        # Check if the order is in the kwargs
        if 'order' in kwargs:
            order = kwargs['order']
            # Check that the order is an integer
            if not isinstance(order, int) and order is not None:
                raise TypeError('Order must be an integer.')
        
        # Check for errors related to the cutoff frequency.
        # Check if the cutoff frequency is in the kwargs
        if 'cutoff' in kwargs:
            cutoff = kwargs['cutoff']
            # Check if the cutoff frequency is a float
            if isinstance(cutoff, float):
                # Check if the cutoff frequency is less than 0
                if cutoff < 0:
                    raise ValueError('Cutoff frequency must be greater than 0.')
            # If the cutoff frequency is not a float, raise an error.
            elif cutoff is not None:
                raise TypeError('Cutoff frequency must be a float.')
        
        # Check for errors related to the padding type.
        if padding not in ['constant', 'edge', 'linear_ramp']:
            raise ValueError('Invalid padding type. Possible values are: constant, edge, linear_ramp.')      
    
LF = LinearFilters()
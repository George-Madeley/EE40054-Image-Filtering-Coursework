import numpy as np
import math

from iFrequencyFilters import IFrequencyFilters

class EdgeDetector(IFrequencyFilters):
    """
    Class for applying edge detection filters to an image
    """
    def applyFilter(self, image, filter_name, kernel_size, **kwargs):
        """
        Applies a linear filter to an image
        
        :param image: The image to be filtered
        :param filter_name: The name of the filter. Possible values are
            - 'horizontal',
            - 'vertical',
            - 'diagonal',
            - 'magnitude',
            - 'direction',
        :param kernel_size: The size of the kernel
        :param kwargs: The arguments for the filter. Possible values are:
            - 'padding': The type of padding to use. Possible values are:
                - 'constant': Pads with a constant value
                - 'edge': Pads with the edge values
                - 'linear_ramp': Pads with a linear ramp
        
        :return: The filtered image
        """

        # Check for errors in the parameters
        self.checkErrors(kernel_size, 'constant', **kwargs)

        # Get the padding type
        padding = kwargs.get('padding', 'constant')

        # Apply the filter specified by the filter name
        if filter_name == 'horizontal':
            # Get the horizontal kernel and apply the filter
            kernel = self.getHorizontalKernel()
            return self.calculateFrequencyDomainConvolution(image, kernel, padding)
        elif filter_name == 'vertical':
            # Get the vertical kernel and apply the filter
            kernel = self.getVerticalKernel()
            return self.calculateFrequencyDomainConvolution(image, kernel, padding)
        elif filter_name == 'diagonal':
            # Get the diagonal kernel and apply the filter
            kernel = self.getDiagonalKernel()
            return self.calculateFrequencyDomainConvolution(image, kernel, padding)
        elif filter_name == 'magnitude':
            # Calculate the magnitude of the edges
            return self.calculateEdgeMagnitude(image, padding)
        elif filter_name == 'direction':
            # Calculate the direction of the edges
            return self.calculateEdgeDirection(image, padding)
        else:
            # Raise an error if the filter name is not recognized
            raise Exception('Invalid filter name.')

    def calculateFrequencyDomainConvolution(self, image, kernel, padding='constant'):
        """
        Performs a convolution on an image using a kernel using the Fast Fourier Transform
        algorithm.

        :param image: The image to be convolved
        :param kernel: The kernel to convolve the image with
        :param padding: The type of padding to use

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
        ), mode=padding)

        # Creates a new kernel with the same size as the padded image and fills it with 0s. This is requried for the
        # convolution to work properly.
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

    def getHorizontalKernel(self):
        """
        Gets the horizontal kernel
        """
        return np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
    
    def getVerticalKernel(self):
        """
        Gets the vertical kernel
        """
        return np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    
    def getDiagonalKernel(self):
        """
        Gets the diagonal kernel
        """
        return np.array([[2, 1, 0], [1, 0, -1], [0, -1, -2]])
    
    
    def calculateEdgeMagnitude(self, image, padding='constant'):
        """
        Calculates the magnitude of the edges
        
        :param image: The image to calculate the magnitude of the edges for
        :param padding: The type of padding to use

        :return: The magnitude of the edges
        """
        
        # Gets the horizontal and vertical kernels
        horizonal_kernel = self.getHorizontalKernel()
        vertical_kernel = self.getVerticalKernel()

        # Gets the horizontal and vertical edges
        horizontal_edges = self.calculateFrequencyDomainConvolution(image, horizonal_kernel, padding)
        vertical_edges = self.calculateFrequencyDomainConvolution(image, vertical_kernel, padding)

        # Calculates the magnitude of the edges using the pythagorean theorem
        edge_magnitude = np.sqrt(np.square(horizontal_edges) + np.square(vertical_edges))
        
        return edge_magnitude
    
    def calculateEdgeDirection(self, image, padding='constant'):
        """
        Calculates the direction of the edges
        
        :param image: The image to calculate the direction of the edges for
        :param padding: The type of padding to use

        :return: The direction of the edges
        """
        
        # Gets the horizontal and vertical kernels
        horizonal_kernel = self.getHorizontalKernel()
        vertical_kernel = self.getVerticalKernel()

        # Gets the horizontal and vertical edges
        horizontal_edges = self.calculateFrequencyDomainConvolution(image, horizonal_kernel, padding)
        vertical_edges = self.calculateFrequencyDomainConvolution(image, vertical_kernel, padding)

        # Calculates the direction of the edges
        edge_direction = np.arctan2(horizontal_edges, vertical_edges)
        
        return edge_direction
    
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
        
        # Check for errors related to the padding type.
        if padding not in ['constant', 'edge', 'linear_ramp']:
            raise ValueError('Invalid padding type. Possible values are: constant, edge, linear_ramp.')

ED = EdgeDetector()
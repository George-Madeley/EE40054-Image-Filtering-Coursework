import numpy as np
import matplotlib.pyplot as plt
import math

class LinearFilters:
    """
    Class for applying linear filters to an image
    """

    def getKernel(self, filter_name, kernel_size):
        """
        Gets the kernel for a given filter name and kernel size
        
        :param filter_name: The name of the filter
        :param kernel_size: The size of the kernel
        
        :return: The kernel
        
        :raises: Exception if the filter name is invalid
        """
        # get the kernel
        if filter_name == 'gaussian':
            kernel = self.getGaussianKernel(kernel_size, 1)
        elif filter_name == 'box':
            kernel = self.getBoxKernel(kernel_size)
        else:
            raise Exception('Invalid filter name.')
        
        return kernel

    def getGaussianKernel(self, size, stdiv):
        """
        Creates a Gaussian kernel of size (size x size) with standard deviation sigma

        :param size: The size of the kernel
        :param stdiv: The standard deviation of the kernel

        :return: The Gaussian kernel
        """

        # Creates a kernel of zeros
        kernel = np.zeros(shape=(size, size))
        # Calculates the center of the kernel
        center = (size - 1) / 2
        # Creates a vector of values from -center to center
        vector = np.linspace(-center, center, size)
        # Calculates the constant for the Gaussian function
        constant = 1 / (2 * math.pi * stdiv ** 2)
        # Calculates the Gaussian filter
        gaussian_fitler = constant * np.exp(-0.5 * vector ** 2 / stdiv ** 2)
        # Creates the Gaussian kernel
        kernel = np.outer(gaussian_fitler, gaussian_fitler)
        # Normalizes the kernel
        kernel /= np.sum(kernel)
        return kernel

    def getBoxKernel(self, size):
        """
        Creates a box kernel of size (size x size)

        :param size: The size of the kernel

        :return: The box kernel
        """
        # Creates a kernel of ones
        kernel = np.ones(shape=(size, size))
        # Normalizes the kernel
        kernel /= np.sum(kernel)
        return kernel

    def apply_filter(self, image, kernel):
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
    
LF = LinearFilters()
import numpy as np
import matplotlib.pyplot as plt
import math

class EdgeDetector:
    """
    Class for applying edge detection filters to an image
    """

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
    
    def apply_filter(self, image, kernel):
        """
        Applies a filter to an image
        
        :param image: The image to be filtered
        :param kernel: The kernel to be applied to the image

        :return: The filtered image
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
    
    def calculateEdgeMagnitude(self, image):
        """
        Calculates the magnitude of the edges
        
        :param image: The image to calculate the magnitude of the edges for

        :return: The magnitude of the edges
        """
        
        # Gets the horizontal and vertical kernels
        horizonal_kernel = self.getHorizontalKernel()
        vertical_kernel = self.getVerticalKernel()

        # Gets the horizontal and vertical edges
        horizontal_edges = self.apply_filter(image, horizonal_kernel)
        vertical_edges = self.apply_filter(image, vertical_kernel)

        # Calculates the magnitude of the edges
        edge_magnitude = np.sqrt(np.square(horizontal_edges) + np.square(vertical_edges))
        
        return edge_magnitude
    
    def calculateEdgeDirection(self, image):
        """
        Calculates the direction of the edges
        
        :param image: The image to calculate the direction of the edges for

        :return: The direction of the edges
        """
        
        # Gets the horizontal and vertical kernels
        horizonal_kernel = self.getHorizontalKernel()
        vertical_kernel = self.getVerticalKernel()

        # Gets the horizontal and vertical edges
        horizontal_edges = self.apply_filter(image, horizonal_kernel)
        vertical_edges = self.apply_filter(image, vertical_kernel)

        # Calculates the direction of the edges
        edge_direction = np.arctan2(horizontal_edges, vertical_edges)
        
        return edge_direction

ED = EdgeDetector()
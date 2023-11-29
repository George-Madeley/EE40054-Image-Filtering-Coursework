from abc import ABC, abstractmethod

class IFrequencyFilters(ABC):
    @abstractmethod
    def applyFilter(self, image, filter_name: str, kernel_size: int, order=2, cutoff=50.0):
        """
        Applies a linear filter to an image
        
        :param image: The image to be filtered
        :param filter_name: The name of the filter
        :param kernel_size: The size of the kernel
        :param order: The order of the filter
        :param cutoff: The cutoff frequency
        
        :return: The filtered image
        """
        pass

    @abstractmethod
    def calculateFrequencyDomainConvolution(self, image, kernel):
        """
        Performs a convolution on an image using a kernel using the Fast Fourier Transform
        algorithm.

        :param image: The image to be convolved
        :param kernel: The kernel to convolve the image with

        :return: The convolved image
        """
        pass
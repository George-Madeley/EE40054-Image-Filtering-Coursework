from abc import ABC, abstractmethod

class ISpatialFilters(ABC):
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
    def calculateSpatialDomainConvolution(self, image, kernel_size, filter_function, padding='constant'):
        """
        Performs a convolution on an image using a kernel using the spatial domain algorithm.
        
        :param image: The image to be convolved
        :param kernel_size: The size of the kernel
        :param filter_function: The filter function to be applied
        :param padding: The type of padding to use. Possible values:
        
        :return: The convolved image
        """
        pass
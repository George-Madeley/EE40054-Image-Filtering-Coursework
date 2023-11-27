import sys
import os.path
import matplotlib.pyplot as plt
from linearFilters import LF
from nonLinearFilters import NLF
from edgeDetector import ED
import random
import string
import csv


def main():
    """
    Main function
    """

    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print('Usage: python main.py <image>')
        sys.exit(1)

    image_path = arguments[0]

    # get image name without the extension
    image_name = os.path.splitext(os.path.basename(image_path))[0]

    # Read the image
    image = plt.imread(image_path)

    MIN_KERNEL_SIZE = 3
    MAX_KERNEL_SIZE = 15

    # Test the linear filters
    testLinearFilters(image, image_name, MIN_KERNEL_SIZE, MAX_KERNEL_SIZE)


def testLinearFilters(source_image, source_image_name, min_kernel_size, max_kernel_size):
    """
    Tests the linear filters
    
    :param source_image: The image to be filtered
    :param source_image_name: The name of the image
    :param min_kernel_size: The minimum kernel size
    :param max_kernel_size: The maximum kernel size
    """

    results_csv_file_name = getResultsFile()

    filters = ['gaussian', 'box', 'butterworth_low_pass', 'low_pass']
    kernel_sizes = range(min_kernel_size, max_kernel_size + 1, 2)

    for filter_name in filters:
        for kernel_size in kernel_sizes:
            # Get the image filename
            dest_image_file_name = getFileName(source_image_name, filter_name, kernel_size, 'constant')

            # Get the kernel
            kernel = LF.getKernel(filter_name, kernel_size)
            
            # Apply the filter
            dest_image = LF.apply_filter(source_image, kernel)

            # Save the image
            plt.imsave(dest_image_file_name, dest_image, cmap='gray')

            # Write the results to the results file
            with open(results_csv_file_name, 'a', newline='') as resultsFile:
                csvWriter = csv.writer(resultsFile)
                csvWriter.writerow([source_image_name, 'linear', filter_name, kernel_size, 'constant', dest_image_file_name])
        

def getResultsFile():
    """
    Gets the file name for the results file

    :return: The file name
    """
    resultsFileName = './results/results.csv'
    headers = ['image_name', 'filter_type', 'filter_name', 'kernel_size', 'padding', 'file_name']

    # Check if the results directory exists
    directory = './results/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Check if the file exists by checking if the file name is already taken.
    # If the file does not exist, create it and write the header
    fileExists = os.path.isfile(resultsFileName)
    if not fileExists:
        with open(resultsFileName, 'w') as resultsFile:
            csvWriter = csv.writer(resultsFile)
            csvWriter.writerow(headers)

    return resultsFileName


def getFileName(image_name, filter_name, kernel_size, padding):
    """
    Creates a file name for the results of the filter

    :param image_name: The name of the image
    :param filter_name: The name of the filter
    :param kernel_size: The size of the kernel
    :param padding: The type of padding

    :return: The file name
    """

    # Create a directory to store the results if it doesn't exist
    directory = './results/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create a directory for the filter type if it doesn't exist
    directory += image_name + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create a directory for the filter name if it doesn't exist
    directory += filter_name + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Check if the file exists by checking if the file name is already taken.
    # If it is, generate a new file name and check again.
    fileExists = True
    while fileExists:
        # Generate a random 8 long string. This will be used to name the file
        # so that we don't overwrite the previous results
        random_string = ''.join(random.choice(string.ascii_letters) for i in range(8))
        # join kernel size, padding, and random_string with '-' to create the file name
        fileName = '-'.join([str(kernel_size), padding, random_string]) + '.png'

        # add the file name to the directory
        fileName = directory + fileName

        # check if the file exists
        fileExists = os.path.isfile(fileName)

    return fileName



if __name__ == '__main__':
    main()
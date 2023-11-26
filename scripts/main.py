import sys
import os.path
import matplotlib.pyplot as plt
from linearFilters import LinearFilters as lf
from nonLinearFilters import NonLinearFilters as nlf
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

    # Read the image
    image = plt.imread(image_path)

    MIN_KERNEL_SIZE = 3
    MAX_KERNEL_SIZE = 15

    # Test the linear filters
    testLinearFilters(image, MIN_KERNEL_SIZE, MAX_KERNEL_SIZE)


def testLinearFilters(image, min_kernel_size, max_kernel_size):
    """
    Tests the linear filters
    
    :param image: The image to be filtered
    :param min_kernel_size: The minimum kernel size
    :param max_kernel_size: The maximum kernel size
    """

    results_csv_file_name = getResultsFile()

    filters = ['gaussian', 'box']
    kernel_sizes = range(min_kernel_size, max_kernel_size + 1, 2)

    for filter_name in filters:
        for kernel_size in kernel_sizes:
            # Get the image filename
            finale_img_file_name = getFileName(filter_name)

            # Get the kernel
            kernel = lf.getKernel(filter_name, kernel_size)
            
            # Apply the filter
            final_img = lf.apply_filter(image, kernel)

            # Save the image
            plt.imsave(finale_img_file_name, final_img, cmap='gray')

            # Write the results to the results file
            with open(results_csv_file_name, 'a', newline='') as resultsFile:
                csvWriter = csv.writer(resultsFile)
                csvWriter.writerow([True, filter_name, kernel_size, 'constant', finale_img_file_name])
        

def getResultsFile():
    """
    Gets the file name for the results file

    :return: The file name
    """
    resultsFileName = './results/results.csv'
    headers = ['linear', 'filter', 'kernel_size', 'padding', 'file_name']

    # Check if the file exists by checking if the file name is already taken.
    # If the file does not exist, create it and write the header
    fileExists = os.path.isfile(resultsFileName)
    if not fileExists:
        with open(resultsFileName, 'w') as resultsFile:
            csvWriter = csv.writer(resultsFile)
            csvWriter.writerow(headers)

    return resultsFileName


def getFileName(filter):
    """
    Creates a file name for the results of the filter

    :param filter: The filter that was used

    :return: The file name
    """

    # Create a directory to store the results if it doesn't exist
    directory = './results/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Check if filter directory exists
    directory += filter + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Check if the file exists by checking if the file name is already taken.
    # If it is, generate a new file name and check again.
    fileExists = True
    while fileExists:
        # Generate a random 8 long string. This will be used to name the file
        # so that we don't overwrite the previous results
        random_string = ''.join(random.choice(string.ascii_letters) for i in range(8))
        fileName = directory + random_string + '.png'

        # check if the file exists
        fileExists = os.path.isfile(fileName)

    return fileName



if __name__ == '__main__':
    main()
import sys
import os.path
import matplotlib.pyplot as plt
import random
import string
import csv
import time
import pandas as pd

from linearFilters import LF
from nonLinearFilters import NLF
from edgeDetector import ED


def main():
    """
    Main function
    """



    arguments = sys.argv[1:]
    if len(arguments) != 1:
        print('Usage: python main.py <image>')
        sys.exit(1)


    if arguments[0] == 'filter':
        image_paths = ['./img/foetus.png']
        for image_path in image_paths:

            linear_filters = ['gaussian', 'box', 'butterworth_low_pass', 'low_pass', 'geometric_mean', 'harmonic_mean', 'contra_harmonic_mean']
            non_linear_filters = ['median', 'adaptive_weighted_median', 'truncated_median', 'max', 'min', 'midpoint', 'alpha_trimmed_mean']

            # Test the linear filters
            testFilters(image_path, LF, linear_filters)

            # Test the non-linear filters
            testFilters(image_path, NLF, non_linear_filters)
    elif arguments[0] == 'edge':
        testEdgeDetectors()
        sys.exit(0)
    else:
        # raise an error if the argument is not recognized
        raise ValueError('Argument not recognized. Use \'filter\' or \'edge\'.')
        

def testFilters(source_image_path, F, filters, min_kernel_size=3, max_kernel_size=15, padding='constant'):
    """
    Tests the filters
    
    :param source_image_path: The path to the image to be filtered
    :param F: The clas that applies the given filter.
    :param filters: The names of the filters
    :param min_kernel_size: The minimum kernel size
    :param max_kernel_size: The maximum kernel size
    :param padding: The type of padding to use
    """
    
    # get image name without the extension
    source_image_name = os.path.splitext(os.path.basename(source_image_path))[0]

    # Read the image
    source_image = plt.imread(source_image_path)

    results_csv_file_name = getResultsFile()

    filter_type = 'linear' if F == LF else 'nonlinear'

    kernel_sizes = range(min_kernel_size, max_kernel_size + 1, 2)

    for filter_name in filters:
        for kernel_size in kernel_sizes:
            # Get the image filename
            dest_image_file_name = getFileName(kernel_size, padding, 'filter', source_image_name, filter_name)
            
            # Start the timer
            start_time = time.perf_counter_ns()
            # Apply the filter
            dest_image = F.applyFilter(source_image, filter_name, kernel_size)
            # Stop the timer
            end_time = time.perf_counter_ns()
            # Calculate the runtime
            runtime = end_time - start_time

            # Save the image
            plt.imsave(dest_image_file_name, dest_image, cmap='gray')

            # Print the results
            print(f'Image: {source_image_name}\tFilter Type: {filter_type}\tFilter: {filter_name}\tKernel Size: {kernel_size}\tPadding: constant')

            # Write the results to the results file
            with open(results_csv_file_name, 'a', newline='') as resultsFile:
                csvWriter = csv.writer(resultsFile)
                csvWriter.writerow([source_image_name, filter_type, filter_name, kernel_size, padding, runtime, dest_image_file_name])

def testEdgeDetectors():
    """
    Tests the edge detectors
    """

    df = pd.read_csv('./results/results.csv')

    results_csv_file_name = getResultsFile('./results/edge-results.csv')

    for row in df.iterrows():
        image_name = row[1]['image_name']
        filter_name = row[1]['filter_name']
        kernel_size = row[1]['kernel_size']
        padding = row[1]['padding']
        file_name = row[1]['file_name']

        # Get the image
        image = plt.imread(file_name)

        # Get the images first channel
        image = image[:, :, 0]

        # Get the image filename
        magnitude_image_file_name = getFileName(kernel_size, f'{padding}', 'edge', image_name, filter_name, 'magnitude')
        direction_image_file_name = getFileName(kernel_size, f'{padding}', 'edge', image_name, filter_name, 'direction')
        combined_image_file_name = getFileName(kernel_size, f'{padding}', 'edge', image_name, filter_name, 'combined')
        
        # Apply the filter
        magnitude_image = ED.applyFilter(image, 'magnitude', kernel_size)
        direction_image = ED.applyFilter(image, 'direction', kernel_size)
        combined_image = magnitude_image * direction_image

        # Save the image
        plt.imsave(magnitude_image_file_name, magnitude_image, cmap='gray')
        # Save the directional image using a rainbow colormap
        plt.imsave(direction_image_file_name, direction_image, cmap='rainbow')
        # Save the combined image
        plt.imsave(combined_image_file_name, combined_image, cmap='rainbow')

        # Print the results
        print(f'Image: {image_name}\tFilter Type: edge\tFilter: {filter_name}')

        with open(results_csv_file_name, 'a', newline='') as resultsFile:
            csvWriter = csv.writer(resultsFile)
            csvWriter.writerow([image_name, 'magnitude', filter_name, kernel_size, 'constant', -1, magnitude_image_file_name])
            csvWriter.writerow([image_name, 'direction', filter_name, kernel_size, 'constant', -1, direction_image_file_name])
            csvWriter.writerow([image_name, 'combined', filter_name, kernel_size, 'constant', -1, combined_image_file_name])

    
def getResultsFile(file_name='./results/results.csv'):
    """
    Gets the file name for the results file

    :return: The file name
    """
    resultsFileName = file_name
    headers = ['image_name', 'filter_type', 'filter_name', 'kernel_size', 'padding', 'runtime', 'file_name']

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


def getFileName(kernel_size, padding, *args):
    """
    Creates a file name for the results of the filter

    :param kernel_size: The size of the kernel
    :param padding: The type of padding
    :param args: Any additional directories to add to the file name in the order stated.

    :return: The file name
    """

    # Create a directory to store the results if it doesn't exist
    directory = './results/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create a directory for very str in args if it doesn't exist
    for arg in args:
        directory += arg + '/'
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
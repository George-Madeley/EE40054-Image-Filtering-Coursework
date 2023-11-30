import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

fileName = './results/results.csv'

df = pd.read_csv(fileName)

# get the unique values of the image_name column
image_names = df.image_name.unique()



for image_name in image_names:
    # Filter the dataframe by image_name
    df_image = df[df.image_name == image_name]
    
    # get the unique values of the filter_name column
    filter_names = df_image.filter_name.unique()
    for filter_name in filter_names:
        # Filter the dataframe by filter_name
        df_filter = df_image[df_image.filter_name == filter_name]

        # get the unique values of the kernel_size column
        kernel_sizes = df_filter.kernel_size.unique()
        num_kernel_sizes = len(kernel_sizes)
        num_rows = np.ceil(num_kernel_sizes / 2.0).astype(int)

        subplot_index = 1
        fig, ax = plt.subplots(nrows=num_rows, ncols=2)

        # Split the filter_name into words and capitalize the first letter of each word
        title = ' '.join([word.capitalize() for word in filter_name.split('_')])
        # set the title of the figure
        fig.suptitle(f'{title} with varying Kernal Sizes', fontsize=14)

        # set the size of the figure
        fig.set_size_inches(6, 8)

        # Plot the original image for comparison
        original_image_file_name = f'./img/{image_name}.png'
        image = plt.imread(original_image_file_name)
        plt.subplot(num_rows, 2, subplot_index)
        plt.imshow(image, cmap='gray')
        plt.title('Original')
        plt.axis('off')
        subplot_index += 1

        for kernel_size in kernel_sizes:
            # Filter the dataframe by kernel_size
            record = df_filter[df_filter.kernel_size == kernel_size]
            record = record.iloc[0]

            # get image fileName
            image_file_name = record.file_name

            # load in the image
            image = plt.imread(image_file_name)

            plt.subplot(num_rows, 2, subplot_index)
            plt.imshow(image, cmap='gray')
            plt.title(f'Kernel size: {kernel_size} x {kernel_size}')
            plt.axis('off')
            subplot_index += 1
        plt.savefig(f'./img/{image_name}-{filter_name}.png', bbox_inches='tight', dpi=600)
        plt.clf()
        plt.close()


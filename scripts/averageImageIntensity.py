import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

filename = './results/results.csv'

df = pd.read_csv(filename)

# get the unique values of the filter_name column
filter_names = df.filter_name.unique()
for filter_name in filter_names:
    # Filter the dataframe by filter_name
    df_filter = df[df.filter_name == filter_name]
    # get the unique values of the image_name column
    image_names = df_filter.image_name.unique()

    # get the figure and axes
    fig, ax = plt.subplots(nrows=1, ncols=2)
    # set the size of the figure
    fig.set_size_inches(8, 4)
    # set the suptitle
    filter_name_title = filter_name.replace('_', ' ').capitalize()

    figure_title = f'Average Intensity of Images Filtered with the {filter_name_title} Filter'
    plt.suptitle(figure_title.capitalize(), fontsize=14)

    for i, image_name in enumerate(image_names):
        # Filter the dataframe by image_name
        df_image = df_filter[df_filter.image_name == image_name]
        
        # get the unique values of the kernel_size column
        kernel_sizes = df_filter.kernel_size.unique()

        bins_size = 20

        image_file_name = f'./img/{image_name}.png'
        # read the image
        image = plt.imread(image_file_name)

        # average the intensity values of the image
        average_intensity = np.average(image)

        intensities = [average_intensity]
        kernel_sizes_str = ['original']

        for kernel_size in kernel_sizes:
            # Filter the dataframe by kernel_size
            record = df_filter[df_filter.kernel_size == kernel_size]
            record = record.iloc[0]
            # get the image filename
            image_file_name = record['file_name']
            # read the image
            image = plt.imread(image_file_name)
            # select the first channel of the image
            image = image[:, :, 0]

            # average the intensity values of the image
            average_intensity = np.average(image)
            # append the first hist value to the amount_of_darks list
            intensities.append(average_intensity)
            # append the kernel_size to the kernel_sizes_str list
            kernel_sizes_str.append(f'{kernel_size}x{kernel_size}')

        plt.subplot(1, 2, i+1)
        # plot the amount_of_darks list against the kernel_size list on a bar chart
        plt.bar(kernel_sizes_str, intensities)
        plt.xlabel('Kernel size')
        plt.ylabel(f'Average intensity')
        # use scientific notation for the y-axis
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        # Angle the x-axis labels
        plt.xticks(rotation=45)
        plt.title(image_name)

    # set the spacing between subplots
    plt.tight_layout()
    # plt.show()
    plt.savefig(f'./img/intensities-{filter_name}.png', bbox_inches='tight', dpi=600)
    plt.clf()
    plt.close()

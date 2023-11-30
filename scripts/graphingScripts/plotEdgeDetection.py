import pandas as pd
import matplotlib.pyplot as plt

filter_names = [
    'low_pass',
    'butterworth_low_pass',
    'gaussian',
    'box',
    'geometric_mean',
    'harmonic_mean',
    'contra_harmonic_mean',
    'median',
    'adaptive_weighted_median',
    'truncated_median',
    'midpoint',
    'alpha_trimmed_mean',
]

sizes = [
    (5, 5),
    (5, 5),
    (11, 11),
    (5, 5),
    (5, 5),
    (3, 3),
    (5, 5),
    (7, 5),
    (7, 5),
    (9, 5),
    (3, 3),
    (7, 7),
]

image_names = [
    'foetus',
    'NZjers1',
]

filter_types = [
    'magnitude',
    'direction',
]

df = pd.read_csv('./results/edge-results.csv')

for i, image_name in enumerate(image_names):
    for filter_type in filter_types:

        fig, ax = plt.subplots(nrows=6, ncols=2)

        # title subplot
        fig.suptitle(f'{image_name} with {filter_type} detection', fontsize=14)

        # set the size of the figure
        fig.set_size_inches(6, 12)

        subplot_index = 1
        for filter_name, size in zip(filter_names, sizes):
            kernel_size = size[i]

            # get the record that matches the filter name, image name, kernel size, and filter type
            record = df.loc[(df['filter_name'] == filter_name) & (df['image_name'] == image_name) & (df['kernel_size'] == kernel_size) & (df['filter_type'] == filter_type)]

            # get the first row
            record = record.iloc[0]

            # get the image
            image = plt.imread(record['file_name'])

            # add the image to the subplot
            plt.subplot(6, 2, subplot_index)
            plt.imshow(image)
            filter_name_title = filter_name.replace('_', ' ').title()
            plt.title(f'{filter_name_title} ({kernel_size}x{kernel_size})')
            plt.axis('off')
            subplot_index += 1

        plt.tight_layout()

        plt.savefig(f'./img/edge-detection-{image_name}-{filter_type}.png')
        # plt.show()





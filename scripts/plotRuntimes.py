import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

fileName = './results/results.csv'

df = pd.read_csv(fileName)

# get the unique values of the filter_name column
filter_names = df.filter_name.unique()

for filter_name in filter_names:
    # Filter the dataframe by filter_name
    df_filter = df[df.filter_name == filter_name]

    # Get the unique values of the image_name column
    image_names = df_filter.image_name.unique()

    # get the figure and axes
    fig, ax = plt.subplots(nrows=1, ncols=2)
    # set the size of the figure
    fig.set_size_inches(6, 3)

    # set the y-axis to use scientific notation
    ax[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    for i, image_name in enumerate(image_names):
        # Filter the dataframe by image_name
        df_image = df_filter[df_filter.image_name == image_name]

        # subplot the image
        plt.subplot(1, 2, i+1)

        # plot a line graph of the runtimes
        sns.lineplot(x='kernel_size', y='runtime', data=df_image)

        # set the title of the subplot
        plt.title(f'Runtime of {image_name}')
        # set the x-axis label
        plt.xlabel('Kernel Size')
        # set the y-axis label
        plt.ylabel('Runtime (ns)')

    # set the spacing between subplots
    plt.tight_layout()

    # save the figure
    plt.savefig(f'./img/runtimes-{filter_name}.png', bbox_inches='tight', dpi=600)
    
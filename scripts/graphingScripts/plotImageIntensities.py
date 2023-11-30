import matplotlib.pyplot as plt

# get the figure and axes
fig, ax = plt.subplots(nrows=1, ncols=2)
# set the size of the figure
fig.set_size_inches(6, 3)

# set the y-axis to use scientific notation
ax[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

image_names = ['foetus', 'NZjers1']

# subplot the intensities of each image on seperate histograms with 26 bins
for i, image_name in enumerate(image_names):
    # get the image file name
    image_file_name = f'./img/{image_name}.png'
    # load in the image
    image = plt.imread(image_file_name)
    # subplot the image
    plt.subplot(1, 2, i+1)
    # plot the intensity histogram
    plt.hist(image.ravel(), bins=26)
    # set the title of the subplot
    plt.title(f'Intensity of {image_name}')
    # set the x-axis label
    plt.xlabel('Intensity')
    # set the y-axis label
    plt.ylabel('Frequency')
    
# set the spacing between subplots
plt.tight_layout()

# save the figure
plt.savefig('./img/intensity_histograms.png', bbox_inches='tight', dpi=600)
# show the figure
plt.show()


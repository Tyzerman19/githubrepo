import matplotlib.pyplot as plt

# Dimensions and distances
distance_to_house = 38.405  # Distance from throw area to house center
playing_area_width = 4.7  # Width of the playable area

# Radii of circles for the house
twelveft_radius = 1.829
eightft_radius = 1.219
fourft_radius = 0.610
button_radius = 0.152

# Function to plot the simplified curling sheet
def plot_curling_sheet():
    # Create a figure and axis
    fig, ax = plt.subplots()

    # Define the center of the house
    house_center = distance_to_house

    # Plot the tee line (end of playable area)
    back_line = house_center + twelveft_radius
    ax.plot([back_line, back_line], [0, playing_area_width], color='red')

    # Define colors and radii for the circles representing the house
    colors = ['red', 'white', 'blue', 'white']
    radii = [twelveft_radius, eightft_radius, fourft_radius, button_radius]

    # Plot the hog line 6.4 meters ahead of the house center
    hog_line = house_center - 6.4
    ax.plot([hog_line, hog_line], [0, playing_area_width], color='red')

    # Plot the center line running down the middle of the playable area
    ax.plot([0, back_line], [playing_area_width / 2, playing_area_width / 2], color='black')

    # Plot the back line
    ax.plot([house_center, house_center], [0, playing_area_width], color='black')

    # Plot the circles for the house with specified colors
    for color, radius in zip(colors, radii):
        ax.add_patch(plt.Circle((house_center, playing_area_width / 2), radius, color=color, fill=True))
    # Set plot limits, labels, and equal aspect ratio for x and y axes
    ax.set_xlim(0, house_center + twelveft_radius)
    ax.set_ylim(0, playing_area_width)
    ax.set_xlabel('Length (m)')
    ax.set_ylabel('Width (m)')
    ax.set_title('Simplified Curling Sheet')
    ax.set_aspect('equal')  # Ensure equal scaling for x and y axes

    plt.show()

# Call the function to visualize the simplified curling sheet
plot_curling_sheet()


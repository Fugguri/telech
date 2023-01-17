import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def add_value_labels(ax, spacing=5):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """
    print(ax)
    # For each bar: Place a label
    for rect in ax:
        print(rect)
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:.1f}".format(y_value)

        # Create annotation
        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va)                      # Vertically align label differently for
        # positive and negative values.


# Call the function above. All the magic happens there.

def create_plot_png(dataset: dict):
    # set seaborn style
    sns.set_theme()
    # define DataFrame
    df = pd.DataFrame(dataset)

    # create area chart
    ax1 = plt.stackplot(df.period,  df["join"],
                        labels=['New'],
                        colors=["#38c286"],
                        )
    ax2 = plt.stackplot(df.period,  df["left"],
                        labels=['Left'],
                        colors=["#ee4c12"],)
    # add legend
    plt.legend(numpoints=1, frameon=False,
               loc='upper center', ncol=2)
    # remove ticks
    # plt.xticks([])
    plt.yticks([])
    # display area chart
    # plt.tight_layout()
    # add text

    plt.figtext(0.02, 0.1, "ChurnAnalytics",
                fontsize=14, fontweight="bold")
    plt.figtext(0.3, 0.1, "TeleChurn.com",
                fontsize=14, )
    plt.title("Last week", loc="left", pad=1.4, fontsize=14, fontweight="bold")
    plt.savefig('out.png', transparent=True)

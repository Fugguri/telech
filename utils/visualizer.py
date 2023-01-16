import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def create(dataset: dict):
    # set seaborn style
    sns.set_theme()
    # define DataFrame
    df = pd.DataFrame(dataset)

    # create area chart
    plt.stackplot(df.period,  df.team_B,
                  labels=['New'],
                  colors=["#38c286",]
                  )
    plt.stackplot(df.period,  df.team_C,
                  labels=['Left'],
                  colors=["#ee4c12"],)
    # add legend
    plt.legend(loc='lower right')

    # display area chart
    plt.tight_layout()
    plt.savefig('out.png')

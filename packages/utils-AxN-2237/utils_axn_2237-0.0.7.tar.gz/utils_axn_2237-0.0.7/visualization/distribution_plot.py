import matplotlib.pyplot as plt
import seaborn as sns

def plot_count_pairs(data_df, feature, title="", hue=None, color_palette=None, save_path=None):
    """
    Plots a countplot (bar chart) of a categorical feature, optionally grouped by a hue.

    Parameters:
        data_df (pd.DataFrame): Input DataFrame.
        feature (str): Categorical feature to plot on the x-axis.
        title (str): Plot title (default: "").
        hue (str): Optional column for hue grouping.
        color_palette (list): Optional list of colors for the palette.
        save_path (str): If provided, saves the figure to this file path.

    Returns:
        None
    """
    if color_palette is None:
        color_palette = color_list   

    fig, ax = plt.subplots(1, 1, figsize=(8, 4))
    
 
    if hue:
        counts = data_df.groupby([feature, hue]).size().reset_index(name='count')
        sns.barplot(x=feature, y='count', hue=hue, data=counts, palette=color_palette, ax=ax)
    else:
        sns.countplot(x=feature, data=data_df, palette=color_palette, ax=ax)

    ax.set_title(title or f"Count plot for '{feature}'")
    ax.set_xlabel(feature)
    ax.set_ylabel("Count")
    ax.grid(color="black", linestyle="-.", linewidth=0.5, axis="y", which="major")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
    else:
        plt.show()

def plot_distribution_pairs(data_df, feature, title="", hue=None, color_palette=None, save_path=None):
    """
    Plots a histogram of a numerical feature, optionally grouped by a hue.

    Parameters:
        data_df (pd.DataFrame): Input DataFrame.
        feature (str): Numerical feature to plot on the x-axis.
        title (str): Plot title (default: "").
        hue (str): Optional column for hue grouping.
        color_palette (list): Optional list of colors for each hue class.
        save_path (str): If provided, saves the figure to this file path.

    Returns:
        None
    """
    if color_palette is None:
        color_palette = color_list

    fig, ax = plt.subplots(1, 1, figsize=(8, 4))

    if hue:
        unique_hues = data_df[hue].dropna().unique()
        for i, h in enumerate(unique_hues):
            sns.histplot(
                data_df.loc[data_df[hue] == h, feature],
                color=color_palette[i % len(color_palette)],
                ax=ax,
                label=str(h),
                kde=False
            )
        ax.legend(title=hue)
    else:
        sns.histplot(data_df[feature], color=color_palette[0], ax=ax, kde=False)

    ax.set_title(title or f"Distribution of '{feature}'")
    ax.set_xlabel(feature)
    ax.set_ylabel("Frequency")
    ax.grid(color="black", linestyle="-.", linewidth=0.5, axis="y", which="major")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
    else:
        plt.show()

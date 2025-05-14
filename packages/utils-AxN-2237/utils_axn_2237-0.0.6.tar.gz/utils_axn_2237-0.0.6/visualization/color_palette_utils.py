from matplotlib.colors import ListedColormap
import seaborn as sns
import matplotlib.pyplot as plt

def set_color_map(color_list):
    """
    Creates and shows a custom color palette, returns the corresponding ListedColormap.

    Parameters:
        color_list (list): List of color hex codes.

    Returns:
        ListedColormap: Custom matplotlib color map.
    """
    cmap_custom = ListedColormap(color_list)
    print("Notebook Color Schema:")
    sns.palplot(sns.color_palette(color_list))
    plt.show()
    return cmap_custom

def get_default_color_map():
    default_colors = ["#A5D7E8", "#576CBC", "#19376D", "#0b2447"]
    return set_color_map(default_colors)

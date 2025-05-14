import matplotlib.pyplot as plt

def plot_correlation_matrix(df, figsize=(10, 8), cmap='coolwarm', annot=True):
    """
    Plots a correlation matrix heatmap for a given pandas DataFrame.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        figsize (tuple): Size of the plot (width, height).
        cmap (str): Colormap for the heatmap.
        annot (bool): Whether to annotate the heatmap with correlation coefficients.
    """
    # Compute the correlation matrix
    corr = df.corr()

    # Create the heatmap plot
    plt.figure(figsize=figsize)
    sns.heatmap(corr, annot=annot, cmap=cmap, fmt=".2f", square=True, linewidths=0.5)
    plt.title("Correlation Matrix Heatmap", fontsize=16)
    plt.tight_layout()
    plt.show()

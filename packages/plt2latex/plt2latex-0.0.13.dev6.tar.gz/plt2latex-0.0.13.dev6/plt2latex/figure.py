import matplotlib

def set_figsize(width_pt: float, height_pt: float):
    """
    Sets the default figure size.

    Args:
        width_pt (float): Width in LaTeX points.
        height_pt (float): Height in LaTeX points.

    Example:
        >>> set_figsize(400, 300)
    """
    width_in = width_pt/72
    height_in = height_pt/72
    matplotlib.rcParams.update({'figure.figsize': (width_in, height_in)})

def set_font(fontsize: int = 12):
    """
    Sets the default font size for all elements in the figure.

    Args:
        fontsize (int): Font size in points.

    Example:
        >>> set_font(14)
    """
    matplotlib.rcParams.update({
        'legend.title_fontsize': fontsize,
        'font.size': fontsize,
        'axes.titlesize': fontsize,
        'axes.labelsize': fontsize,
        'xtick.labelsize': fontsize,
        'ytick.labelsize': fontsize,
        'legend.fontsize': fontsize,
        'figure.titlesize': fontsize,
    })
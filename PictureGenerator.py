from typing import Union, Tuple
import os
import matplotlib.pyplot as plt


def to_inline_expr(math_expr: str) -> str:
    """
    Convert a LaTeX math expression to an inline math expression.

    Parameters
    ----------
    math_expr : str
        The LaTeX math expression to convert.

    Returns
    -------
    str
        The converted inline math expression.
    """
    return '$' + math_expr + '$'


def latex_to_image(math_expr: str, file_name: str, location: str, file_format: str = 'png',
                   picture_dims: Union[str,Tuple[float,float]] = 'A4',
                   resolution: Union[float, int] = 300, transparent: bool = True) -> None:
    """
    Converts a LaTeX math expression to an image in the specified file format and saves it with the specified file name.

    Args:
        math_expr (str): The LaTeX math expression to be converted to an image.
        file_name (str): The name of the file to be saved.
        file_format (str, optional): The format of the output file. Defaults to 'png'.
        picture_dims (Union[str,Tuple[float,float]], optional): The dimensions of the output picture. Can be either a
                                                               string specifying one of the standard dimensions (Letter,
                                                               Legal, A4, A5) or a tuple of the form (width, height).
                                                               Defaults to 'A4'.
        resolution (Union[float, int], optional): The resolution of the output image in DPI (dots per inch). Defaults to 300.
        transparent (bool, optional): Whether to save the image with a transparent background. Defaults to True.

    Raises:
        ValueError: If picture_dims is not one of the standard dimensions (Letter, Legal, A4, A5).
    """

    # Standard square dimensions of output picture
    std_dims = {"Letter":(8.5,14.0), "Legal":(8.5,14.0),
                "A4":(8.3,11.7), "A5":(5.8, 8.3)}

    if picture_dims in list(std_dims.keys()):
        DIMS = std_dims[picture_dims]
    else:
        raise ValueError(f"{picture_dims} not known - should be in: {list(std_dims.keys())}.")

    # Create the download directory if it doesn't exist
    if not os.path.exists(location):
        # Notify the user that the download directory was created
        print(f"N.B.: Path '{location}' didn't already exist, so it was created... ")
        os.makedirs(location)

    # Set the LaTeX font
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

    # Add $ symbols to format the string as an inline math expression
    inline_expr = to_inline_expr(math_expr=math_expr)

    # Create a plot with the expression
    fig, ax = plt.subplots(figsize=DIMS)
    ax.text(0.5, 0.5, inline_expr, size=20, ha='center')

    # Remove the plot axes
    ax.set_axis_off()

    # Save the plot as a PNG with a transparent background
    plt.savefig(fname=location+file_name+"."+file_format, format=file_format, transparent=transparent, bbox_inches='tight', pad_inches=0.0, dpi=resolution)
    plt.close(fig)


def render_and_show(math_expr: str) -> None:
    """
    Renders the given LaTeX math expression as an inline math expression in a plot using matplotlib, and displays the plot.

    Args:
        math_expr: A string representing the LaTeX math expression to be rendered.

    Returns:
        None
    """
    # Set the LaTeX font
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

    # Add $ symbols to format the string as an inline math expression
    inline_expr = to_inline_expr(math_expr=math_expr)

    # Create a plot with the expression
    fig, ax = plt.subplots(figsize=(4.0, 4.0))
    ax.text(0.5, 0.5, inline_expr, size=20, ha='center')

    # Remove the plot axes
    ax.set_axis_off()

    # Show plot
    plt.show()


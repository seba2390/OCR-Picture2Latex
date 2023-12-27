from typing import Union, List, Tuple
import subprocess
import os.path
import re

from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


def is_valid_latex_math(expr: str) -> bool:
    """Check whether a given string is a valid LaTeX math expression.

        N.B. Notice 'amsmath' is included as it is also used
        when saving .png pictures w. matplotlib
    Args:
        expr: A string representing a LaTeX math expression.

    Returns:
        A boolean indicating whether the expression is valid.

    Raises:
        None.

    Example:
        >>> expr = r'\frac{1}{2} + \sqrt{3}'
        >>> is_valid_latex_math(expr)
        True
    """
    try:
        # Create a LaTeX document with the expression inside a math environment
        input_str = f'\\documentclass{{article}}\\usepackage{{amsmath}}\\usepackage{{physics}}\\begin{{document}} {expr} \\end{{document}}'
        # Compile the LaTeX document using pdflatex with batchmode and halt-on-error options
        output = subprocess.check_output(['pdflatex', '-halt-on-error', '-interaction=batchmode'],
                                         input=input_str.encode(), stderr=subprocess.STDOUT)
        # If there is no error, return True
        return True
    except subprocess.CalledProcessError as e:
        # Print the output of the command for debugging purposes
        # If there is an error, return False
        return False



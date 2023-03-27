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
        input_str = f'\\documentclass{{article}}\\usepackage{{amsmath}}\\begin{{document}}$ {expr} $\\end{{document}}'
        # Compile the LaTeX document using pdflatex with batchmode and halt-on-error options
        subprocess.check_output(['pdflatex', '-halt-on-error', '-interaction=batchmode'], input=input_str.encode(), stderr=subprocess.STDOUT)
        # If there is no error, return True
        return True
    except subprocess.CalledProcessError as e:
        # If there is an error, return False
        return False


def filter_formulas(in_filename: str, nr_equations: int, seed: int = 1) -> List[str]:
    """
    Reads a file containing LaTeX formulas from 'in_filename' and removes all
    occurrences of the '\label{...}' substring from each formula. Each formula is
    separated by two newline characters.

    Parameters:
        in_filename : str
            The name of the input file containing LaTeX formulas.
        nr_equations : int
            The number of equations to choose from the input file.

    Returns:
        List[str] or None:
            The function returns a list of the filtered formulas if successful.
            Returns None if there is an error.

    Raises:
        FileNotFoundError:
            If the input file does not exist.
        IOError:
            If the input file cannot be opened for reading.
        Exception:
            If the specified number of equations to choose is greater than the number of available equations in the input file.
    """

    def contains_only_digits_and_backslashes(string):
        # Remove whitespace characters
        string = re.sub(r'\s', '', string)
        # Check if string only contains digits and backslashes
        return bool(re.match(r'^[0-9\\\\]+$', string))

    # Setting seed for numpy RNG
    np.random.seed(seed)

    # Check if the input file exists
    if not os.path.isfile(in_filename):
        raise FileNotFoundError(f"File not found: {in_filename}")

    # Importing initial formulas
    with open(in_filename, 'r', encoding='ISO-8859-1') as f:
        formulas = [line.strip() for line in f.readlines()]

    # Check if the number of equations to choose is greater than the number of available equations
    if nr_equations > len(formulas):
        raise Exception(f'{nr_equations} equations requested, but only {len(formulas)} available in file: {in_filename}')
    else:
        # Choose a random sample of equations without replacement
        formulas = np.random.permutation(formulas).tolist()

    # Define a regular expression pattern to match \label{...}, %, $, \nonumber and & substrings
    pattern = re.compile(r'(\\label\{.*?\}|%|\$|\\nonumber|&)')

    # Remove the \label{...}, % and $ substring from each string in the 'formulas' list
    first_filtering = [re.sub(pattern, "", s) for s in formulas]

    # Remove strings that local latex engine doesn't recognize as genuine latex math
    final_filtering = []
    for idx in tqdm(range(int(len(first_filtering[:nr_equations])*1.1))):
        if len(final_filtering) < nr_equations:
            if is_valid_latex_math(first_filtering[idx]):
                # Don't want string if all characters are whitespace characters, such as spaces, tabs, and line breaks
                s = first_filtering[idx]
                if not s.isspace() and s != '' and not contains_only_digits_and_backslashes(s):
                    final_filtering.append(s)
        else:
            break

    # Return the final filtered list of formulas
    return final_filtering


def save_filtered_formulas(filtered_formulas: List[str], out_filename: str) -> None:
    """
    Saves the filtered formulas to a file.

    Args:
        filtered_formulas: A list of filtered formulas to be saved.
        out_filename: The name of the output file.

    Returns:
        None
    """

    # Open the output file and write the filtered formulas to it
    with open(out_filename, 'w') as f:
        for line in filtered_formulas:
            # Write each formula to a new line and add a blank line after it
            f.write(line+'\n')


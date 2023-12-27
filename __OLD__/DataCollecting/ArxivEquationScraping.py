import os
import re
import subprocess
import shutil
from datetime import datetime
from typing import List

import requests
import tarfile
from bs4 import BeautifulSoup
from tqdm import tqdm


def math_scraper(input_names: List[str], output_name: str) -> List[str]:
    """
    Reads the input LaTeX file and extracts all equations environments. All equations
    are written to the output file, with each math environment on a separate line.
    All equations are returned as list of strings.

    Args:
        input_names (List[str]): A list of the names of the input LaTeX files.
        output_name (str): The name of the output text file.

    Returns:
        formatted_equations (List[str]): A list of strings, where each string corresponds a latex math equation.

    Example Usage:
        >>> math_scraper(['input1.tex', 'input2.tex'], 'output.txt')
    """

    # Define the regular expressions to match and remove \nonumber, \label{} and % tokens
    nonumber_regex = r'\\nonumber'
    label_regex = r'\\label{.*?}'
    bm_regex = r'\\bm'
    prct_rexeg = r'%'

    def remover(math_str: str) -> str:
        # Remove \nonumber tokens
        _math_str = re.sub(nonumber_regex, '', math_str)
        # Remove \label{} tokens and their contents
        _math_str = re.sub(label_regex, '', _math_str)
        # Remove % tokens and their contents
        _math_str = re.sub(prct_rexeg, '', _math_str)
        # Removing explicit \bm toke
        _math_str = re.sub(bm_regex, '', _math_str)
        # Removing explicit \n chars
        _math_str = _math_str.replace('\n', '')
        # Adding space to after special chars like \circ
        _math_str = _math_str.replace('\circ', '\circ ')
        return _math_str

    # Define the regular expression to match and extract '\begin{equation}' type fields
    equation_regex = r'\\begin{equation}(.*?)\\end{equation}\s*'
    equation_start_token = r'\begin{equation}'
    equation_end_token = r'\end{equation}'

    # Open the output file for writing
    formatted_equations = []
    with open(output_name, 'w') as output_file:
        # Find matches within each input file and write them to the output file
        for idx in tqdm(range(len(input_names))):
            input_name = input_names[idx]
            with open(input_name, 'r') as input_file:
                try:
                    # Read .tex file contents
                    input_contents = input_file.read()
                    # Use regex to find all '\begin{equation}' type fields
                    equation_fields = re.findall(equation_regex, input_contents, re.DOTALL)
                    for math_equation in equation_fields:
                        # Removing unwanted tokens
                        math_equation = remover(math_str=math_equation)
                        # Putting start and end tokens back
                        math_equation = math_equation#equation_start_token + math_equation + equation_end_token
                        # Saving equation
                        formatted_equations.append(math_equation)
                        # Writing equation to file
                        output_file.write(math_equation+'\n')
                except UnicodeDecodeError:
                    print(f"Error: File {input_name} cannot be decoded - skipping..")
                    continue

            input_file.close()
    output_file.close()
    with open(output_name, 'r') as f:
        lines = f.read().split('\n')
        num_lines = len(lines)
        print(f"==== Scraped: {num_lines} equations, and saved to: {output_name} ====")
    f.close()
    return formatted_equations


def move_files_to_parent(download_directory: str) -> None:
    # Walk through the subdirectories and move the files to the parent directory
    for root, dirs, files in os.walk(download_directory):
        for file in files:
            # Get the full path of the file and the destination path in the parent directory
            src_path = os.path.join(root, file)
            dst_path = os.path.join(download_directory, file)

            # If the file already exists in the parent directory, add a number to the filename
            if os.path.exists(dst_path):
                i = 1
                while os.path.exists(os.path.join(download_directory,
                                                  f"{os.path.splitext(file)[0]}_{i}{os.path.splitext(file)[1]}")):
                    i += 1
                dst_path = os.path.join(download_directory,
                                        f"{os.path.splitext(file)[0]}_{i}{os.path.splitext(file)[1]}")

            # Move the file to the parent directory
            shutil.move(src_path, dst_path)

    # Delete empty subdirectories (The topdown=False argument ensures that the function deletes empty directories from the bottom up, so that it doesn't try to delete a directory that still contains files.)
    for root, dirs, files in os.walk(download_directory, topdown=False):
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))


def unpack_tex_files(download_directory: str) -> None:
    """
    Deletes all files in the specified directory that are not '.tex' files or compressed '.pdf' files containing '.tex' files.
    Extracts all '.tex' files from compressed '.tar.gz' or '.tar' files to the specified directory.

    Args:
        download_directory: The path of the directory containing the downloaded files.

    Raises:
        subprocess.CalledProcessError: If the 'file' command fails to execute properly.

    """
    file_names = os.listdir(path=download_directory)

    for idx, filename in enumerate(file_names):
        if filename[-4:] != ".tex":
            print(f" ===== Handling file nr: {idx + 1} with id: {filename} =====")
            full_filename = os.path.join(download_directory, filename)
            file_type_info_list = subprocess.check_output(["file", full_filename]).decode().strip().split()
            file_removed = False

            # If file_type_info_list contains 'PDF', file is either a '.pdf' or a compressed '.pdf' file.
            # We want only '.tex' files, so we delete it.
            if "PDF" in file_type_info_list:
                print(f" Deleting file nr: {idx + 1} with id: {filename} - no '.tex' file found...")
                file_removed = True
                os.remove(full_filename)

            # If file_type_info_list contains 'gzip' and 'compressed', file is a compressed '.tar.gz' file.
            # We extract all '.tex' files to the specified directory and delete the original file.
            elif "gzip" in file_type_info_list and "compressed" in file_type_info_list:
                try:
                    tar = tarfile.open(full_filename, 'r:gz')
                    file_types = [os.path.splitext(os.path.basename(member.name))[1] for member in tar.getmembers()]
                    tar.close()
                    if ".tex" not in file_types:
                        print(f" Deleting file nr: {idx + 1} with id: {filename} - no '.tex' file found...")
                        file_removed = True
                        os.remove(full_filename)
                    else:
                        print(f" File nr: {idx + 1} with id: {filename} - contains '.tex' file: ")
                        tar = tarfile.open(full_filename, 'r:gz')
                        # Doing the following to make sure that no pre-existing file(s) in 'download_directory'
                        # is(are) overwritten if it(they) has(have) the same name.
                        tex_members = [m for m in tar.getmembers() if os.path.splitext(m.name)[1] == ".tex"]
                        for member in tex_members:
                            extracted_name = member.name
                            counter = 0
                            while os.path.exists(os.path.join(download_directory, extracted_name)):
                                counter += 1
                                extracted_name = f"{os.path.splitext(member.name)[0]}_{counter}.tex"
                            print(f"Extracting {member.name} as {extracted_name}")
                            member.name = extracted_name
                            tar.extract(member, path=download_directory)
                        tar.close()
                except tarfile.TarError as e:
                    print(f"{e} - file nr: {idx + 1} with id: {filename} skipped and deleted...")
                    os.remove(full_filename)

            # If file_type_info_list contains 'tar', 'POSIX' and 'archive', file is a '.tar' file.
            # We extract all '.tex' files to the specified directory and delete the original file.
            elif "tar" in file_type_info_list and "POSIX" in file_type_info_list and "archive" in file_type_info_list:
                try:
                    tar = tarfile.open(full_filename, 'r:')
                    file_types = [os.path.splitext(os.path.basename(member.name))[1] for member in tar.getmembers()]
                    tar.close()
                    if ".tex" not in file_types:
                        print(f" Deleting file nr: {idx + 1} with id: {filename} - no '.tex' file found...")
                        file_removed = True
                        os.remove(full_filename)
                    else:
                        print(f" File nr: {idx + 1} with id: {filename} - contains '.tex' file: ")
                        tar = tarfile.open(full_filename, 'r:')
                        # Doing the following to make sure that no pre-existing file(s) in 'download_directory'
                        # is(are) overwritten if it(they) has(have) the same name.
                        tex_members = [m for m in tar.getmembers() if os.path.splitext(m.name)[1] == ".tex"]
                        for member in tex_members:
                            extracted_name = member.name
                            counter = 0
                            while os.path.exists(os.path.join(download_directory, extracted_name)):
                                counter += 1
                                extracted_name = f"{os.path.splitext(member.name)[0]}_{counter}.tex"
                            print(f"Extracting {member.name} as {extracted_name}")
                            member.name = extracted_name
                            tar.extract(member, path=download_directory)
                        tar.close()
                except tarfile.TarError as e:
                    print(f"{e} - file nr: {idx + 1} with id: {filename} skipped an deleted...")
                    os.remove(full_filename)
            # Always remove original after.
            if not file_removed:
                os.remove(full_filename)

    # Move files from created sub-folders to parent folder
    move_files_to_parent(download_directory=download_directory)


def download_arxiv_papers(category: str, num_papers: int, download_dir: str) -> None:
    """
    Downloads STEM (Science, Technology, Engineering and Math) category arXiv papers in the specified category and saves them to the specified directory.

    Parameters:
        category (str): The arXiv category to download papers from.
        num_papers (int): The number of papers to download.
        download_dir (str): The directory to save the downloaded papers to.

    Returns:
        None.
    """
    # Physics, Mathematics, Computer Science, Quantitative biology, Electrical Engineering and Systems Science
    # Quantitative finance, Economics, Statistics
    STEM = ['physics','math', 'cs', 'eess', 'q-bio', 'q-fin', 'econ', 'stat']
    if category not in STEM:
        raise Exception(f'Category: {category} is not in the defined STEM categories: {STEM}')

    # Create the download directory if it doesn't exist
    if not os.path.exists(download_dir):
        # Notify the user that the download directory was created
        print(f"N.B.: Path '{download_dir}' didn't already exist, so it was created... ")
        os.makedirs(download_dir)

    # Request the arXiv category page and parse it with BeautifulSoup
    # Get the current date and time
    now = datetime.now()
    # Format the date as YY/MM
    current_formatted_date = now.strftime("%y%m")

    # Construct the URL of the arXiv category page for the current date and specified category
    url = f"https://arxiv.org/list/{category}/{current_formatted_date}"
    # Send an HTTP request to the URL and get the response
    response_1 = requests.get(url)
    # Parse the HTML content of the response with BeautifulSoup
    soup = BeautifulSoup(response_1.content, 'html.parser')
    # Construct a regular expression that matches links to the arXiv category page for the current date and specified category
    regex = re.compile(re.escape(f'/list/{category}/{current_formatted_date}'))
    # Find all links on the page that match the regular expression
    links = soup.find_all('a', href=regex)
    link = None
    # Loop over the links and find the link with the text ">all</a>"
    for l in links:
        if str(l)[-8:] == ">all</a>":
            link = l
    # Send an HTTP request to the URL of the page that contains links to individual papers in the category
    response_2 = requests.get(url+link['href'])
    # Parse the HTML content of the response with BeautifulSoup
    soup = BeautifulSoup(response_2.content, 'html.parser')

    # Extract the links to the individual papers from the page
    paper_links = soup.find_all('a', title='Abstract')

    # Raise an exception if the number of papers requested is greater than the number of papers available
    if num_papers > len(paper_links):
        raise Exception(f"{num_papers} papers requested, but only: {len(paper_links)} available in category: '{category}' in YY/MM: {current_formatted_date} ...")
    else:
        # Notify the user of the number of papers being downloaded
        print(f"======= Downloading: {num_papers} (out of {len(paper_links)}) papers in category: '{category}' in YY/MM: {current_formatted_date} =======")

    # Loop over the paper links and download the source files for each paper
    for i, link in enumerate(paper_links):
        if i >= num_papers:
            break

        # Get the URL of the paper page
        paper_url = "https://arxiv.org" + link['href']

        # Extract the paper ID from the URL
        paper_id = paper_url.split('/')[-1]

        # Construct the URL of the source files
        source_url = f"https://arxiv.org/e-print/{paper_id}"

        print("Downloading paper: ", i+1, " with id: ", paper_id, " ...")
        # Download the source files and save them to the download directory
        response_3 = requests.get(source_url)

        with open(download_dir+str(paper_id), "wb") as f:
            f.write(response_3.content)
        f.close()

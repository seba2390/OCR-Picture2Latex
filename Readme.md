## OCR-Picture2Latex 
Repository currently consists of:
- DataCollecting/ArxivEquationFiltering.py: A collection of functions that utilizes python std. libs and 'BeautifulSoup' to scrape ArXiv for STEM (Science, Technology, Engineering & Mathematics) papers and extract any available .tex file.
- DataCollecting/EquationFiltering.py: Utilizes Regular Expressions (Regex) to extract equations from math fields in .tex files and remove characters, to enable local rendering of corresponding .png.
- DataCollecting/PictureGenerator.py: Transforms any Python string representation of valid Latex math into transparent .png files, to use as labels for ML. 

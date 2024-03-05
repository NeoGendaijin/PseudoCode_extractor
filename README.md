# Pseudocode Extractor

Pseudocode Extractor is a tool designed to extract pseudocode from academic papers in PDF format, displaying both the content and the number of pseudocode snippets found.

## Installation Instructions

To use this project, please follow the steps below:

1. Clone this repository.
   ```
   git clone https://github.com/NeoGendaijin/PseudoCode_extractor.git
   cd PseudoCode_extractor
   ```

2. Install the required Python packages.
   ```
   pip install -r requirements.txt
   ```


### How to Use

`quick_start.py` is a script designed to extract pseudocode from a PDF file and display the number and content of the pseudocode snippets. Below is how to use this script.

First, place the PDF you want to extract from into the `./PDF/` directory (for example, `pseudocode.pdf`). Then, run the following command:

```bash
python quick_start.py
```

The main code of `quick_start.py` is as follows:

```python
from src.main import process_paper, find_peudo_code

# How to use
path_to_paper = "./PDF/pseudocode.pdf"

count, pseudo_codes_list = find_peudo_code(path_to_paper,0.6) # put your path and confidence level

print(f"A number of pseudocode: {count}")

for i, pseudo_code in enumerate(pseudo_codes_list):
    print(f"\n\n\nPseudocode {i+1}:")
    print(pseudo_code)
```

This script will display the number of pseudocode snippets within the specified PDF file and the content of each pseudocode snippet. The `find_peudo_code` function analyzes the PDF, identifies pseudocode snippets, and returns them as a list. From this list, you can easily review the number and content of the pseudocode snippets.

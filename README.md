# Invoice Parser

This Python script is designed to parse invoice PDF files and extract item information from them. It renames the invoice PDF files, parses the content, and generates a new PDF file with the extracted item information.

## Features

- Parses invoice PDF files to extract item information
- Renames the invoice PDF files for better organization
- Generates a new PDF file with the extracted item information
- Saves the extracted item data in a JSON file for further analysis or processing

## Usage

1. Place all the invoice PDF files in the same folder as this script.

2. **Optional:** If you want to specify a different folder, provide the path to the folder when prompted.

3. Run the script: Open a terminal or command prompt, navigate to the directory containing the script, and run the script.

```
python invoice_parser.py
```

4. Follow the on-screen instructions: The script will prompt you to enter the path to the folder containing the invoice PDF files. Press enter to use the current directory.

5. Results: The script will parse the invoice PDF files, extract the item information, rename the invoice PDF files, and generate a new PDF file with the extracted information. It will also save the extracted item data in a `items_data.json` file.

## Dependencies

- `pdfplumber` library: Used to extract text from PDF files.
- `reportlab` library: Used to generate new PDF files.

Make sure to install the dependencies by running the following command:
```
pip install pdfplumber reportlab
```

## Note

Invoice Parser has been built into an executable as well in the ```dist``` directory.


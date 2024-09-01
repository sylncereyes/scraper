# Directory Scanner

This Python script scans a given website URL to find and list all directories (URLs) present on that website. The script eliminates duplicate URLs, even if they differ due to language paths like `/en/` or `/id/`.

## Features

- Recursively scans directories within a website.
- Eliminates duplicate URLs, considering variations like language paths or trailing slashes.
- Outputs results either to the console or to a specified output file.
- Provides an option to only list URLs without additional output.

## Requirements

To run this script, you need to have Python installed on your system along with the following Python packages:

- `requests`
- `beautifulsoup4`
- `lxml`

### Installation

You can install the required packages using `pip`:

```bash
pip install requests beautifulsoup4 lxml

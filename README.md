# Kindle Clipper
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Unlicense](https://img.shields.io/badge/License-Unlicense-blue.svg)](https://unlicense.org/)

**Kindle Clipper** processes Kindle clippings and organizes them into separate files for each book. It reads Kindle's `My Clippings.txt` file and a template file to generate the output files with user-defined formatting. The template file can be of any extension of your choice. The clippings are saved in a specified `books/` folder in the same directory as the clippings file.

## Installation

Just download the script from this repository.

## Usage

```
python kindleclipper.py <clippings_file> <template_file>
```
The directory containing the `clippings_file` is going to look like this:
```
path/to/clippings/
│
├── My Clippings.txt
│
└── books/
    ├── Book One.md
    ├── Book Two.md
    └── Book Three.md

```
The `template_file` doesn't have to be in the same folder as the `clippings_file`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[Unlicense](UNLICENSE)

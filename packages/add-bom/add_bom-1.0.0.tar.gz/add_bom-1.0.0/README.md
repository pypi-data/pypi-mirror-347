# add-bom

A simple command-line utility to add a UTF-8 BOM (Byte Order Mark) to files. This is particularly useful for CSV files that need to be opened correctly in Excel on macOS, where files without a BOM might be interpreted with incorrect character encoding.

## Installation

The recommended way to install this tool is using `pipx`:

```bash
pipx install add-bom
```

## Usage

```bash
add-bom <file>
```

### Options

- `--force`: Force add BOM to file regardless of current encoding

### Examples

Add BOM to a UTF-8 CSV file:
```bash
add-bom data.csv
```

Force add BOM to a file (use with caution):
```bash
add-bom data.csv --force
```

## What is a BOM?

A BOM (Byte Order Mark) is a special character sequence at the beginning of a text file that indicates the encoding of the file. For UTF-8 files, the BOM is the sequence `EF BB BF` in hexadecimal.

## Why is this needed?

When opening CSV files in Excel on macOS, files without a BOM might be interpreted with incorrect character encoding (like MacRoman or Windows-1252), leading to garbled text. Adding a UTF-8 BOM ensures that Excel correctly recognizes the file as UTF-8 encoded.

## Safety Features

The tool includes several safety checks:
- Verifies the file exists
- Checks if the file already has a BOM
- By default, only adds BOM to files that are already UTF-8 encoded
- Requires `--force` flag to add BOM to files with other encodings

## License

MIT License - See LICENSE file for details

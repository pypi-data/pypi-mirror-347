# q2numfmt

[![PyPI version](https://img.shields.io/pypi/v/q2numfmt.svg)](https://pypi.org/project/q2numfmt/)
[![License](https://img.shields.io/github/license/AndreiPuchko/q2numfmt.svg)](https://github.com/AndreiPuchko/q2numfmt/blob/main/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/q2numfmt.svg)](https://pypi.org/project/q2numfmt/)

**q2numfmt** is a lightweight Python package for formatting numeric data using Excel-style number format strings. It follows the [ECMA-376 - Office Open XML file formats - 5th edition, December 2021](https://ecma-international.org/publications-and-standards/standards/ecma-376/) specification—the same standard used by Microsoft Excel to format numbers.

## Features

- Format integer, float, string, or `Decimal` values.
- Supports custom Excel-like format strings (e.g. `"0.00"`, `"0%"`, `"$#,##0.00"`).
- Implements rules from ECMA-376 Part 1, Section 18.8.31 (`numFmts`).
- No external dependencies.
- Ideal for spreadsheet tools, reports, exports, and other data presentation needs.

## Installation

```bash
pip install q2numfmt
```

## Usage

```python
from q2numfmt import format_number

print(format_number(1234.567, "#,##0.00"))     # "1,234.57"
print(format_number("0.056", "0.0%"))          # "5.6%"
print(format_number(-1234.5, "$#,##0.00"))     # "-$1,234.50"
print(format_number(0, '[Green]0.00;[Red]-0.00'))  # "0.00"
```

## API

format_number(value, format_string)

Formats a number using an Excel-style number format string.

    value: int, float, str, or decimal.Decimal

    format_string: A string format as defined in Excel / ECMA-376

Returns a str with the formatted result.


## Example Format Strings

Format String	Input	Output
0.00	12.3	12.30
#,##0	12345	12,345
0.0%	0.1234	12.3%
$#,##0.00	-1234.5	-$1,234.50
[Red]-0.0	-5.5	-5.5


## Specification

The package is based on:

    ECMA-376-1:2016, Part 1 – Office Open XML File Formats

    Section 18.8.31: numFmts (Custom Number Formats in Excel)

## License

This project is licensed under the MIT License – see the [LICENSE]() file for details.

## Links

    📦 PyPI: https://pypi.org/project/q2numfmt

    🧑‍💻 GitHub: https://github.com/AndreiPuchko/q2numfmt

## Author

Andrei Puchko
GitHub: https://github.com/AndreiPuchko

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.
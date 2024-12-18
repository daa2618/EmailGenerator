# EmailGenerator
Generates an email address based on person's name, a specified email format and the domain

# Python Script for Generating Email Addresses

This Python script generates email addresses based on a specified format and a person's name. It offers flexibility in how names are represented (initials or first few letters) and handles separators between name parts.

## Functionality

* Splits a person's name into first, middle, and last names.
* Extracts format elements and separators from an email format string.
* Generates a new email format based on a given word and a list of existing formats.
* Constructs an email address based on a specified format using parts of a person's name.

## Usage

This script can be used as a standalone tool or imported as a module in other Python projects.

**1. Standalone Usage**

The script will prompt you to enter a name, email format, and domain. It will then print the generated email address to the console.

**2. Module Usage**

```python
import emailGenerator

name = "John Doe"
email_format = "[first_initial].[last]"
domain = "@example.com"

email_address = emailGenerator.generateEmailString(name, email_format, domain)

print(email_address)  # Output: [jdoe@example.com]
```

## Features
Supports various name representations: first name, last name, initials, and first/last few letters.
Handles separators between name parts in the email format.
Provides flexibility in specifying the desired level of detail for each name part.
## Error Handling
The script handles potential errors such as:

Names that cannot be split into first, middle, and last names.
Missing middle names when the format specifies a middle name placeholder.
Malformed email format strings.
## Dependencies
This script does not require any external libraries.

## Contributing
I welcome contributions to this project. Feel free to submit pull requests with improvements or additional features.

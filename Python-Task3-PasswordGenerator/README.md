# OIBSIP Task 3 – Random Password Generator

## Objective

Build a Python tool that generates strong, random passwords based on
user-defined criteria.

This project implements the Advanced Tier of the OIBSIP Random Password
Generator task with a graphical user interface, secure password
generation, password strength feedback, clipboard integration, and
session-based password history.

## Tech Stack

- Python
- Tkinter
- secrets
- string
- pyperclip

## Beginner Tier Features

- [x] Prompt user to specify the desired password length
- [x] Enforce a minimum password length of 8 characters
- [x] Allow selection of uppercase letters
- [x] Allow selection of lowercase letters
- [x] Allow selection of numbers
- [x] Allow selection of symbols
- [x] Require at least 2 character types to be selected
- [x] Generate and display a password matching the selected criteria
- [x] Validate invalid password lengths
- [x] Validate when insufficient character types are selected
- [x] Allow users to generate another password without restarting

## Advanced Tier Features

- [x] GUI window built using Tkinter
- [x] Password length control using a Spinbox
- [x] Character type selection using checkboxes
- [x] Cryptographically secure password generation using the `secrets` module
- [x] Password strength indicator with Weak, Medium, and Strong levels
- [x] Guarantee at least one character from every selected character type
- [x] Copy to Clipboard functionality using `pyperclip`
- [x] Automatically copy the generated password to the clipboard
- [x] Option to exclude ambiguous characters
- [x] Display the last 5 generated passwords during the current session
- [x] Password history is not persisted to a file for security

## Character Types

The application supports four character types:

- Lowercase letters: `a-z`
- Uppercase letters: `A-Z`
- Numbers: `0-9`
- Symbols

At least two character types must be selected before generating a
password.

## Password Length

The minimum password length is 8 characters.

The GUI provides a Spinbox that allows the user to select a password
length from 8 to 128 characters.

## Secure Password Generation

The application uses Python's `secrets` module instead of the
`random` module for password generation.

The `secrets` module provides cryptographically secure random values
suitable for generating passwords.

The generated password is also securely shuffled using the `secrets`
module.

## Security Rules

The application guarantees that at least one character from every
selected character type is included in the generated password.

For example, if the user selects:

- Uppercase
- Lowercase
- Numbers
- Symbols

the generated password will contain at least one character from each
of those four categories.

## Password Strength Indicator

The application displays a password strength label based on password
length and character diversity.

The available strength levels are:

- Weak
- Medium
- Strong

## Copy to Clipboard

The application provides a **Copy to Clipboard** button using the
`pyperclip` library.

The generated password is also automatically copied to the clipboard
when a password is generated.

## Ambiguous Character Exclusion

The application provides an option to exclude visually similar
characters.

Examples include:

```text
0
O
1
l
I

This option can make generated passwords easier to read and manually
enter.

Generation History

The application displays the last 5 generated passwords during the
current application session.

The password history is stored only in memory and is not written to a
file or database.

This prevents passwords from being permanently stored by the
application.

Input Validation

The application validates:

Password length
Minimum length of 8 characters
Character type selection
At least 2 character types selected
Availability of selected character sets when ambiguous characters
are excluded

Helpful error messages are displayed when invalid options are selected.

Installation

Clone the OIBSIP repository:

git clone https://github.com/prudviraj12345/OIBSIP.git

Navigate to the Task 3 folder:

cd OIBSIP/Python-Task3-PasswordGenerator

Install the required dependency:

pip install -r requirements.txt
Requirements

The requirements.txt file contains:

pyperclip

Tkinter, secrets, and string are provided by the Python standard
library.

How to Run

Run the application using:

python password_generator.py

A graphical password generator window will open.

Basic Usage
Select the password length.
Select at least two character types.
Optionally enable ambiguous-character exclusion.
Click Generate Secure Password.
View the generated password.
Check the password strength.
The generated password is automatically copied to the clipboard.
Use Copy to Clipboard when required.
View the last 5 generated passwords in the current session.
Project Structure
Python-Task3-PasswordGenerator/
│
├── password_generator.py
├── requirements.txt
└── README.md
Security Considerations

The application uses Python's secrets module instead of random for
cryptographically secure password generation.

Generated passwords are not permanently stored.

Only the last 5 generated passwords are temporarily maintained during
the current application session.

Password history is not saved to a file or database.

Users should avoid sharing generated passwords and should use unique
passwords for different accounts.

References

The project follows the resources suggested in the OIBSIP task
guidelines:

Python password generator tutorials
Python Tkinter GUI tutorials
Python secrets module documentation
Python pyperclip tutorials
Project Information

Program: OIBSIP – Python Programming

Task: Task 3 – Random Password Generator

Implementation: Advanced Tier

Technologies: Python, Tkinter, secrets, pyperclip
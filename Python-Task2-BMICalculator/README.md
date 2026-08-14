# OIBSIP Task 2 – BMI Calculator

## Objective

Build a Python program that calculates a user's Body Mass Index (BMI)
and classifies it into standard health categories.

This project implements the Advanced Tier of the OIBSIP BMI Calculator
task, including a graphical user interface, persistent BMI records,
multi-user support, and BMI trend visualization.

## Tech Stack

- Python
- Tkinter
- Matplotlib
- SQLite3

## Beginner Tier Features

- [x] Prompt user for weight in kilograms
- [x] Prompt user for height in meters
- [x] Calculate BMI using the formula:

```text
BMI = weight / (height²)

 Classify BMI into standard categories:

Underweight: BMI < 18.5

Normal: BMI 18.5–24.9

Overweight: BMI 25–29.9

Obese: BMI ≥ 30

 Display the BMI value rounded to 2 decimal places

 Display the BMI category

 Reject non-numeric input with a helpful error message

 Reject negative and zero values with a helpful error message

Advanced Tier Features
 GUI application built using Tkinter

 Input fields for user name, weight, and height

 Calculate BMI button

 Colour-coded BMI category feedback

 Multi-user support for different named users

 Historical BMI records stored in an SQLite database

 BMI trend displayed using a Matplotlib line chart

 Error handling for SQLite database read/write failures

BMI Formula
BMI = Weight (kg) / Height² (m)
BMI Categories
BMI Range	Category
Below 18.5	Underweight
18.5 – 24.9	Normal
25.0 – 29.9	Overweight
30.0 and above	Obese
Application Features
1. BMI Calculation
The application accepts the user's:

Name

Weight in kilograms

Height in meters

After clicking the Calculate BMI button, the application calculates
the BMI and displays the result rounded to two decimal places.

2. Colour-Coded Feedback
The BMI category is displayed using colour-coded feedback.

Underweight – Orange

Normal – Green

Overweight – Orange

Obese – Red

3. Multi-User Support
The application allows BMI records to be saved for different named users.

Each record is associated with the name entered by the user.

4. Historical BMI Records
BMI records are stored persistently using SQLite.

The database stores:

User name

Weight

Height

BMI

BMI category

Date and time

The application provides a View History option to display previously
saved BMI records for a user.

5. BMI Trend Visualization
The application provides a View BMI Trend option.

A Matplotlib line chart displays the user's BMI values over time,
allowing the user to visualize changes in BMI.

6. Input Validation
The application validates user input and displays helpful error messages
when:

Weight is not numeric

Height is not numeric

Weight is zero

Height is zero

Weight is negative

Height is negative

User name is empty

7. Database Error Handling
SQLite database operations include error handling for database
read and write failures.

The application displays an appropriate error message instead of
crashing when a database operation fails.

Installation
Clone the OIBSIP repository:

git clone https://github.com/prudviraj12345/OIBSIP.git
Navigate to the Task 2 directory:

cd OIBSIP/Python-Task2-BMICalculator
Install the required Python dependency:

pip install -r requirements.txt
Requirements
The requirements.txt file contains:

matplotlib
Tkinter and SQLite3 are part of the standard Python environment used
by this project.

How to Run
Run the application using:

python bmi_calculator.py

A graphical BMI Calculator window will open.

Basic Usage
Enter the user's name.
Enter weight in kilograms.
Enter height in meters.
Click Calculate BMI.
View the BMI value and category.
Use View History to view previous records.
Use View BMI Trend to display the BMI trend graph.
Database

The application automatically creates an SQLite database:

bmi_records.db

The database is created when the application is started.

BMI records are stored in the database so that historical information
can be viewed later.

Project Structure
Python-Task2-BMICalculator/
│
├── bmi_calculator.py
├── requirements.txt
├── README.md
└── bmi_records.db

The bmi_records.db file is generated automatically by the application.

Example
User Name: Rahul
Weight: 70 kg
Height: 1.75 m


BMI: 22.86
Category: Normal
References

The project follows the resources suggested in the OIBSIP task guidelines:

Python BMI calculator tutorials
Python Tkinter GUI tutorials
Python Matplotlib line chart tutorials
Official Python Tkinter documentation
Python sqlite3 tutorials
Project Information

Program: OIBSIP – Python Programming

Task: Task 2 – BMI Calculator

Implementation: Advanced Tier

Technologies: Python, Tkinter, SQLite3, Matplotlib

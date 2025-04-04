# Hospital Management System

## Overview
This Python program is a Hospital Management System designed to manage patient appointments efficiently. 
It allows hospital staff to add patients, cancel appointments, and display the waiting list.

## Features
- Add new patients with their information such as name, phone number, age, gender, and emergency status.
- Cancel appointments for patients by their unique ID.
- Display the waiting list, sorted by priority.
- Automatically updates patient records in a CSV file.
- Uses a linked list data structure for efficient patient management.

## Requirements
- Python 3.x
- `csv` module
- `datetime` module
- `os` module

## Usage
1. Run the `main()` function in the `hospital_management_system.py` file.
2. Choose options from the menu:
   - Add Patient: Enter patient details to add them to the waiting list.
   - Cancel Appointment: Enter the patient ID to cancel their appointment.
   - Display Waiting List: View the current waiting list sorted by priority.
   - Exit: Save patient data to a CSV file and exit the program.

## Data Storage
- Patient information is stored in a CSV file named `patients.csv`.
- Waiting list data is written to a CSV file named `waiting.csv`.


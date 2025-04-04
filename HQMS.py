import csv
from datetime import datetime
import os


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Patient:
    def __init__(self, name, phone, age, gender, is_emergency):
        self.name = name
        self.phone = phone
        self.age = age
        self.gender = gender
        self.is_emergency = is_emergency
        self.patient_id = self.generate_patient_id()
        self.next = None  # Pointer to the next patient in the linked list

    def generate_patient_id(self):
        if self.is_emergency.lower() == 'yes':
            return 'EMERGENCY'
        elif self.gender.lower() == 'male':
            prefix = 'B' if self.age < 18 else ('M' if self.age < 65 else 'U')
        elif self.gender.lower() == 'female':
            prefix = 'G' if self.age < 18 else ('W' if self.age < 65 else 'A')
        else:
            return None
        return f"{prefix}{self.name[0].upper()}{self.phone[-4:]}"

class LinkedList:
    def __init__(self):
        self.head = None  # Initialize the head of the linked list

    def add_patient(self, patient):
        if not self.head:
            self.head = patient
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = patient

    def remove_patient(self, patient_id):
        if not self.head:
            return
        if self.head.patient_id == patient_id:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.patient_id == patient_id:
                current.next = current.next.next
                return
            current = current.next

class HospitalManagementSystem:
    def __init__(self):
        self.waiting_list = LinkedList()  # Initialize the linked list for waiting patients

    def add_patient(self):
        name = input("Enter patient's name: ")
        phone = input("Enter patient's phone number: ")
        age = int(input("Enter patient's age: "))
        gender = input("Enter patient's gender (Male/Female): ")
        is_emergency = input("Is it an emergency case? (Yes/No): ")

        new_patient = Patient(name, phone, age, gender, is_emergency)

        # Add patient to the waiting list
        self.waiting_list.add_patient(new_patient)

        print("Patient information saved successfully.")

    def cancel_appointment(self, patient_id):
        # Remove patient from the waiting list
        self.waiting_list.remove_patient(patient_id)

        # Update waiting list CSV
        waiting_list = self.display_waiting_list()
        self.write_to_waiting_list_csv(waiting_list, 'waiting.csv')

        # Update patient CSV to mark the appointment as canceled
        self.update_patient_csv(patient_id, status='Canceled')

        print("Appointment cancelled for patient with ID:", patient_id)

    def update_patient_csv(self, patient_id, status):
        try:
            temp_file = 'temp.csv'
            with open('patients.csv', mode='r', newline='') as file, \
                 open(temp_file, mode='w', newline='') as temp:
                reader = csv.DictReader(file)
                writer = csv.DictWriter(temp, fieldnames=reader.fieldnames)
                writer.writeheader()
                for row in reader:
                    if row['Patient ID'] == patient_id:
                        row['Status'] = status
                    writer.writerow(row)
            os.remove('patients.csv')
            os.rename(temp_file, 'patients.csv')
            print(f"Patient CSV updated for patient with ID: {patient_id}")
        except FileNotFoundError:
            print("Error: File not found.")
        except Exception as e:
            print("An error occurred while updating patient CSV:", e)

    def write_to_waiting_list_csv(self, patient_ids, filename):
        try:
            with open(filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                for patient_id in patient_ids:
                    writer.writerow([patient_id])
            print(f"Successfully wrote {len(patient_ids)} patient IDs to '{filename}'.")
        except IOError:
            print(f"Error writing to '{filename}'.")

    def display_waiting_list(self):
        print("Patients Waiting for Appointments:")
        current = self.waiting_list.head

        # Sort the patient list based on priority before displaying
        sorted_patients = self.sort_patients_by_priority()

        for patient_id in sorted_patients:
             print("Patient ID:", patient_id)
        return sorted_patients
            
    def sort_patients_by_priority(self):
        priority_dict = {
            'EMERGENCY': -1,  # Highest priority
            'A': 0, 'U': 1, 'G': 2, 'B': 3, 'W': 4, 'M': 5
        }

        patients = []
        current = self.waiting_list.head
        while current:
            patients.append(current.patient_id)
            current = current.next

        # Sort the patients list based on priority
        patients.sort(key=lambda x: (priority_dict.get(x[0], float('inf')), x))

        # Create a new list to rearrange patients
        rearranged_patients = []
        emergency_patients = []

        # Iterate through the sorted list
        for patient_id in patients:
            # Separate emergency patients
            if patient_id.startswith('EMERGENCY'):
                emergency_patients.append(patient_id)
            else:
                rearranged_patients.append(patient_id)

        # Place emergency patients at the beginning
        rearranged_patients = emergency_patients + rearranged_patients

        return rearranged_patients


def main():
    file_exists = os.path.isfile('patients.csv')
    hms = HospitalManagementSystem()
    while True:
        print("\nHospital Management System")
        print("1. Add Patient")
        print("2. Cancel Appointment")
        print("3. Display Waiting List")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            hms.add_patient()
        elif choice == '2':
            patient_id_to_cancel = input("Enter ID to cancel Appointment: ")
            hms.cancel_appointment(patient_id_to_cancel)
        elif choice == '3':
            patient_list = hms.display_waiting_list()
            hms.write_to_waiting_list_csv(patient_list, 'waiting.csv')
        elif choice == '4':
            print("Exiting...")
            with open('patients.csv', 'a', newline='') as csvfile:  # 'a' for append mode
                fieldnames = ['Name', 'Phone', 'Patient ID', 'Age', 'Emergency', 'Time In', 'Time Out', 'Time Given', 'Status']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()  # Write header only if the file is newly created
                current = hms.waiting_list.head
                while current:
                    writer.writerow({
                        'Name': current.name,
                        'Phone': current.phone,
                        'Patient ID': current.patient_id,
                        'Age': current.age,
                        'Emergency': current.is_emergency,
                        'Time In': get_current_time(),
                        'Time Out': '',  # Assuming it's empty initially
                        'Time Given': '',  # Assuming it's empty initially
                        'Status': 'Waiting'  # Assuming it's 'Waiting' initially
                    })
                    current = current.next
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
            continue



if __name__ == "__main__":
    main()

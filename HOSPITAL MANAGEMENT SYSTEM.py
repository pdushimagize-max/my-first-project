"""
HOSPITAL MANAGEMENT SYSTEM
Projet pédagogique en Python.

Les données sont conservées en mémoire pendant l'exécution seulement.
Utiliser exclusivement des données fictives pour les tests.
"""

from datetime import datetime

patients = {}
appointments = []
consultations = []
bills = {}


def read_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def read_int(prompt, minimum=None):
    while True:
        try:
            value = int(input(prompt).strip())
            if minimum is not None and value < minimum:
                print(f"Enter a number greater than or equal to {minimum}.")
                continue
            return value
        except ValueError:
            print("Invalid number. Please enter a whole number.")


def read_date(prompt):
    while True:
        value = input(prompt + " (YYYY-MM-DD): ").strip()
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d").date()
            return parsed.isoformat()
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD, for example 2026-10-20.")


def read_time(prompt):
    while True:
        value = input(prompt + " (HH:MM): ").strip()
        try:
            parsed = datetime.strptime(value, "%H:%M").time()
            return parsed.strftime("%H:%M")
        except ValueError:
            print("Invalid time. Use 24-hour format, for example 14:30.")


def register_patient():
    print("\n--- REGISTER A NEW PATIENT ---")
    patient_id = read_non_empty("Patient ID: ").upper()
    if patient_id in patients:
        print("Patient ID already exists!")
        return

    name = read_non_empty("Full name: ")
    age = read_int("Age: ", minimum=0)
    sex = read_non_empty("Sex (optional description): ")
    phone = read_non_empty("Phone number: ")
    blood_group = input("Blood group (optional): ").strip() or "Not provided"

    patients[patient_id] = {
        "name": name,
        "age": age,
        "sex": sex,
        "phone": phone,
        "blood_group": blood_group,
        "status": "Admitted",
        "admission_date": datetime.today().date().isoformat(),
        "discharge_date": None,
    }
    bills[patient_id] = {"charges": [], "paid": 0}
    print(f"Patient {patient_id} registered successfully.")


def display_patient(patient_id):
    info = patients[patient_id]
    print(f"\nPatient ID: {patient_id}")
    print(f"Name: {info['name']}")
    print(f"Age: {info['age']}")
    print(f"Sex: {info['sex']}")
    print(f"Phone: {info['phone']}")
    print(f"Blood group: {info['blood_group']}")
    print(f"Status: {info['status']}")
    print(f"Admission date: {info['admission_date']}")
    if info["discharge_date"]:
        print(f"Discharge date: {info['discharge_date']}")


def view_patients():
    print("\n--- ALL PATIENTS ---")
    if not patients:
        print("No patients registered.")
        return
    for patient_id in patients:
        display_patient(patient_id)
        print("-" * 35)


def find_patient():
    patient_id = input("Enter patient ID: ").strip().upper()
    if patient_id not in patients:
        print("Patient not found!")
        return None
    return patient_id


def search_patient():
    print("\n--- SEARCH FOR A PATIENT ---")
    patient_id = find_patient()
    if patient_id:
        display_patient(patient_id)


def book_appointment():
    print("\n--- BOOK AN APPOINTMENT ---")
    patient_id = find_patient()
    if not patient_id:
        return

    doctor = read_non_empty("Doctor's name: ")
    date = read_date("Appointment date")
    time = read_time("Appointment time")
    reason = read_non_empty("Reason for appointment: ")

    for appointment in appointments:
        if (appointment["doctor"].casefold() == doctor.casefold()
                and appointment["date"] == date
                and appointment["time"] == time
                and appointment["status"] == "Scheduled"):
            print("This doctor already has a scheduled appointment at that time.")
            return

    appointments.append({
        "patient_id": patient_id,
        "doctor": doctor,
        "date": date,
        "time": time,
        "reason": reason,
        "status": "Scheduled",
    })
    print("Appointment booked successfully!")


def view_appointments():
    print("\n--- APPOINTMENTS ---")
    if not appointments:
        print("No appointments registered.")
        return

    for number, appointment in enumerate(appointments, start=1):
        patient = patients[appointment["patient_id"]]
        print(f"\nAppointment {number}")
        print(f"Patient: {patient['name']} ({appointment['patient_id']})")
        print(f"Doctor: {appointment['doctor']}")
        print(f"Date/time: {appointment['date']} {appointment['time']}")
        print(f"Reason: {appointment['reason']}")
        print(f"Status: {appointment['status']}")


def register_consultation():
    print("\n--- REGISTER A CONSULTATION ---")
    patient_id = find_patient()
    if not patient_id:
        return
    if patients[patient_id]["status"] != "Admitted":
        print("This patient has been discharged. Re-admission workflow is not implemented.")
        return

    doctor = read_non_empty("Doctor's name: ")
    date = read_date("Consultation date")
    symptoms = read_non_empty("Symptoms reported: ")
    observations = read_non_empty("Clinical observations (entered by clinician): ")
    diagnosis = read_non_empty("Diagnosis (entered by authorized clinician): ")
    treatment = read_non_empty("Treatment (prescribed by authorized clinician): ")

    consultations.append({
        "patient_id": patient_id,
        "doctor": doctor,
        "date": date,
        "symptoms": symptoms,
        "observations": observations,
        "diagnosis": diagnosis,
        "treatment": treatment,
    })
    print("Consultation recorded successfully.")


def view_medical_history():
    print("\n--- MEDICAL HISTORY ---")
    patient_id = find_patient()
    if not patient_id:
        return

    history = [
        consultation for consultation in consultations
        if consultation["patient_id"] == patient_id
    ]
    if not history:
        print("No medical history available.")
        return

    print(f"Medical history for {patients[patient_id]['name']}:")
    for number, item in enumerate(history, start=1):
        print(f"\nConsultation {number}")
        print(f"Date: {item['date']}")
        print(f"Doctor: {item['doctor']}")
        print(f"Symptoms: {item['symptoms']}")
        print(f"Observations: {item['observations']}")
        print(f"Diagnosis: {item['diagnosis']}")
        print(f"Treatment: {item['treatment']}")


SERVICE_PRICES = {
    "consultation": 10000,
    "laboratory": 15000,
    "xray": 25000,
    "medication": 20000,
    "hospital_day": 30000,
}


def calculate_bill():
    print("\n--- HOSPITAL BILL ---")
    patient_id = find_patient()
    if not patient_id:
        return

    bill = bills[patient_id]
    print("Services:")
    print("1. Consultation - 10,000 BIF")
    print("2. Laboratory test - 15,000 BIF")
    print("3. X-ray - 25,000 BIF")
    print("4. Medication - 20,000 BIF")
    print("5. Hospital day - 30,000 BIF")
    print("6. Finish adding charges")

    service_keys = {
        "1": ("consultation", "Consultation"),
        "2": ("laboratory", "Laboratory test"),
        "3": ("xray", "X-ray"),
        "4": ("medication", "Medication"),
        "5": ("hospital_day", "Hospital day"),
    }

    while True:
        choice = input("Choose service (1-6): ").strip()
        if choice == "6":
            break
        if choice not in service_keys:
            print("Invalid option.")
            continue

        key, label = service_keys[choice]
        quantity = read_int("Quantity (whole number): ", minimum=1)
        unit_price = SERVICE_PRICES[key]
        bill["charges"].append({
            "service": label,
            "quantity": quantity,
            "unit_price": unit_price,
            "total": quantity * unit_price,
        })
        print(f"Added {label}: {quantity * unit_price:,} BIF")

    total = sum(charge["total"] for charge in bill["charges"])
    print_bill(patient_id, total)


def print_bill(patient_id, total=None):
    bill = bills[patient_id]
    if total is None:
        total = sum(charge["total"] for charge in bill["charges"])
    paid = bill["paid"]
    balance_due = total - paid

    print(f"\nBill for {patients[patient_id]['name']} ({patient_id})")
    if not bill["charges"]:
        print("No charges recorded.")
    else:
        for charge in bill["charges"]:
            print(
                f"{charge['service']}: {charge['quantity']} x "
                f"{charge['unit_price']:,} = {charge['total']:,} BIF"
            )
    print(f"Total: {total:,} BIF")
    print(f"Paid: {paid:,} BIF")
    print(f"Balance due: {balance_due:,} BIF")

    if total > paid:
        record = input("Record a payment now? (y/n): ").strip().lower()
        if record == "y":
            amount = read_int("Payment amount (BIF): ", minimum=1)
            if amount > balance_due:
                print("Payment exceeds the amount due. Payment not recorded.")
            else:
                bill["paid"] += amount
                print("Payment recorded.")
                print(f"Remaining balance: {total - bill['paid']:,} BIF")


def discharge_patient():
    print("\n--- DISCHARGE PATIENT ---")
    patient_id = find_patient()
    if not patient_id:
        return

    patient = patients[patient_id]
    if patient["status"] == "Discharged":
        print("This patient is already discharged.")
        return

    discharge_date = read_date("Discharge date")
    doctor = read_non_empty("Responsible doctor's name: ")

    patient["status"] = "Discharged"
    patient["discharge_date"] = discharge_date
    patient["discharge_doctor"] = doctor
    print("Patient discharged successfully.")
    print(f"Status: {patient['status']}")


def hospital_statistics():
    print("\n--- HOSPITAL STATISTICS ---")
    total_patients = len(patients)
    admitted = sum(1 for p in patients.values() if p["status"] == "Admitted")
    discharged = sum(1 for p in patients.values() if p["status"] == "Discharged")
    scheduled_appointments = sum(1 for a in appointments if a["status"] == "Scheduled")
    print(f"Total patients: {total_patients}")
    print(f"Currently admitted: {admitted}")
    print(f"Discharged patients: {discharged}")
    print(f"Total appointments: {len(appointments)}")
    print(f"Scheduled appointments: {scheduled_appointments}")
    print(f"Total consultations: {len(consultations)}")
    total_charges = sum(
        charge["total"]
        for bill in bills.values()
        for charge in bill["charges"]
    )
    total_paid = sum(bill["paid"] for bill in bills.values())
    print(f"Total charges: {total_charges:,} BIF")
    print(f"Total payments recorded: {total_paid:,} BIF")


def main():
    menu = {
        "1": ("Register a new patient", register_patient),
        "2": ("View all patients", view_patients),
        "3": ("Search for a patient", search_patient),
        "4": ("Book an appointment", book_appointment),
        "5": ("View appointments", view_appointments),
        "6": ("Register a consultation", register_consultation),
        "7": ("View patient medical history", view_medical_history),
        "8": ("Calculate hospital bill / record payment", calculate_bill),
        "9": ("Discharge a patient", discharge_patient),
        "10": ("View hospital statistics", hospital_statistics),
        "11": ("Exit", None),
    }

    while True:
        print("\n" + "=" * 45)
        print("       HOSPITAL MANAGEMENT SYSTEM")
        print("=" * 45)
        for number, (label, _) in menu.items():
            print(f"{number}. {label}")

        choice = input("Choose an option: ").strip()

        if choice == "11":
            print("Goodbye!")
            break
        elif choice in menu:
            menu[choice][1]()
        else:
            print("Invalid option. Choose from 1 to 11.")


if __name__ == "__main__":
    main()

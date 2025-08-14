import re

# This is the source of truth, in a simple format: (text, [(entity_text, LABEL)])
SOURCE_DATA = [
    # --- get_person_details ---
    ("details for Mira Yadav", [("Mira Yadav", "name")]),
    ("contact number for Siya Reddy", [("Siya Reddy", "name")]),
    ("find the teacher with a PhD", [("teacher", "role"), ("PhD", "education")]),
    ("who is the admin for Library", [("admin", "role"), ("Library", "department")]),
    ("get details for roll number 107", [("107", "rollNumber")]),
    ("whose father is Aditya Kumar", [("Aditya Kumar", "fatherName")]),
    ("find student with contact 9980327308", [("student", "role"), ("9980327308", "contact")]),
    ("who teaches mathematics", [("mathematics", "subject")]),
    ("show student in class 7B", [("student", "role"), ("7B", "classSection")]),
    ("show me the physics teacher", [("physics", "subject"), ("teacher", "role")]),
    ("roll number of Aarav", [("Aarav", "name")]),
    ("find student in class 9C", [("student", "role"), ("9C", "classSection")]),
    ("who is head of Accounts", [("Accounts", "department")]),
    ("show me roll number 42", [("42", "rollNumber")]),
    ("find teacher with number 9876543210", [("teacher", "role"), ("9876543210", "contact")]),
    ("find Rohan Sharma", [("Rohan Sharma", "name")]), # New
    ("show me Kunal", [("Kunal", "name")]), # New
    ("details for Aditya Kumar", [("Aditya Kumar", "name")]), # New

    # --- add_person ---
    ("add student Aarav Kumar to class 8A", [("student", "role"), ("Aarav Kumar", "name"), ("8A", "classSection")]),
    ("create admin Isha Mehta for Accounts", [("admin", "role"), ("Isha Mehta", "name"), ("Accounts", "department")]),
    ("enroll Vikram Singh as a teacher for Math", [("Vikram Singh", "name"), ("teacher", "role"), ("Math", "subject")]),
    ("add teacher Anita Singh subject English", [("teacher", "role"), ("Anita Singh", "name"), ("English", "subject")]),
    ("create a new student", [("student", "role")]),
    ("i want to add a teacher", [("teacher", "role")]),
    ("add student named Kunal in 10A", [("student", "role"), ("Kunal", "name"), ("10A", "classSection")]),
    ("insert a new admin for HR", [("admin", "role"), ("HR", "department")]),
    ("add student with father Ramesh Kumar", [("student", "role"), ("Ramesh Kumar", "fatherName")]),
    ("create a teacher for Computer Science", [("teacher", "role"), ("Computer Science", "subject")]),
    ("add vikash chahar", [("vikash chahar", "name")]), # New
    ("create user Siya Reddy", [("Siya Reddy", "name")]), # New
    ("enroll teacher Aarav", [("teacher", "role"), ("Aarav", "name")]), # New

    # --- edit_person ---
    ("change Siya Reddy's contact to 9998887776", [("Siya Reddy", "name"), ("9998887776", "contact")]),
    ("update education for Prisha Yadav to PhD", [("Prisha Yadav", "name"), ("PhD", "education")]),
    ("move roll number 107 to section C", [("107", "rollNumber"), ("C", "section")]),
    ("assign Social as new subject for Prisha Yadav", [("Social", "subject"), ("Prisha Yadav", "name")]),
    ("update Aarav's class to 11B", [("Aarav", "name"), ("11B", "classSection")]),
    ("correct father name for Mira", [("Mira", "name")]),
    ("change department for Isha Mehta", [("Isha Mehta", "name")]),
    ("update subject of Vikram Singh", [("Vikram Singh", "name")]),
    ("edit Vikram Singh", [("Vikram Singh", "name")]), # New
    ("update Reyansh Patel", [("Reyansh Patel", "name")]), # New
    ("change details for Anita", [("Anita", "name")]), # New

    # --- block_person ---
    ("block Mira Yadav", [("Mira Yadav", "name")]),
    ("i want to block vikash chahar", [("vikash chahar", "name")]),
    ("block student with father Aditya Kumar", [("student", "role"), ("Aditya Kumar", "fatherName")]),
    ("block admin from Library", [("admin", "role"), ("Library", "department")]),
    ("block contact 9701758896", [("9701758896", "contact")]),
    ("remove roll number 55", [("55", "rollNumber")]),
    ("delete teacher Anita Singh", [("teacher", "role"), ("Anita Singh", "name")]),
    ("block meera yadav", [("meera yadav", "name")]), # New
    ("remove Isha Mehta", [("Isha Mehta", "name")]), # New
    ("delete Prisha", [("Prisha", "name")]), # New

    # --- promote_person ---
    ("promote student with roll 107", [("student", "role"), ("107", "rollNumber")]),
    ("promote Reyansh Patel to head of Library", [("Reyansh Patel", "name"), ("Library", "department")]),
    ("promote the english teacher", [("english", "subject"), ("teacher", "role")]),
    ("promote Siya", [("Siya", "name")]),
    ("assign head admin to Isha Mehta", [("Isha Mehta", "name")]),
    ("promote Mira Yadav", [("Mira Yadav", "name")]), # New

    # --- clarify_action ---
    ("Mira Yadav", [("Mira Yadav", "name")]),
    ("Siya Reddy", [("Siya Reddy", "name")]),
    ("student Aarav Kumar class 7", [("student", "role"), ("Aarav Kumar", "name"), ("7", "className")]),
    ("teacher Prisha", [("teacher", "role"), ("Prisha", "name")]),
    ("admin Isha Mehta", [("admin", "role"), ("Isha Mehta", "name")]),
    ("roll number 12", [("12", "rollNumber")]),
    ("class 5B", [("5B", "classSection")]),
    ("contact 9123456789", [("9123456789", "contact")]),
]


def generate_training_data_file(source_data):
    """Generates a training_data.py file with calculated character indices."""
    formatted_data = []
    for text, annotations in source_data:
        entities = []
        processed_text = text
        for entity_text, label in annotations:
            match = re.search(re.escape(entity_text), processed_text)
            if match:
                start, end = match.span()
                entities.append((start, end, label))
                processed_text = processed_text[:start] + ("_" * len(entity_text)) + processed_text[end:]
            else:
                print(f"WARNING: Could not find entity '{entity_text}' in text '{text}'")
        
        entities.sort(key=lambda x: x[0])
        formatted_data.append((text, {"entities": entities}))

    with open("training_data.py", "w", encoding="utf-8") as f:
        f.write("TRAIN_DATA = [\n")
        for item in formatted_data:
            f.write(f"    {item},\n")
        f.write("]\n")
    print("✅ Successfully generated and saved training_data.py with correct indices.")

if __name__ == "__main__":
    generate_training_data_file(SOURCE_DATA)
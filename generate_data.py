import re

# This is the source of truth, in a simple format: (text, [(entity_text, LABEL)])
# New and enhanced examples are marked with comments.
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
    ("find Rohan Sharma", [("Rohan Sharma", "name")]), 
    ("show me Kunal", [("Kunal", "name")]), 
    ("details for Aditya Kumar", [("Aditya Kumar", "name")]),
    ("find details for Mr. Sharma", [("Mr. Sharma", "name")]), # New & Advanced: Handles titles
    ("who is the techer for maths?", [("techer", "role"), ("maths", "subject")]), # New & Advanced: Handles typos
    ("Can you tell me who the head of the Science department is?", [("Science", "department")]), # New & Advanced: Conversational

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
    ("add vikash chahar", [("vikash chahar", "name")]), 
    ("create user Siya Reddy", [("Siya Reddy", "name")]), 
    ("enroll teacher Aarav", [("teacher", "role"), ("Aarav", "name")]),
    ("register new student Rohan", [("student", "role"), ("Rohan", "name")]), # New & Advanced: Verb variation
    ("Add a new student named Kabir, roll number 15, to class 6A", [("student", "role"), ("Kabir", "name"), ("15", "rollNumber"), ("6A", "classSection")]), # New & Advanced: Complex multi-entity query

    # --- edit_person ---
    ("change Siya Reddy's contact to 9998887776", [("Siya Reddy", "name"), ("9998887776", "contact")]),
    ("update education for Prisha Yadav to PhD", [("Prisha Yadav", "name"), ("PhD", "education")]),
    ("move roll number 107 to section C", [("107", "rollNumber"), ("C", "section")]),
    ("assign Social as new subject for Prisha Yadav", [("Social", "subject"), ("Prisha Yadav", "name")]),
    ("update Aarav's class to 11B", [("Aarav", "name"), ("11B", "classSection")]),
    ("correct father name for Mira", [("Mira", "name")]),
    ("change department for Isha Mehta", [("Isha Mehta", "name")]),
    ("update subject of Vikram Singh", [("Vikram Singh", "name")]),
    ("edit Vikram Singh", [("Vikram Singh", "name")]),
    ("update Reyansh Patel", [("Reyansh Patel", "name")]),
    ("change details for Anita", [("Anita", "name")]),
    ("update Mr. Kumar's phone number to 8877665544", [("Mr. Kumar", "name"), ("8877665544", "contact")]), # New & Advanced: Surname with title
    ("assign Physics to Mr. Singh", [("Physics", "subject"), ("Mr. Singh", "name")]), # New & Advanced: Simple but effective phrase
    ("change a student's father name", [("student", "role")]), # New & Advanced: General query without specifics

    # --- block_person ---
    ("block Mira Yadav", [("Mira Yadav", "name")]),
    ("i want to block vikash chahar", [("vikash chahar", "name")]),
    ("block student with father Aditya Kumar", [("student", "role"), ("Aditya Kumar", "fatherName")]),
    ("block admin from Library", [("admin", "role"), ("Library", "department")]),
    ("block contact 9701758896", [("9701758896", "contact")]),
    ("remove roll number 55", [("55", "rollNumber")]),
    ("delete teacher Anita Singh", [("teacher", "role"), ("Anita Singh", "name")]),
    ("block meera yadav", [("meera yadav", "name")]),
    ("remove Isha Mehta", [("Isha Mehta", "name")]),
    ("delete Prisha", [("Prisha", "name")]),
    ("block yadav", [("yadav", "name")]), # New & Advanced: Handles just a surname
    ("Roll number 88, please remove them", [("88", "rollNumber")]), # New & Advanced: Different sentence structure
    ("block students Aarav and Mira", [("students", "role"), ("Aarav", "name"), ("Mira", "name")]), # New & Advanced: Multiple entities of the same type

    # --- promote_person ---
    ("promote student with roll 107", [("student", "role"), ("107", "rollNumber")]),
    ("promote Reyansh Patel to head of Library", [("Reyansh Patel", "name"), ("Library", "department")]),
    ("promote the english teacher", [("english", "subject"), ("teacher", "role")]),
    ("promote Siya", [("Siya", "name")]),
    ("assign head admin to Isha Mehta", [("Isha Mehta", "name")]),
    ("promote Mira Yadav", [("Mira Yadav", "name")]),
    ("Okay, now please go ahead and promote Isha Mehta to be the new head of the HR department", [("Isha Mehta", "name"), ("HR", "department")]), # New & Advanced: Handles conversational fluff

    # --- clarify_action ---
    ("Mira Yadav", [("Mira Yadav", "name")]),
    ("Siya Reddy", [("Siya Reddy", "name")]),
    ("student Aarav Kumar class 7", [("student", "role"), ("Aarav Kumar", "name"), ("7", "className")]),
    ("teacher Prisha", [("teacher", "role"), ("Prisha", "name")]),
    ("admin Isha Mehta", [("admin", "role"), ("Isha Mehta", "name")]),
    ("roll number 12", [("12", "rollNumber")]),
    ("class 5B", [("5B", "classSection")]),
    ("contact 9123456789", [("9123456789", "contact")]),
    ("Mr. Patel", [("Mr. Patel", "name")]), # New & Simple
    ("class 8 section C", [("8", "className"), ("C", "section")]), # New & Advanced: Decomposed entities
    ("detials for Riya", [("Riya", "name")]), # New & Advanced: Typo without a clear verb
]


def generate_training_data_file(source_data):
    """Generates a training_data.py file with calculated character indices."""
    formatted_data = []
    for text, annotations in source_data:
        entities = []
        # Create a placeholder text to mark found entities and avoid re-matching
        processed_text = text
        for entity_text, label in annotations:
            # Use a case-insensitive search to be more robust
            match = re.search(re.escape(entity_text), processed_text, re.IGNORECASE)
            if match:
                start, end = match.span()
                entities.append((start, end, label))
                # Replace the found entity in the processed text to avoid matching it again
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
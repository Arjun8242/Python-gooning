# Name: Arjun Jaiswal
# project: CLI Student Grade Manager

students = []

print("===================================")
print("   CLI Student Grade Manager")
print("===================================")
print("\n")

while(True):
    print("\nMenu")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")
    print("\n")

    choice = input("Enter your choice:")

    if(choice=="1"):
        name=input("Enter student name:")
        roll_number=input("Enter roll number:")
        grade=input("Enter grade:")

        student={
            "name":name,
            "roll_number":roll_number,
            "grade":grade
        }

        students.append(student)

        print("Student added successfully")

    elif(choice=="2"):
        if(len(students)==0):
            print("No students found")
        else:
            for student in students:
                print(f"Name: {student['name']}, Roll Number: {student['roll_number']}, Grade: {student['grade']}")
                
    elif(choice=="3"):
        name=input("Enter student name:")
        roll_number=input("Enter roll number:")
        for student in students:
            if(student["name"]==name and student["roll_number"]==roll_number):
                print(f"Name: {student['name']}, Roll Number: {student['roll_number']}, Grade: {student['grade']}")
                break
        else:
            print("Student not found")
    elif(choice=="4"):
        name=input("Enter student name:")
        roll_number=input("Enter roll number:")
        for student in students:
            if(student["name"]==name and student["roll_number"]==roll_number):
                student["grade"]=input("Enter new grade:")
                print("Student updated successfully")
                break
        else:
            print("Student not found")
    elif(choice=="5"):
        name=input("Enter student name:")
        roll_number=input("Enter roll number:")
        for student in students:
            if(student["name"]==name and student["roll_number"]==roll_number):
                students.remove(student)
                print("Student deleted successfully")
                break
        else:
            print("Student not found")
    elif(choice=="6"):
        break
    else:
        print("Invalid choice")
        


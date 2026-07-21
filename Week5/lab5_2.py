# lab5_2.py

python_students = {"S001", "S003", "S005", "S007", "S009"}
java_students = {"S002", "S003", "S006", "S007", "S010"}

# Students in both courses
print("Students in both courses:")
print(python_students & java_students)

# All unique students
print("\nAll unique students:")
print(python_students | java_students)

# Students only in Python
print("\nStudents only in Python:")
print(python_students - java_students)

# Students in only one course
print("\nStudents in only one course:")
print(python_students ^ java_students)

# Remove duplicates
all_students_list = ["S001", "S003", "S005", "S001", "S002"]

unique_students = list(set(all_students_list))

print("\nOriginal List:")
print(all_students_list)

print("Unique List:")
print(unique_students)
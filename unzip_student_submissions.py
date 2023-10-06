import csv
import zipfile
from itertools import islice
import sys


if len(sys.argv) != 5:
        print("Usage: python script_name.py <top|bottom> <number_of_students> <zip_file_path> <csv_file_path>")
        sys.exit(1)


top_or_bottom = sys.argv[1]
number_of_students = int(sys.argv[2])
zip_path = sys.argv[3]
csv_path = sys.argv[4]
out = "unzipped_submissions"
student_names = set()


def count_number_of_students():
        count = 0
        with open(csv_path, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                        name = row[0]
                        # Check if name is Test Student
                        if name == "Student, Test":
                                print(f"Skipping {name}.")
                        else:
                                count += 1
        return count


def get_student_names(skip, number_of_students, step=1):
        reader = csv.reader(file)
        for row in islice(reader, skip, skip + number_of_students, step):
                name = row[0]
                # Check if name is Test Student
                if name == "Student, Test":
                        print(f"Skipping {name}.")
                else:
                        last_name, first_name = "".join(row[0].replace('"', '').replace('-', '').split()).split(',')
                        formatted_name = f"{last_name.lower()}{first_name.lower()}"
                        student_names.add(formatted_name)


with open(csv_path, "r") as file:
        student_count = count_number_of_students()

        if top_or_bottom == "top":
                get_student_names(3, number_of_students)
        elif top_or_bottom == "bottom":
                # Start from end of file
                get_student_names(student_count - number_of_students, number_of_students)
        else:
                print("Usage: python script_name.py <top|bottom> <number_of_students> <zip_file_path> <csv_file_path>")
                sys.exit(1)


unzip_count = 0
with zipfile.ZipFile(zip_path, "r") as zip_file:
        for file_name in zip_file.namelist():
                prefix = file_name.split("_")[0]
                if prefix in student_names:
                        zip_file.extract(file_name, out)
                        unzip_count += 1
                        student_names.remove(prefix)
                        print(f"Extracted {file_name} to {out}.")
print(f"Done. Extracted {unzip_count} files. Missing {len(student_names)} students: {student_names}")
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def _get_average_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        avg_grade = self._get_average_grade()
        courses_in_progress_str = ', '.join(self.courses_in_progress)
        finished_courses_str = ', '.join(self.finished_courses)
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {avg_grade:.1f}\n'
                f'Курсы в процессе изучения: {courses_in_progress_str}\n'
                f'Завершенные курсы: {finished_courses_str}')

    def __lt__(self, other):
        if not isinstance(other, Student):
            print('Ошибка: Сравнивать можно только студентов со студентами')
            return
        return self._get_average_grade() < other._get_average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _get_average_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        avg_grade = self._get_average_grade()
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {avg_grade:.1f}')

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('Ошибка: Сравнивать можно только лекторов с лекторами')
            return
        return self._get_average_grade() < other._get_average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')


def avg_grade_for_course(students, course):
    total_sum = 0
    total_count = 0
    for student in students:
        if course in student.grades:
            total_sum += sum(student.grades[course])
            total_count += len(student.grades[course])
    if total_count == 0:
        return 0
    return total_sum / total_count


def avg_grade_for_lecturers(lecturers, course):
    total_sum = 0
    total_count = 0
    for lecturer in lecturers:
        if course in lecturer.grades:
            total_sum += sum(lecturer.grades[course])
            total_count += len(lecturer.grades[course])
    if total_count == 0:
        return 0
    return total_sum / total_count


student1 = Student('Ruoy', 'Eman', 'male')
student1.courses_in_progress += ['Python', 'Git']
student1.finished_courses += ['Введение в программирование']

student2 = Student('Jane', 'Doe', 'female')
student2.courses_in_progress += ['Python', 'Git']
student2.finished_courses += ['Введение в программирование']

lecturer1 = Lecturer('Some', 'Buddy')
lecturer1.courses_attached += ['Python']

lecturer2 = Lecturer('Other', 'Person')
lecturer2.courses_attached += ['Git']

reviewer1 = Reviewer('Some', 'Reviewer')
reviewer1.courses_attached += ['Python']

reviewer2 = Reviewer('Another', 'Reviewer')
reviewer2.courses_attached += ['Git']

reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student2, 'Python', 8)
reviewer1.rate_hw(student2, 'Python', 7)

reviewer2.rate_hw(student1, 'Git', 10)
reviewer2.rate_hw(student2, 'Git', 5)

student1.rate_lecture(lecturer1, 'Python', 10)
student1.rate_lecture(lecturer1, 'Python', 10)
student2.rate_lecture(lecturer1, 'Python', 9)

student1.rate_lecture(lecturer2, 'Git', 5)
student2.rate_lecture(lecturer2, 'Git', 7)

print(student1)
print()
print(student2)
print()
print(lecturer1)
print()
print(lecturer2)
print()
print(reviewer1)
print()
print(reviewer2)
print()

print(f'Студент 1 > Студент 2: {student1 > student2}')
print(f'Лектор 1 > Лектор 2: {lecturer1 > lecturer2}')

print(f"Средняя оценка студентов по курсу Python: {avg_grade_for_course([student1, student2], 'Python')}")
print(f"Средняя оценка студентов по курсу Git: {avg_grade_for_course([student1, student2], 'Git')}")

print(f"Средняя оценка лекторов по курсу Python: {avg_grade_for_lecturers([lecturer1, lecturer2], 'Python')}")
print(f"Средняя оценка лекторов по курсу Git: {avg_grade_for_lecturers([lecturer1, lecturer2], 'Git')}")
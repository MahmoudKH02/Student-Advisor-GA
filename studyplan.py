from courses import Course
from courses import calculate_prerequisists_priority


class StudyPlan:

    def __init__(self, name=None, total_hours=None) -> None:
        self.name = name
        self.total_credit_hours = total_hours
        self.courses: dict[str, list] = {}
        self.elective_courses = set()


    def get_total_hours(self):
        return self.total_credit_hours
    

    def set_total_hours(self, hours):
        self.total_credit_hours = hours


    def get_name(self):
        return self.name
    

    def get_name(self, name):
        self.name = name


    def get_electives(self) -> set:
        return self.elective_courses


    def get_courses(self) -> dict:
        return self.courses


    def add_course_to_plan(self, course_code, year, sem):
        key = str(year) + "-" + str(sem)

        if not self.courses.get(key):
            self.courses[key] = []

        self.courses[key].append(course_code)


    def __repr__(self) -> str:
        return f'Name: {self.name} | Total Hours: {self.total_credit_hours} \
            \nCourses: {self.courses}'


def read_study_plan(filename):
    """
    Reads the Study Plan from a .txt file.

    Arguments:
        filename -- a file name that contains the study plan as a (.txt) file.
    
    Returns:
        * study_plan -- an object of type (StudyPlan) containing:
                    The name of the specialization.
                    The total credit hours.
                    A list of courses in this specialization, ordered with respect to year and semester.
        * study_courses --  dictionary that has the course_code as the key, and the value as an object of type Courase.
    """
    study_plan = StudyPlan("computer Engineering", 158)
    study_courses = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()[1:]

        # iterate through each line
        for line in lines:
            info = line.strip().split(',')

            year, sem, course_code = info[:3]

            # add the course to the courses list of the study plan
            study_plan.add_course_to_plan(course_code, year, sem)

            if (len(course_code) > 5) and (course_code not in ['ENCS53xx', 'ENCS51xx']):
                credit_hours = int(course_code[5])

                course = Course(
                    course_id=course_code,
                    credit_hours=credit_hours,
                    prerequisists=info[3:]
                )

                # add the course to the courses dict
                study_courses[ course_code ] = course

            calculate_prerequisists_priority( study_courses, course.get_prerequisists() )
            
    return study_plan, study_courses


def read_electives(filename, study_plan: StudyPlan):
    """
    Read the elective courses from a .txt file

    Arguments:
        filename -- the file name contating the elective courses as a (.txt) file.

    Returns:
        elective_courses -- a dictionary that has the course_code as the key, and the value as an object of type Course.
    """
    electives = {}

    with open(filename, 'r') as f:
        lines = f.readlines()[1:]

        # iterate through each line
        for line in lines:
            info = line.strip().split(',')

            # get the credit hours from course code
            credit_hours = int(info[1][5])

            course = Course(
                course_id=info[1],
                credit_hours=credit_hours,
                prerequisists=info[2:]
            )

            study_plan.get_electives().add(info[1])

            course.group = int(info[0])

            # add the course to the elective dict
            electives[ info[1] ] = course

            calculate_prerequisists_priority( electives, info[2:] )

    return electives

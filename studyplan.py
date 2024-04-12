from courses import Course
from courses import calculate_prerequisists_priority


class StudyPlan:

    def __init__(self, spec_name=None, total_hours=None) -> None:
        self.spec_name = spec_name
        self.total_credit_hours = total_hours
        self.courses: dict[str, list] = {}


    def get_total_hours(self):
        return self.spec_name
    

    def set_total_hours(self, hours):
        self.total_credit_hours = hours


    def get_spec_name(self):
        return self.spec_name
    

    def get_spec_name(self, name):
        self.spec_name = name


    def get_courses(self) -> dict:
        return self.courses


    def add_course(self, course_code, year, sem):
        key = str(year) + "-" + str(sem)

        if not self.courses.get(key):
            self.courses[key] = []

        self.courses[key].append(course_code)


    def __repr__(self) -> str:
        return f'Name: {self.spec_name} | Total Hours: {self.total_credit_hours} \
            \nCourses: {self.courses}'


def read_study_plan(filename):
    """
    Reads the Study Plan from a .txt file.

    Arguments:
    filename -- a file name that contains the study plan as a (.txt) file.
    
    Returns:
    study_plan -- an object of type (StudyPlan) containing:
                    - The name of the specialization.
                    - The total credit hours.
                    - A list of courses in this specialization, ordered with respect to year and semester.

    study_courses -- a dictionary that has the course_code as the key, and the value as an object of type Course.
    """
    study_plan = StudyPlan("computer Engineering", 158)
    study_courses = dict()
    
    with open(filename, 'r') as f:
        lines = f.readlines()[1:]

        # iterate through each line
        for line in lines:
            info = line.strip().split(',')

            year, sem, course_code = info[:3]

            # add the course to the courses list of the study plan
            study_plan.add_course(course_code, year, sem)

            if (len(course_code) > 5) and (course_code not in ['ENCS53xx', 'ENCS51xx']):
                credit_hours = course_code[5]

                course = Course(
                    course_id=course_code,
                    credit_hours=credit_hours,
                    prerequisists=info[3:]
                )

                # add the course to the courses dict
                study_courses[ course_code ] = course

            calculate_prerequisists_priority( study_courses, course.get_prerequisists() )
            
    return study_plan, study_courses


def read_electives(filename):
    """
    Read the elective courses from a .txt file

    Arguments:
    filename -- the file name contating the elective courses as a (.txt) file.

    Returns:
    elective_courses -- a dictionary that has the course_code as the key, and the value as an object of type Course.
    """
    pass
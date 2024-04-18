from courses import Course
from courses import calculate_prerequisites_priority
from typing import Dict, List, Tuple


class StudyPlan:

    def __init__(self, name=None, total_hours=None) -> None:
        self.__name = name
        self.__total_credit_hours = total_hours
        self.__compulsory_courses: Dict[str, List] = {}
        self.__elective_courses: Dict[str, List] = {}


    def get_name(self):
        return self.__name
    

    def get_name(self, name):
        self.__name = name


    def get_total_hours(self):
        return self.__total_credit_hours
    

    def set_total_hours(self, hours):
        self.__total_credit_hours = hours


    def get_compulsory_courses(self) -> Dict[str, List]:
        return self.__compulsory_courses


    def get_elective_courses(self) -> Dict[str, List]:
        return self.__elective_courses


    def __repr__(self) -> str:
        return f'Name: {self.__name} | Total Hours: {self.__total_credit_hours} \
            \nCourses: {self.__compulsory_courses}\nElectives {self.__elective_courses}'


def read_study_plan(filename, spec_name, total_hours) -> Tuple[StudyPlan, Dict[str, Course]]:
    """
    Reads the Study Plan from a .txt file.

    Args:
        filename -- a file name that contains the study plan as a (.txt) file.
    
    Returns:
        * study_plan -- an object of type (StudyPlan) containing:
                    The name of the specialization.
                    The total credit hours.
                    A dictionary of list of courses representing each semester and the courses associated with the study plan,
                        ordered with respect to year and semester.
        * college_courses --  dictionary that has the course_code as the key, and the value as an object of type Course.
    """
    study_plan = StudyPlan(name=spec_name, total_hours=total_hours)
    college_courses = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()[1:]

    # iterate through each line
    for line in lines:
        info = line.strip().split(',')
        
        year, sem, course_code = info[:3]
        prereq = info[3:]

        # create a new semester if it doesn't exist in the study plan
        if not study_plan.get_compulsory_courses().get(str(year) + "-" + str(sem)):
            study_plan.get_compulsory_courses()[ str(year) + "-" + str(sem) ] = []

        # add the course to the corresponding semester in the study plan
        study_plan.get_compulsory_courses()[ str(year) + "-" + str(sem) ].append(course_code)

        if (len(course_code) > 5) and (course_code not in ['ENCS53xx', 'ENCS51xx']):
            credit_hours = int(course_code[5])

            course = Course(
                course_id=course_code,
                credit_hours=credit_hours,
                prerequisites=prereq
            )
            Course.num_courses += 1

            # add the course to the courses dict
            college_courses[ course_code ] = course

        calculate_prerequisites_priority( college_courses, prereq )

    return study_plan, college_courses


def read_electives(
        filename,
        study_plan: StudyPlan,
        college_courses: Dict[str, Course]
) -> Dict[str, Course]:
    """
    Read the elective courses from a .txt file

    Args:
        filename -- the file name containing the elective courses as a (.txt) file.

    Returns:
        elective_courses -- a dictionary that has the course_code as the key, and the value as an object of type Course.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()[1:]

    # iterate through each line
    for line in lines:
        info = line.strip().split(',')

        group, course_code = info[:2]
        prereq = info[2:]

        # get the credit hours from course code
        credit_hours = int(course_code[5])

        course = Course(
            course_id=course_code,
            credit_hours=credit_hours,
            prerequisites=prereq
        )
        Course.num_courses += 1

        # add the course to the elective dict
        college_courses[ course_code ] = course

        # create a new group if it doesn't exist in the elective courses
        if not study_plan.get_elective_courses().get(group):
            study_plan.get_elective_courses()[ group ] = []

        # add the course to the corresponding group in the elective courses
        study_plan.get_elective_courses()[ group ].append(course_code)

        calculate_prerequisites_priority( college_courses, prereq )

    return college_courses

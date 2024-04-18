from datetime import timedelta
from typing import Dict, Set, List
import json


class Course:

    num_courses = 0
    
    def __init__( self, course_id=None, credit_hours=None, prerequisites=[] ):
        self.__id = course_id
        self.__credit_hours = credit_hours
        self.__prerequisites = prerequisites
        self.__priority = 0
        self.__passed = False
        self.__sections: List[Section] = []


    def get_course_id(self):
        return self.__id
    

    def set_course_id(self, id):
        self.__id = id


    def get_credit_hours(self):
        return self.__credit_hours

    
    def get_prerequisites(self) -> List:
        return self.__prerequisites
    
    
    def set_prerequisites(self, pre):
        self.__prerequisites = pre
    

    def get_priority(self):
        return self.__priority
    

    def increase_priority(self, by=1):
        self.__priority += by


    def is_passed(self):
        return self.__passed


    def pass_course(self):
        self.__passed = True
        self.__priority = 0 # no priority for finished courses


    def is_available(self):
        return len(self.__prerequisites) == 0
    

    def get_sections(self):
        return self.__sections


    def set_sections(self, sections):
        self.__sections = sections


    def __repr__(self) -> str:
        return f'CourseCode: {self.__id} | Credit Hours: {self.__credit_hours} \
            \nPreReq: {self.__prerequisites} | Priority: {self.__priority}\n \
            Sections: {self.__sections}\n-----------------\n'


def calculate_prerequisites_priority(courses_dict: Dict[str, Course], prerequisites):
    """
    Calculate the priority of each prerequisites course depending on the number
    of courses that this course is prerequisites for.
    Iterate through the courses inside prerequisites, and increase the priority of these courses.

    Args:
        * course_dict -- a dict of all courses.
        * prerequisites -- a list of prerequisites.
    
    Modifies:
        modifies the __priority attribute in all courses inside the prerequisites

    Returns: None
    """
    for pre in prerequisites:

        if c := courses_dict.get(pre):
            c.increase_priority()


# ----------- Course Section Class -----------
class Section:

    def __init__(self, number=None, sec_type=None) -> None:
        if number:
            self.__number = int(number)

        self.__type = sec_type
        self.__instructor = None
        self.__days = set()
        self.__start_time = None
        self.__end_time = None

    
    def get_number(self):
        return self.__number


    def set_number(self, num):
        self.__number = num


    def get_type(self):
        return self.__type
    

    def set_type(self, sec_type):
        self.__type = sec_type


    def get_instructor(self):
        return self.__instructor
    

    def set_instructor(self, instructor):
        self.__instructor = instructor


    def get_days(self) -> Set:
        return self.__days


    def set_days(self, days):
        self.__days = days


    def get_start_time(self) -> timedelta:
        return self.__start_time
    

    def set_start_time(self, sec_time):
        self.__start_time = sec_time


    def get_end_time(self) -> timedelta:
        return self.__end_time
    

    def set_end_time(self, sec_time):
        self.__end_time = sec_time


    def __repr__(self) -> str:
        return f'ID: {self.__number}-{self.__type} | Days: {self.__days} \
            time: {self.__start_time}-{self.__end_time}\n'


    def has_conflict(self, other_section: 'Section'):
        """
        Returns weather the referenced Section object has time conflict with other_section.

        Args:
            other_section -- an instance of type Section, which is the other_section to check for time conflict with.

        Returns:
        True if there is conflict in time and day, False if not.
        """
        if other_section is self:
            return False

        return self.__days.intersection( other_section.get_days() ) \
            and ( 
                (other_section.get_start_time() <= self.__start_time < other_section.get_end_time())
                or (other_section.get_start_time() < self.__end_time <= other_section.get_end_time())
            )


def read_sections(filename, college_courses: Dict[str, Course]) -> Dict[str, Course]:
    """
    Read the sections from the course browser.

    Args:
        * filename -- Name for a JSON file, which contains sections and the section details.
        * college_courses -- a dictionary containing the courses with course code as the key, and Course as value.

    Modifies:
        college_courses. the sections that are read from the json file (course Browser) are added to the correct course if it exists.

    Returns:
        other_courses -- a dictionary containing the courses that are not included in the study plan
    """
    with open(filename, 'r') as f:
        json_date = json.load(f)

    for section_id, section_details in json_date.items():

        course_code, section_type, section_num = section_id.split('-')
        
        section = Section(
            number=int(section_num),
            sec_type=section_type
        )
        
        # get the rest of attributes for the course
        for key, value in section_details.items():
            if key == 'Instructor':
                section.set_instructor(value)
                
            # the day of week in which the section is reserved in
            else:
                section.get_days().add(key)

                # check if the time is already set, no need to recreate it
                if section.get_start_time() and section.get_end_time():
                    continue

                # get the start and end time (10:00 - 11:25)
                start, end = value.split(" - ")

                # split hours and minutes for the start time
                hours, minutes = map( int, start.split(':') )
                section.set_start_time( timedelta(hours=hours, minutes=minutes) )

                # split hours and minutes for the start time
                hours, minutes = map( int, end.split(':') )
                section.set_end_time( timedelta(hours=hours, minutes=minutes) )

        # check if the course already exists
        if c := college_courses.get(course_code):
            c.get_sections().append(section)
        else:
            # add the course to college courses (not needed for now).
            pass
            # credit_hours = int(course_code[5]) if course_code[5].isnumeric() else 0

            # # create new course
            # new_course = Course(course_code, credit_hours)
            # Course.num_courses += 1

            # # add the section to the new course
            # new_course.get_sections().append(section)

            # # add the course to other_courses
            # college_courses[ new_course.get_course_id() ] = new_course

    return college_courses

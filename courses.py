from datetime import timedelta
import json


class Course:

    def __init__( self, course_id=None, credit_hours=None, prerequisists=[] ):
        self.__id = course_id
        self.__credit_hours = credit_hours
        self.__prerequisists = prerequisists
        self.__priority = 0
        self.__passed = False
        self.__sections: list[Section] = []


    def get_course_id(self):
        return self.__id
    

    def set_course_id(self, id):
        self.__id = id


    def get_credit_hours(self):
        return self.__credit_hours

    
    def get_prerequisists(self) -> list:
        return self.__prerequisists
    
    
    def set_prerequisists(self, pre: list):
        self.__prerequisists = pre
    

    def get_priority(self):
        return self.__priority
    

    def inc_priority(self):
        self.__priority += 1


    def is_passed(self):
        return self.__passed


    def pass_course(self):
        self.__passed = True
    

    def get_sections(self):
        return self.__sections


    def set_sections(self, sections):
        self.__sections = sections


    def __repr__(self) -> str:
        if hasattr(self, 'group'):
            s = f'| Group: {self.group}'

        return f'CourseCode: {self.__id} | Credit Hours: {self.__credit_hours} {s} \
            \nPreReq: {self.__prerequisists} | Priority: {self.__priority}\n \
            Sections: {self.__sections}\n-----------------\n'


def calculate_prerequisists_priority(courses_dict: dict[str, Course], prerequisists):
    """
    Calculate the priority of each prerequisist course depending on the number
    of courses that this course is prerequisist for.
    Iterate throught the courses inside prerequisists, and increase the priority of these courses.

    Arguments:
        * course_dict -- a dict of all courses.
        * prerequisists -- a list of prerequests.
    
    Modifies:
        modifies the __priority attribute in all courses inside the prerequisists

    Returns: None
    """
    for pre in prerequisists:

        if c := courses_dict.get(pre):
            c.inc_priority()


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


    def get_days(self) -> set:
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


    def has_conflict(self, other_section: 'Section') -> bool:
        """
        returns weather the refrenced Section object has time conflict with other_section

        Arguments:
        other_section -- an instance of type Section, which is the other_section to check for time conflict with.

        Retrurns:
        True if there is conflict in time and day, False if not.
        """
        return self.__days.intersection( other_section.get_days() ) \
            and ( 
                (self.__start_time < other_section.get_end_time())
                or (self.__end_time > other_section.get_start_time())
            )


def read_sections(filename, compulsory_courses: dict[str, Course], elective_courses: dict[str, Course]):
    """
    Read the sections from the course browser.

    Arguments:
        * filename -- Name for a JSON file, which contains sections and the section details.
        * compulsory_courses -- a dictionary containing the compulsory courses with course code as the key, and Coruse as value.
        * elective_courses -- a dictionary containing the elective courseswith course code as the key, and Coruse as value.

    Modifies:
        * compulsory_courses.
        * elective_courses.
            the sections that are read from the json file (course Browser) are added to the correct course if it exists in either.

    Returns:
        other_courses -- a dictionary containing the courses that are not included in the study plan
    """
    other_courses = {} # other courses that dont exist in the neither compulsory nor the electives

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

                # if the time is already set, no need to recreate it
                if section.get_start_time() and section.get_end_time():
                    continue

                # get the start and end time (10:00 - 11:25)
                start, end = value.split(" - ")

                # split hours and minutes for the start time
                hours, minutes = map(int, start.split(':'))
                section.set_start_time( timedelta(hours=hours, minutes=minutes) )

                # split hours and minutes for the start time
                hours, minutes = map(int, end.split(':'))
                section.set_end_time( timedelta(hours=hours, minutes=minutes) )

        # check if the courses exists in compulsory, or elective courses
        if c:=compulsory_courses.get(course_code):
            c.get_sections().append(section)
        elif c:=elective_courses.get(course_code):
            c.get_sections().append(course_code)
        else:
            credit_hours = int(course_code[5]) if course_code[5].isnumeric() else 0

            # create new course
            new_course = Course(course_code, credit_hours)

            # add the section to the new course
            new_course.get_sections().append(section)

            # add the course to other_courses
            other_courses[ new_course.get_course_id() ] = new_course

    return other_courses

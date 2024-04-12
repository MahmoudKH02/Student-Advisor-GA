class Course:
    num_courses = 0

    def __init__( self, course_id=None, credit_hours=None, prerequisists=[] ):
        self.num_courses += 1

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


    def pass_course(self):
        self.__passed = True


    def is_passed(self):
        return self.__passed
    

    def get_sections(self):
        return self.__sections


    def set_sections(self, sections):
        self.__sections = sections


    def __repr__(self) -> str:
        return f'CourseCode: {self.__id} | Credit Hours: {self.__credit_hours} \
            \nPreReq: {self.__prerequisists} | Priority: {self.__priority}\n\n'


def calculate_prerequisists_priority(courses_dict: dict[str, Course], prerequisists):
    """
    Calculate the priority of each prerequisist course depending on the number
    of courses that this course is prerequisist for.
    Iterate throught the courses inside prerequisists, and increase the priority of these courses.

    Arguments:
    coruse_dict -- a dict of all courses.
    prerequisists -- a list of prerequests
    
    Modifies:
    modifies the __priority attribute in all courses inside the prerequisists

    Returns: None
    """
    for pre in prerequisists:

        if c := courses_dict.get(pre):
            c.inc_priority()


class Section:

    def __init__(self, instructor=None, day=None, time=None) -> None:
        self.__instructor = instructor
        self.__day = day
        self.__time = time

    
    def get_instructor(self):
        return self.__instructor
    

    def set_instructor(self, instructor):
        self.__instructor = instructor


    def get_day(self):
        return self.__day


    def set_day(self, day):
        self.__day = day


    def get_time(self):
        return self.__time
    

    def set_time(self, time):
        self.__time = time


def read_sections(filename):
    pass
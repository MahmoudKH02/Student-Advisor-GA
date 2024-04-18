from studyplan import StudyPlan, read_study_plan, read_electives
from courses import Course, read_sections
from ga import fitness
from typing import Dict


def create_course_pool(college_courses: Dict[str, Course], study_plan: StudyPlan):
    """
    Creates a pool of available courses that the student is able to register for.

    Args:
        * college_courses -- Dictionary of courses, with course_code as key, and Course object as value.
        * study_plan -- StudyPlan object, containing information about the study plan (compulsory courses).

    Returns:
        pool -- List containing all available courses for this student.
    """
    pool = []

    # Compulsory Courses
    for semester in study_plan.get_compulsory_courses().values():
        
        for course in semester:
            
            # check if the course is available (prerequisites are finished)
            if college_courses.get(course) and college_courses[ course ].is_available():
                pool.append(course)
            
    # Elective Courses
    for group in study_plan.get_elective_courses().values():

        for course in group:

            # check if the course is available (prerequisites are finished)
            if college_courses.get(course) and college_courses[ course ].is_available():
                pool.append(course)

    return pool


def main():

    # read the student inputs
    student_year = int(input('What Year you will be in the next semester?'))
    student_semester = int(input('Which Semester?'))

    CE_study_plan, college_courses = read_study_plan("CEStudyPlan.txt", "Computer Engineering", 158)
    college_courses = read_electives("Electives.txt", CE_study_plan, college_courses)

    for key, value in CE_study_plan.get_compulsory_courses().items():
        print(key + ':', value)

    print()

    for key, value in CE_study_plan.get_elective_courses().items():
        print(key + ':', value)

    print( 'Compulsory Courses:', len(CE_study_plan.get_compulsory_courses()) )
    print( 'Elective Courses:', len(CE_study_plan.get_elective_courses()) )

    other_courses = read_sections('courseBrowser_1.json', college_courses)

    print(college_courses)

    ape_chromosome = [
        ("MATH1411", college_courses["MATH1411"].get_sections()[0]),
        ("PHYS141", college_courses["PHYS141"].get_sections()[0]),
        ("ENME120", college_courses["ENME120"].get_sections()[0]),
        ("ARAB135", college_courses["ARAB135"].get_sections()[0]),
        ("ENGC1201", college_courses["ENGC1201"].get_sections()[0])
    ]
    print(ape_chromosome)
    print( ape_chromosome[2][1].has_conflict(ape_chromosome[2][1]) )

    print('fitness:', fitness(ape_chromosome, college_courses))

    normal_chromosome = []

    print(create_course_pool(college_courses, study_plan=CE_study_plan))


if __name__ == '__main__':
    main()
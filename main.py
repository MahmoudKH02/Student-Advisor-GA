from studyplan import StudyPlan, read_study_plan, read_electives
from courses import Course, read_sections
from genetic import run_ga
from typing import Dict


def create_courses_pool(college_courses: Dict[str, Course], study_plan: StudyPlan):
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
    student_year = input('What Year you will be in the next semester? ')
    student_semester = input('Which Semester? ')

    CE_study_plan, college_courses = read_study_plan(
        "CEStudyPlan.txt",
        "Computer Engineering", 158,
        student_year, student_semester
    )
    college_courses = read_electives("Electives.txt", CE_study_plan, college_courses)

    for key, value in CE_study_plan.get_compulsory_courses().items():
        print(key + ':', value)

    print()

    for key, value in CE_study_plan.get_elective_courses().items():
        print(key + ':', value)

    print( 'Compulsory Courses:', len( [c for semester in CE_study_plan.get_compulsory_courses().values() for c in semester] ) )
    print( 'Elective Courses:', len( [c for group in CE_study_plan.get_elective_courses().values() for c in group] ) )

    college_courses = read_sections('courseBrowser_1.json', college_courses)
    print(college_courses)

    best_schedule, best_schedule_fitness = run_ga(create_courses_pool(college_courses, CE_study_plan), college_courses, instructor='Mohammad Y. M. Alkhanafseh', days_off=0)
    
    print('best:', best_schedule)
    print('fitness:', best_schedule_fitness)

    print('\n'.join( [section[1].get_instructor() for section in best_schedule] ))


if __name__ == '__main__':
    main()

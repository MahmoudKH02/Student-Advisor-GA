import studyplan
from courses import read_sections


def main():
    CE_study_plan, college_courses = studyplan.read_study_plan("CEStudyPlan.txt")
    college_courses = studyplan.read_electives("Electives.txt", CE_study_plan, college_courses)

    for key, value in CE_study_plan.get_compusory_courses().items():
        print(key + ':', value)

    print()

    for key, value in CE_study_plan.get_elective_courses().items():
        print(key + ':', value)

    print( 'Compulsary Courses:', len(CE_study_plan.get_compusory_courses()) )
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

    normal_chromosome = []


if __name__ == '__main__':
    main()

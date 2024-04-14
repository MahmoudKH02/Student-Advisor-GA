import studyplan
from courses import read_sections


if set([1, 2, 3, 4]).intersection(set([10, 5])):
    print('hello world')

CE_study_plan, compulsory_courses = studyplan.read_study_plan("CEStudyPlan.txt")
elective_courses = studyplan.read_electives("Electives.txt", CE_study_plan)

for key, value in CE_study_plan.get_courses().items():
    print(f'{key}: {value}\n')

print(CE_study_plan.get_electives())

print('Compulsary Courses:', len([ course for courselist in CE_study_plan.get_courses().values() for course in courselist ]))
print('Elective Courses:', len(CE_study_plan.get_electives()))

# print(compulsory_courses)
# print(elective_courses)
# print(studyplan.compulsory_courses)
# print(studyplan.elective_courses)

# other_courses = read_sections('courseBrowser_1.json', compulsory_courses, elective_courses)

# print(compulsory_courses)
# print(elective_courses)

# print(other_courses)

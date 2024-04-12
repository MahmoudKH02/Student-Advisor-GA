import studyplan


CE_study_plan, compolsary_courses = studyplan.read_study_plan("CEStudyPlan.txt")

for key, value in CE_study_plan.get_courses().items():
    print(f'{key}: {value}\n')

print(compolsary_courses)

from typing import Tuple, List, Dict
from courses import Section, Course
from studyplan import StudyPlan


MAX_POPULATION = 200


def count_gene_collisions(selected_gene, chromosome: List[ Tuple[str, Section] ]):
    """
    Counts the number of collisions the gene at gene_index is causing.

    Args:
        * chromosome -- a list of tuple represeting the genes ("course_code", Section object).
        * gene_index -- an int, the index of the gene that the function is counting collisions caused by it.

    Returns:
        count -- the number of collisions.
    """
    count = 0

    for gene in chromosome:

        if gene[1].has_conflict(selected_gene[1]):
            count += 1

    return count


def fitness(
        chromosome: List[ Tuple[str, Section] ],
        prefrences: Dict,
        study_plan: StudyPlan,
        college_courses: Dict[str, Course],
):
    """
    Calculates the fitness of a given chromosome

    Args:
        prefrences -- a dict containing the prefrence for the student:
                    {
                        Credit Hours: <credit_hours>,
                        Prefered Instructor-soft/hard: [<instructor-1>, <instructor-2>, ...],
                        days-off: <days_off>,
                        max hours per day: <max_hours_day>
                    }
    """
    score = 0
    credit_hours = 0
    occupied_days = set()

    for gene in chromosome:
        score -= (count_gene_collisions(gene, chromosome) * 10)

        # penalize finished courses
        score -= (college_courses[ gene[0] ].is_passed() * 10)
        
        # add the days of this section as occupied days.
        occupied_days.add( gene[1].get_days() )
        
        # add the credit hours of the course
        credit_hours += college_courses[ gene[0] ].get_credit_hours()

        # add the priority of the course as a score
        score += college_courses[ gene[0] ].get_priority()

        # add multiple points if the course is a compulsory course
        if gene[0] in study_plan.get_compusory_courses():
            score += 3

        # add only one point if the course is an elective
        if gene[0] in study_plan.get_elective_courses():
            
            # give higher score if the student has finished courses from the same group
            # Code Here...
            score += 1

    return score


def mutate():
    pass


def populate():
    pass


def run_ga():
    pass
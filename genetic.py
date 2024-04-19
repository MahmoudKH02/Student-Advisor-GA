from typing import Tuple, List, Dict
from courses import Section, Course
import random


MAX_POPULATION = 200
MAX_COURSES = 10 # Per semester
MIN_COURSES = 2 # Per semester


def count_gene_collisions(selected_gene, chromosome: List[ Tuple[str, Section] ]):
    """
    Counts the number of collisions the gene at gene_index is causing.

    Args:
        * chromosome -- a list of tuple representing the genes ("course_code", Section object).
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
        college_courses: Dict[str, Course],
        preferences: Dict={}
):
    """
    Calculates the fitness of a given chromosome

    Args:
        * chromosome -- ...
        * preference -- a dictionary containing the preference for the student:
            - Credit Hours: <credit_hours>,
            - Preferred Instructors: [<instructor-1>, <instructor-2>, ...],
            - days-off: <days_off>,
            - max hours per day: <max_hours_day>, ---> not implemented yet
            - soft_preference: <True or False> (default True) ---> not implemented yet

            hard preferences means that the algorithm should not generate a solution that breaks the preference
        * college_courses -- ...
    """
    MAX_DAYS = 5
    
    score = 0
    credit_hours = 0 # used to satisfy the Credit Hours preference
    occupied_days = set() # used to satisfy the days-off preference

    for gene in chromosome:
        score -= ( (count_gene_collisions(gene, chromosome) / 2) * 10 )

        # highly penalize finished courses
        score -= (college_courses[ gene[0] ].is_passed() * 10)

        # add the priority of the course as a score
        score += college_courses[ gene[0] ].get_priority()
        
        # add the days of this section as occupied days.
        occupied_days.update( gene[1].get_days() )
        
        # add the credit hours of the course
        credit_hours += college_courses[ gene[0] ].get_credit_hours()

        # check the preferences of instructor
        if preferences.get("instructor"):

            if gene[1].get_instructor() in preferences.get("instructor"):
                score += 1

        # increase score by 1 for each day-off
        if preferred_days_off:=preferences.get("days-off"):
            days_off = ( MAX_DAYS - len(occupied_days) )
            score += ( preferred_days_off - abs(preferred_days_off - days_off) )

        # check credit hours preference
        if preferred_credit_hours:=preferences.get("credit"):
            score -= abs(preferred_credit_hours - credit_hours)

    return score


def populate(pool, college_courses: Dict[str, Course]):
    generation = []

    for i in range(MAX_POPULATION):
        num_courses = random.randint(MIN_COURSES, MAX_COURSES)

        # Randomly select courses
        selected_courses = random.sample(pool, num_courses)

        individual = []

        # Randomly select a section for each course
        for course in selected_courses:
            section = random.choice(college_courses[course].get_sections())
            individual.append( (course, section) )
        else:
            generation.append(individual)
    
    return generation


def crossover(first_parent, second_parent):
    cross_point = random.randint(1, min(len(first_parent), len(second_parent)) - 1)

    # Copy first half from each parent
    offspring1 = first_parent[:cross_point]
    offspring2 = second_parent[:cross_point]

    unique_courses1 = {}
    unique_courses2 = {}

    for course, section in offspring1:
        if not unique_courses1.get(course):
            unique_courses1[course] = section

    for course, section in offspring2:
        if not unique_courses2.get(course):
            unique_courses2[course] = section

    # Copy each gene one by one, to avoid duplicates
    # and ignore already existing courses

    # First Offspring
    for course, section in second_parent[cross_point:]:
        if unique_courses1.get(course):
            continue
        
        unique_courses1[course] = section

    # Second Offspring
    for course, section in first_parent[cross_point:]:
        if unique_courses2.get(course):
            continue
        
        unique_courses2[course] = section

    offspring1 = list(unique_courses1.items())
    offspring2 = list(unique_courses2.items())

    return offspring1, offspring2


def mutate(mutation_rate):
    pass


def run_ga(**kwargs):
    pass
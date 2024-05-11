from typing import Tuple, List, Dict
from courses import Section, Course
import random
import numpy as np

MAX_ITERATIONS = 20
MAX_POPULATION = 100

MAX_COURSES = 10 # Per semester
MIN_COURSES = 3  # Per semester
MAX_DAYS = 5     # Per Week


def count_gene_collisions(selected_gene, chromosome: List[ Tuple[str, Section] ]):
    """
    Counts the number of collisions the gene at gene_index is causing.

    Args:
        * selected_gene -- a tuple, representing the gene we wish to check if it has any conflicts with other genes.
        * chromosome -- a list of tuple representing all the genes `("course_code", Section object)` in the chromosome.

        Note that the `has_conflict()` returns false when checking if the gene has conflict with itself.

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
        * college_courses -- ...
        * preference -- a dictionary containing the preference for the student:
            - Credit Hours: <credit_hours>,
            - Preferred Instructors: <instructor>,
            - days_off: <days_off>,
            - max hours per day: <max_hours_day>, ---> not implemented yet
            - soft_preference: <True or False> (default True) ---> not implemented yet

            hard preferences means that the algorithm should not generate a solution that breaks the preference
    """
    score = 0
    credit_hours = 0 # used to satisfy the Credit Hours preference
    occupied_days = set() # used to satisfy the days-off preference
    instructors = set()

    for gene in chromosome:
        # score -= ( (count_gene_collisions(gene, chromosome) / 2) * 10 )

        if count_gene_collisions(gene, chromosome) or college_courses[ gene[0] ].is_passed():
            return 0

        # Highly penalize finished courses
        # score -= (college_courses[ gene[0] ].is_passed() * 10)

        # Add the priority of the course as a score
        score += college_courses[ gene[0] ].get_priority()
        
        # Add the days of this section as occupied days.
        occupied_days.update( gene[1].get_days() )

        # Add the instructor to instructors set
        instructors.add( gene[1].get_instructor() )
        
        # Add the credit hours of the course
        credit_hours += college_courses[ gene[0] ].get_credit_hours()
    
    # Penalize unmatched instructor preference
    if preferred_instructor:= preferences.get("instructor"):
        
        if preferred_instructor in instructors:
            # score -= 5
            score += 5

    # increase score by 1 for each day-off
    if preferred_days_off:= preferences.get("days_off"):
        days_off = ( MAX_DAYS - len(occupied_days) )
        score += ( preferred_days_off - abs(preferred_days_off - days_off) )

    # Penalize unmatched credit hours preference
    if preferred_credit_hours:= preferences.get("credit"):
        score -= abs(preferred_credit_hours - credit_hours)

    return score


def populate(pool, college_courses: Dict[str, Course]):
    generation = []

    for i in range(MAX_POPULATION):
        num_courses = random.randint(MIN_COURSES, MAX_COURSES)

        # Randomly select courses
        selected_courses = random.sample(pool, min(num_courses, len(pool)))

        individual = []

        # Randomly select a section for each course
        for course in selected_courses:

            if college_courses[course].get_sections():
                section = random.choice(college_courses[course].get_sections())
                individual.append( (course, section) )
        else:
            generation.append(individual)
    
    return generation


def crossover(first_parent, second_parent):

    # assert len(first_parent) > 2 and len(second_parent) > 2, 'error in range -- first:{} second:{}'.format(len(first_parent), len(second_parent))

    if len(first_parent) <= 2 or len(second_parent) <= 2:
        cross_point = 1
    else:
        cross_point = random.randint(1, min( len(first_parent), len(second_parent) ) - 1)


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

    # Copy each gene one by one to avoid duplicates
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


def roulette_wheel_selection(population, pop_fitness, total_fitness):
    selection_probabilities = [fit / total_fitness for fit in pop_fitness]

    # Create a roulette wheel (list with probabilities)
    roulette_wheel = np.cumsum(selection_probabilities)

    selected_parents = []

    for _ in range(MAX_POPULATION):
        spin_value = random.random()
        selected_index = np.searchsorted(roulette_wheel, spin_value)
        selected_parents.append(population[selected_index])

    return selected_parents


def run_ga(initial_pool, college_courses, **kwargs):

    assert all(key in ['instructor', 'days_off', 'credit_hours'] for key in kwargs.keys()), 'Unexpected preference'

    parents = populate(initial_pool, college_courses)

    for _ in range(MAX_ITERATIONS):

        offsprings = []

        # Generate the offsprings
        for i in range(0, len(parents), 2):
            offsprings.extend( crossover(parents[i], parents[i+1]) )

        population = parents + offsprings

        pop_fitness = []
        total_fitness = 0

        # Calculate the fitness for population
        for chromosome in population:
            fit = fitness(chromosome, college_courses)
            total_fitness += fit
            pop_fitness.append(fit)

        # Most fitted, will become parents for the next iteration
        parents = roulette_wheel_selection(population, pop_fitness, total_fitness)

    most_fitted_index = 0
    fitness_max = 0

    for i, individual in enumerate(parents):
        ind_fitness = fitness(individual, college_courses)

        if ind_fitness > fitness_max:
            fitness_max = ind_fitness
            most_fitted_index = i

    return parents[ most_fitted_index ], fitness_max

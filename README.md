***This Project is still under Development...***

# Main Idea
Using the Genetic Algorithm to select the most fitted schedule for the student semester, based on multiple factors according to college regulations, as well as the user (student) preferences.

---
# Introduction
The Program currently handles one study plan format, but development is still ongoing and it will be generalized in the future.


# Implementation
The main algorithm used is the *Genetic Algorithm* to find the best schedule for the student.
Before the algorithm is started, the program reads all essential information from `txt` files, and `json` files.

Information is stored inside objects, and here is each object, and what is its role in this program.

### Objects
* `StudyPlan`: This object mainly stores the compulsory, and elective courses offered by a certain study plan.
* `Course`: This stored the main information for a give course, such as: (*credit hours, priority, and available sections*). The priority increases with the course being a prerequisite for more courses.
* `Section`: This stored the days, start, end time, and the instructor.
* `Chromosomes & Genes`: Before going further in the implementation, the main thing in any genetic algorithm is the *chromosome*, and in this project, a `List` was used to represent the chromosome. Each *Gene* was represented with a `tuple` with this form `(course_code, Section)`

    i.e. `[("MATH101", <Section_Object>), ..., ("PHYS141", <Section_Object>)]`.


## Fitness function
The fitness function will take into consideration the university regulations as well as student preferences.

And it works as follows:
### Penalties
The following will result in the algorithm penalizing the total fitness of the chromosome (individual).

    1. Conflicting sections assigned (if there are sections that have the same days and time).
    2. If there are courses that has already been passed by the student.
    3. The number of credit hours doesn't meet the student preference.

### Rewards
The following will result in the algorithm rewarding (increasing) the total fitness of the chromosome (individual).

    1. Number of days-off, giving extra fitness score for each day-off.
    2. If the selected section/s's instructor meet the student preference for certain instructors.
    3. The priority of the courses being assigned (higher priority courses result in higher fitness).

## Crossover Function
* The crossover function uses the *single point crossover* method, to make the crossover between two chromosomes.
* Chromosomes have variable sizes, so the crossover point is chosen with respect to the smallest chromosome of the two parents.

## Selection Function (Criteria)
The selection is done using the *roulette-wheel-selection* method. After the offsprings has been generated from the crossover operation, all parents and offsprings are subject to this selection, with the best fitted individuals (chromosomes) being selected (100 in this project).

## Mutation Function
*Currently not implemented*

## Running All Functions
The `run_ga()` function runs the above functions in a loop, until a certain number of iterations is complete (20 in this project).

### Flow of Execution

1. The initial Population is generated (100 chromosomes)
2. The crossover function is run on the 100 chromosomes (parents), and now the population consists of (100 parents), and (50 offsprings).
3. The most fitted 100 chromosomes are selected using the `roulette_wheel_selection()` function.
4. Repeat from step 2 until max number if iteration is reached.

---
# Future Work
    - The program should be able to handle more than just one study plane (Computer Engineering plan.
    - The algorithm should be able to handle more preferences.
    - The program should be able to handle free elective courses, as for now it has not been dealt with.

MAX_POPULATION = 200


def count_gene_collision(chromosome, gene_index):
    """
    Counts the number of collisions gene_index is causing.

    Args:
        * chromosome -- a list of tuple represeting the genes ("course_code", Section object).
        * gene_index -- an int, the index of the gene that the function is counting collisions caused by it.

    Returns:
        count -- the number of collisions.
    """
    pass


def fitness(chromosome):
    score = 0

    for gene in chromosome:
        score -= count_gene_collision(chromosome, gene)
        
        # check prefrences and other factors...

    return score


def populate():
    pass
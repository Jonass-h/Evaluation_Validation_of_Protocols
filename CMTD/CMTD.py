import numpy as np
from Graph import Graph


class CMTD:
    ## properties

    transition_matrix = 0
    initial_distribution = 0
    card_Etat = 0

    ## methods
    def __init__(self):
        print(" CMTD created")

    def set_transition_matrix(self):
        # read one by one and check
        print("la cardinalit√© de l'espace des etats : ")
        self.card_Etat = int(input())
        self.initial_distribution = np.zeros(shape=self.card_Etat)

        # declare a local transition matrix
        self.transition_matrix = np.zeros(shape=(self.card_Etat, self.card_Etat))
        i = 0
        while i < self.card_Etat:
            line = np.zeros(self.card_Etat)
            j = 0
            while j < self.card_Etat:
                print(f"p[{i}][{j}] = ")
                element = float(input())
                # print(f"element = {element}")
                line[j] = element
                if not self.is_probability(element):
                    print(" help : les valeurs doivent etre entre 0 et 1")
                    print("        re-taper ... ")
                    j = j - 1
                j = j + 1

            self.transition_matrix[i] = line
            if not self.line_is_distribution(line):
                print(
                    " help : les lignes doivent etre des distributions de probabilit√©"
                )
                print("        re-taper ... ")
                i = i - 1
            i = i + 1

        print("###############" " matrice de transitoin #################")
        print(self.transition_matrix)
        print("##########################################################")
        return True

    def is_probability(self, number):
        return number <= float(1) and number >= float(0)

    def line_is_distribution(self, line):
        local_line = np.array(line)
        return local_line.sum() == float(1)

    def transitoire(self, given_initial_distribution, n):
        resultat = np.array(given_initial_distribution)
        for i in range(0, n):
            resultat = resultat.dot(self.transition_matrix)
        return resultat

    def all_possible_transitoire(self):
        print(" simulation du regime transitoire ")
        print("entrer n =")
        n = int(input())

        print("######## voici les different vecteur d'etat transitoire ########")
        for i in range(0, self.card_Etat):
            # generate an initial distribution
            local_initial_distribution = np.zeros(self.card_Etat)
            local_initial_distribution[i] = 1
            ##
            print(
                f"{local_initial_distribution} { self.transitoire(local_initial_distribution, n) } "
            )

    def is_irreductible(self):
        g = Graph(self.card_Etat)
        g_prime = g.graph_from_matrix(self.card_Etat, self.transition_matrix)
        return g_prime.is_irreductible()

    def get_states_period_old_version(self):
        # this function return the period for each state
        # and  the period of the CMTD

        # build all the matrices M.power(1-->card_Etat)
        matrix_powers = np.zeros(shape=(self.card_Etat, self.card_Etat, self.card_Etat))
        matrix_powers[:][:][0] = self.transition_matrix
        print("matrix_powers[:][:][0]")
        print(matrix_powers[:][:][0])

        for i in range(1, self.card_Etat):
            matrix_powers[:][:][i] = (matrix_powers[:][:][i - 1]).dot(
                self.transition_matrix
            )
            print(f"matrix_powers[:][:][ {i} ]")
            print(matrix_powers[:][:][i])

        state_period = np.ones(shape=self.card_Etat)
        i = 0
        while i < self.card_Etat:
            state_gcd = np.gcd.reduce(matrix_powers[i][i][:])
            state_period[i] = state_gcd
            i = i + 1
        return state_period, np.gcd.reduce(state_period)

    def get_states_period(self):
        return 5

    def is_ergodic(self):
        _, cmtd_period = self.get_states_period()
        return self.is_irreductible() and cmtd_period == 1

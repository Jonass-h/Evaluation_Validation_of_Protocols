import numpy as np


class RdP:
    ## properties
    n = 0  # cardinalité des place
    m = 0  # cardinalité des transitions
    c_moins = 0
    c_plus = 0
    marquage = 0

    ## methods
    def __init__(self):
        print(" entrer le nombre de place")
        self.n = int(input())
        print(" entrer le nombre de transition")
        self.m = int(input())
        print(" entrer le marquage initiale")
        self.read_marquage()
        print(" entrer la matrice c moins")
        self.read_c(1)
        print(" entrer la matrice c plus")
        self.read_c(0)
        print(" Bornitude de rdp")
        self.rdp_est_borne()

    def read_marquage(self):
        self.marquage = np.zeros(shape=self.n)
        i = 0
        while i < self.n:
            print(f"marquage[{i}] = ")
            element = int(input())
            while element < 0:
                print(" retaper :")
                element = int(input())
            self.marquage[i] = element
            i = i + 1

    def read_c(self, signe):
        if signe == 0:
            self.c_plus = np.zeros(shape=(self.n, self.m))
        elif signe == 1:
            self.c_moins = np.zeros(shape=(self.n, self.m))
        else:
            print("error of signe")
            return false

        i = 0
        while i < self.n:
            line = np.zeros(self.m)
            j = 0
            while j < self.m:
                if signe == 0:
                    print(f"c_plus[{i}][{j}] = ")
                else:
                    print(f"c_moins[{i}][{j}] = ")

                element = int(input())
                while element < 0:
                    print(" retaper :")
                    element = int(input())
                line[j] = element
                j = j + 1

            if signe == 0:
                self.c_plus[i] = line
            else:
                self.c_moins[i] = line
            i = i + 1

        print("###############" " afichage  #################")
        if signe == 0:
            print(("c plus"))
            print(self.c_plus)
        else:
            print(("c moins"))
            print(self.c_moins)
        print("##########################################################")
        return True

    def est_franchissable(self, marquage_tuple, transition_idx):
        return np.greater_equal(marquage_tuple, self.c_moins[:][transition_idx])

    def calcuer_prochain_marquage(self, marquage_tuple, transition_idx):
        return (
            marquage_tuple
            - self.c_moins[:][transition_idx]
            + self.c_plus[:][transition_idx]
        )

    def stop(self, marquage_actuel, prochain_marquage):
        return np.greater(prochain_marquage, marquage_actuel)

    def rdp_est_borne(self):
        np_marquage = 1
        marquage_traité = []
        marquage_non_traité = [self.marquage]
        i = 0
        while len(marquage_non_traité) > 0:
            try:
                marquage_actuele = marquage_non_traité.pop()
                while i < self.m:
                    if self.est_franchissable(marquage_actuele, i):
                        np_marquage += 1
                        prochain_marquage = self.calcuer_prochain_marquage(
                            marquage_actuel, i
                        )
                        if self.stop(marquage_actuele, prochain_marquage):
                            return False, _, _
                        if not prochain_marquage in marquage_traité:
                            marquage_non_traité.add(prochain_marquage)
                    i = i + 1
                marquage_traité.add(marquage_actuele)
            except:
                # ensemble des marquage non trité est vide
                return True, np_marquage, marquage_traité

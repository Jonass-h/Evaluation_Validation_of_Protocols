import numpy as np


class RdP:
    ## properties
    n = 0  # cardinalité des place
    m = 0  # cardinalité des transitions
    c_moins = 0
    c_plus = 0
    marquage = 0

    ## methods
    def __init__(self, n, m, c_moins, c_plus, marquage):
        self.n = n
        self.m = m
        self.marquage = marquage
        self.c_moins = c_moins
        self.c_plus = c_plus

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
        print(" est franchissable ... ")
        print(f"marquage_tuple = {marquage_tuple}")
        print(f"transition_idx = {transition_idx}")
        print(
            f" c_moins = { self.c_moins[:, transition_idx] }"
        )  # self.c_moins[:, transition_idx]

        return np.all(marquage_tuple >= self.c_moins[:, transition_idx])

    def calcuer_prochain_marquage(self, marquage_tuple, transition_idx):
        return (
            marquage_tuple
            - self.c_moins[:, transition_idx]
            + self.c_plus[:, transition_idx]
        )

    def stop(self, marquage_actuel, prochain_marquage):
        return np.greater(prochain_marquage, marquage_actuel)

    def rdp_est_borne(self):
        nb_marquage = 1
        marquage_traité = []
        marquage_non_traité = [self.marquage]
        print(f" self.marquage : {self.marquage}")
        print(f" marquage_non_traité : {marquage_non_traité}")

        while len(marquage_non_traité) > 0:
            print("****************************************")
            try:
                marquage_actuele = marquage_non_traité.pop(0)
                print(f" marquage_actuele : {marquage_actuele}")
                marquage_traité.append(marquage_actuele)
                print(f" marquage_traité : {marquage_traité}")
                i = 0
                print(f"m = {self.m}")
                print(f"i = {i}")
                while i < self.m:
                    print(" enter the inner while of transitions ...")
                    print(self.est_franchissable(marquage_actuele, i))
                    if self.est_franchissable(marquage_actuele, i):
                        print(f" la transition {i} est franchissable")
                        np_marquage += 1
                        prochain_marquage = self.calcuer_prochain_marquage(
                            marquage_actuel, i
                        )
                        if self.stop(marquage_actuele, prochain_marquage):
                            return False, _, _
                        if not prochain_marquage in marquage_traité:
                            marquage_non_traité.append(prochain_marquage)
                    i = i + 1
            except:
                # ensemble des marquage non trité est vide
                return True, nb_marquage, marquage_traité

    def tirable(self, M, t):
        return np.all(M >= self.c_moins[:, t])

    def rdp_est_borne1(self):

        checked = []
        pending = [self.marquage]

        while pending != []:

            # chek if it already checked
            M = pending.pop(0)
            M_in_checked = False
            for item in checked:
                if np.all(item == M):
                    M_in_checked = True
                    break

            if not M_in_checked:
                checked.append(M)
                for t in range(self.m):
                    if self.tirable(M, t=t):
                        newM = M + self.c_plus[:, t] - self.c_moins[:, t]
                        print(f"{M} ---> {newM}")
                        pending.append(newM)

                        if self.superior(newM, M):
                            print("--- not bounded ---")
                            return False

        print(f"bounded with |A| = {len(checked)}")
        return True

    def superior(self, newM, oldM):
        return np.all(newM >= oldM) and np.any(newM > oldM)

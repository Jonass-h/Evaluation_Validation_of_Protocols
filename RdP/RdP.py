import numpy as np

class RdP:
    ## properties
    n = 0  # cardinalité des place
    m = 0  # cardinalité des transitions
    c_moins = 0
    c_plus = 0
    c=0
    marquage = 0

    ## methods
    def __init__(self, n, m, c_moins, c_plus, marquage):
        self.n = n
        self.m = m
        self.marquage = marquage
        self.c_moins = c_moins
        self.c_plus = c_plus
        self.c = (c_plus)-(c_moins)

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
    
    def calcuer_prochain_marquage(self, marquage_tuple, transition_idx):
        return (
            marquage_tuple
            - self.c_moins[:, transition_idx]
            + self.c_plus[:, transition_idx]
        )

    def stop(self, marquage_actuel, prochain_marquage):
        return np.greater(prochain_marquage, marquage_actuel)

    def est_franchissable(self, marquage_actuel, transition_idx):
        return np.all(marquage_actuel >= self.c_moins[:, transition_idx])
    
    def superior(self, nouveau_marquage, ancien_marquage):
        return np.all(nouveau_marquage >= ancien_marquage) and np.any(nouveau_marquage > ancien_marquage)
    
    def superior_all(self,nouveau_marquage,list_marquage_traité):
        for item in list_marquage_traité :
            if not self.superior(nouveau_marquage,item):
                return False
        return True

    def rdp_est_borne(self):
        traité = []
        non_traité = [self.marquage]
        
        while len(non_traité) != 0:

            marquage_actuel = non_traité.pop(0)
            marquage_exist = False
            for item in traité:
                if (np.all(item == marquage_actuel)):
                    marquage_exist = True
                    break

            if not marquage_exist:
                traité.append(marquage_actuel)
                for t in range(self.m):
                    if self.est_franchissable(marquage_actuel,t):
                        nouveau_marquage= marquage_actuel + self.c[:,t]
                        print(f"{marquage_actuel} ****** {nouveau_marquage}")
                        non_traité.append(nouveau_marquage)
                        if( self.superior_all(nouveau_marquage,traité) ):
                            print("  rdp non borné ")
                            return False
                    
        print(f" rdp borné avec : {len(traité)}")
        return True

    def rdp_sans_blocage(self):
        traité = []
        non_traité = [self.marquage]
        
        while len(non_traité) != 0:

            marquage_actuel = non_traité.pop(0)
            marquage_exist = False
            for item in traité:
                if (np.all(item == marquage_actuel)):
                    marquage_exist = True
                    break

            if not marquage_exist:
                traité.append(marquage_actuel)
                counter=0
                for t in range(self.m):
                    if self.est_franchissable(marquage_actuel,t):
                        counter+=1
                        nouveau_marquage= marquage_actuel + self.c[:,t]
                        # print(f"{marquage_actuel} ****** {nouveau_marquage}")
                        non_traité.append(nouveau_marquage)
                        
                    
                        if( self.superior(nouveau_marquage, marquage_actuel) ):
                            # branche infinie
                            traité.append(nouveau_marquage)
                if counter==0:
                    print("blocage")
                    return False
                    
        print("rdp sans blocage ")
        return True
    
    def marquage_existe(self,marquage,liste_traité):
        for item in liste_traité:
            if (np.all(item == marquage)):
                return True
        return False

    def marquage_mene_vers_initiale(self,marquage,liste_marquage_menant):
        # verifier si un marquage donné mene vers le marquage initiale
        for item in liste_marquage_menant:
            if (np.all(item == marquage)):
                return True
        else :
            traité = []
            non_traité = [marquage]
            
            while len(non_traité) != 0:
                marquage_actuel = non_traité.pop(0)
                #print(f"marquage_actuel  = {marquage_actuel}")
                # verifier si le marquage est déja traité
                marquage_exist = self.marquage_existe(marquage_actuel,traité)

                if not marquage_exist:
                    traité.append(marquage_actuel)
                    for t in range(self.m):
                        if self.est_franchissable(marquage_actuel,t):
                            nouveau_marquage= marquage_actuel + self.c[:,t]
                            #print(nouveau_marquage)
                            if np.all(nouveau_marquage == self.marquage) or self.marquage_existe(nouveau_marquage,liste_marquage_menant):
                                return True
                            if( self.superior(nouveau_marquage, marquage_actuel) ):
                                print("RdP infini ... ")
                                traité.append(nouveau_marquage)
                            else :
                                #print("appednig non_traité")
                                non_traité.append(nouveau_marquage)
                #print(non_traité)
            return False

    def rdp_est_reinitialisable(self):
        mene_ver_marquage_initial=[]
        traité = []
        non_traité = [self.marquage]
        
        while len(non_traité) != 0:
            # verifier si le marquage à été déja calculé
            marquage_actuel = non_traité.pop(0)
            print(marquage_actuel)
            marquage_exist = self.marquage_existe(marquage_actuel,traité)
            #print(f"marquage_exist exist : {marquage_exist}")
            if not marquage_exist:
                # tester si ce marquage mene vers le marquage initale
                if self.marquage_mene_vers_initiale(marquage_actuel,mene_ver_marquage_initial) :
                    mene_ver_marquage_initial.append(marquage_actuel)
                else:
                    return False
                
                traité.append(marquage_actuel)
                for t in range(self.m):
                    if self.est_franchissable(marquage_actuel,t):
                        nouveau_marquage= marquage_actuel + self.c[:,t]
                        if( self.superior(nouveau_marquage, marquage_actuel) ):
                            traité.append(nouveau_marquage)
                        else :
                            non_traité.append(nouveau_marquage)
        return True

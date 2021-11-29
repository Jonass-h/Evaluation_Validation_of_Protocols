import numpy as np

class RdP:
    ## properties
    n = 0  # cardinalité des place
    m = 0  # cardinalité des transitions
    c_moins = 0
    c_plus = 0
    c=0 # calculable
    marquage = 0
    ensemble_marquage_accessible=0#calculable
    flag=[]#calculable => qui dit mene ou non vers marquage initiale

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
                        if( self.superior(nouveau_marquage,marquage_actuel) ):
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
                    print(f"etat de blocage {marquage_actuel}")

                    return False
                    
        print("rdp sans blocage ")
        return True
    
    def marquage_existe(self,marquage,liste_traité):
        for item in liste_traité:
            if (np.all(item == marquage)):
                return True
        return False
    ## idée de réinitialisation
    def construire_ensemble_marquage_accessible_and_flag(self):
        traité = []
        non_traité = [self.marquage]
        ensemble_marquage_accessible=[self.marquage]
        flag=[True]
        
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
                        
                        if( self.superior(nouveau_marquage,marquage_actuel) ):
                            # branche infinie
                            traité.append(nouveau_marquage)
                        else :
                            non_traité.append(nouveau_marquage)
                            ensemble_marquage_accessible.append(nouveau_marquage)
                            flag.append(False)
                    
        self.ensemble_marquage_accessible=ensemble_marquage_accessible
        self.flag=flag
        """ print(len(self.flag)==len(self.ensemble_marquage_accessible))
        print("ensemble de marquage accessible creé") """

    def marquage_mene_vers_initiale_one_step(self,marquage,indice,liste_marquage_menant):
        for t in range(self.m):
            if self.est_franchissable(marquage,t):
                nouveau_marquage= marquage + self.c[:,t]
                if self.marquage_existe(nouveau_marquage,liste_marquage_menant) :
                    liste_marquage_menant.append(marquage)
                    self.flag[indice]=True
                    return liste_marquage_menant
        return liste_marquage_menant

    def rdp_est_reinitialisable(self):
        self.construire_ensemble_marquage_accessible_and_flag()
        """ print(f"ensemble_marquage_accessible {self.ensemble_marquage_accessible}")
        print(f"flag {self.flag}") """
        self.ensemble_marquage_accessible.pop(0)
        self.flag.pop(0)
        ensemble_marquage_menant=[self.marquage]
        ## idée :
        # 1. construire ensemble de marquage accessible
        # 2. parcourir ensemble de marquage accessible plusieur itération
        # 3. et pour chaque itération noter les marquage qui mene vers marquage initiale
        # et ainsi de suite
        sortir=False
        while not sortir:
                sortir=True
                # pour chaque niveau de marquage
                avant=len(ensemble_marquage_menant)
                for i in range(len(self.ensemble_marquage_accessible)):
                    if not self.flag[i]:
                        sortir=False
                        liste_marquage_menant=self.marquage_mene_vers_initiale_one_step(self.ensemble_marquage_accessible[i],i,ensemble_marquage_menant)
                if avant==len(ensemble_marquage_menant) :
                    """                     
                    print(f"ensemble_marquage_accessible {self.ensemble_marquage_accessible}")
                    print(f"flag {self.flag}")
                    print(len(self.flag)==len(self.ensemble_marquage_accessible)) 
                    """
                    return all(self.flag)

        return False

    def rdp_quasi_vivant(self):
        # toutes les transition doivent apparaitre dans le GMA
        traité = []
        non_traité = [self.marquage]
        ensemble_transition_fanchi = set()
        
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
                        ensemble_transition_fanchi.add(t)
                        print(len(ensemble_transition_fanchi))
                        if len(ensemble_transition_fanchi)==self.m:
                            return True
                        nouveau_marquage= marquage_actuel + self.c[:,t]
                        
                        if( self.superior(nouveau_marquage,marquage_actuel) ):
                            traité.append(nouveau_marquage)
                        else :
                            non_traité.append(nouveau_marquage)
                    
        return False

    def rdp_vivant(self):
        self.construire_ensemble_marquage_accessible_and_flag()
        for item in self.ensemble_marquage_accessible:
            temp_rdp=RdP(self.n, self.m, self.c_moins, self.c_plus, marquage=item)
            if not temp_rdp.rdp_quasi_vivant():
                return False
        return True

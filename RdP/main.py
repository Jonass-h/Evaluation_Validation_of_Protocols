import numpy as np
from RdP import RdP


if __name__ == "__main__":
  
    # Borné  Réinitialisable
    c_moins_1   = np.array([[1,0],[0,0],[1,1]])
    c_plus_1    = np.array([[1,1],[0,1],[0,0]])
    marquage_1  = np.array( [1, 2, 0])
    rdp_1       = RdP(n=3, m=2, c_moins=c_moins_1, c_plus=c_plus_1, marquage=marquage_1)

    c_moins_2   = np.array([[1,0,0],[0,1,0],[0,0,1],[0,0,1]])
    c_plus_2    = np.array([[0,0,1],[0,0,1],[1,0,0],[0,1,0]])
    marquage_2  = np.array( [1,1,0,0])
    rdp_2       = RdP(4,3,c_moins_2, c_plus_2,marquage_2)

    print("rdp2")
    print("*********************************************************")
    print(f"bornitude de RdP : {rdp_2.rdp_est_borne()}")
    print("*********************************************************")
    print(f" RdP sans blocage  : {rdp_2.rdp_sans_blocage()}")
    print("*********************************************************")
    print(f" RdP reinitialisable  : {rdp_2.rdp_est_reinitialisable()}")
    print("*********************************************************")
    print("rdp1")
    print("*********************************************************")
    print(f"bornitude de RdP : {rdp_1.rdp_est_borne()}")
    print("*********************************************************")
    print(f" RdP sans blocage  : {rdp_1.rdp_sans_blocage()}")
    print("*********************************************************")
    print(f" RdP reinitialisable  : {rdp_1.rdp_est_reinitialisable()}")
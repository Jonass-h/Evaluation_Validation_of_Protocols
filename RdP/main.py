import numpy as np
from RdP import RdP


if __name__ == "__main__":
    c_moins = np.array([[1, 2, 4], [0, 1, 0], [0, 0, 0]])
    c_plus = np.array([[0, 0, 0], [0, 3, 0], [2, 1, 1]])
    marquage =np.array( [3, 1, 0])
    rdp1 = RdP(n=3, m=3, c_moins=c_moins, c_plus=c_plus, marquage=marquage)
    print("*********************************************************")
    print(f"bornitude de RdP : {rdp1.rdp_est_borne()}")  
    print("*********************************************************")
    print(f" RdP sans blocage  : {rdp1.rdp_sans_blocage()}")
    
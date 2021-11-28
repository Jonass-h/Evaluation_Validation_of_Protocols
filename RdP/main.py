import numpy as np
from RdP import RdP


if __name__ == "__main__":
    c_moins = [[1, 2, 4], [0, 1, 0], [0, 0, 0]]
    c_plus = [[0, 0, 0], [0, 3, 0], [2, 1, 1]]
    marquage = [3, 1, 0]
    rdp1 = RdP(n=3, m=3, c_moins=c_moins, c_plus=c_plus, marquage=marquage)
    print("bornitude de RdP :")
    print(rdp1.rdp_est_borne1())

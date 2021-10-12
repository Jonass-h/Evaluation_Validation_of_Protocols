import numpy as np
from CMTD import CMTD


def main():
    # create CMTD
    cmtd1 = CMTD()
    # fill properties from STDIN
    cmtd1.set_transition_matrix()
    # do some simulations
    cmtd1.all_possible_transitoire()


if __name__ == "__main__":
    main()

import numpy as np
def get_P_matrix(K : int):

    user_disk_probability = .4

    P = [[.15, .2, .15, .1],
        [.35, .25, .0, .0],
        [.35, .0, .25, .0],
        [.35, .0, .0, .25], 
        ]


    additional_columns = np.full((4, K), user_disk_probability / K)
    P = np.hstack((P, additional_columns))

    zero_rows = np.zeros((K, 4 + K))
    P = np.vstack((P, zero_rows))

    return P
import numpy as np
def get_P_matrix(K : int):
    cpu_index = 0
    system_disk_indexes = [1,2,3]

    user_disk_probability = .4
    user_disk_indexes = [4 + i for i in range(K)]

    P = [[.15, .2, .15, .1],
        [.35, .25, .0, .0],
        [.35, .0, .25, .0],
        [.35, .0, .0, .25], 
        ]


    for i in range(4):
        for kk in range(K):
            P[i].append(user_disk_probability/K)

    for i in range(K):
        P.append([0. for j in range(4 + K)])

    P = np.array(P)

    # print all
    #print('P:')
    #for arr in P:
    #    print(arr)

    return P
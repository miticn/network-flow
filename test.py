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
    print('P:')
    for arr in P:
        print(arr)

    return P

for i in range(2,6):
    P_transposed = get_P_matrix(i).transpose()
    I_minus_P_transposed =  np.identity(P_transposed.shape[0]) - P_transposed
    inverted  = np.linalg.inv(I_minus_P_transposed)

    A = np.zeros(inverted.shape[0])
    A[0] = 1
    
    lambda_matrix = np.dot(inverted, A)


    mi_array = [1/4, 1/10, 1/15, 1/15]
    for i in range(len(lambda_matrix) - len(mi_array)):
        mi_array.append(1/25)
    mi_array = np.array(mi_array)
    print('mi_array:', mi_array)
    print('lambda_matrix:', lambda_matrix)

    max_alpha = min(np.divide(mi_array, lambda_matrix))
    print('solution:', max_alpha*1000)

    lambda_matrix = max_alpha * lambda_matrix
    print("X:", lambda_matrix * 1000)
    print('U:', np.divide(lambda_matrix, mi_array))
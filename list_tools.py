def find_one(lista, needle):
    """
    returns True if needle is in list, False otherwise
    """
    return find_n(lista, needle, 1)

def find_n(lista, needle, n):
    """
    returns True if needle occurs n times in lista, False otherwise
    """
    counter = 0
    i = 0
    while counter < n and i <len(lista):
        if lista[i] == needle:
            counter += 1
        i += 1
    return counter >= n

##rewrite, streak isn't necessaryrot
def find_n_cons(lista, needle, n):
    """
    returns True if neddle occurs n consecutive times in list, False otherwise
    """
    biggest_streak = 0
    counter = 0
    i = 0
    while counter < n and i < len(lista):
        if lista[i] == needle:
            counter += 1
        else:
            biggest_streak = max(biggest_streak, counter)
            counter = 0
        i += 1
    biggest_streak = max(biggest_streak, counter)
    return biggest_streak >= n

def transpose_matrix(list_of_lists):
    transposed_matrix = []
    for i in range(len(list_of_lists)):
        column = []
        for j in range(len(list_of_lists[0])):
            column.append(list_of_lists[j][i])
        transposed_matrix.append(column)
    return transposed_matrix

def shift_list(lista, k):
    if k == 0:
        return lista
    if k > 0:
        return [None]*k + lista[:len(lista) - k]
    if k < 0:
        k = -k
        return lista[k:] + [None]*k

def rot_matrix_ccw(matrix):
    """
    rotates a matrix counter-clockwise
    """
    rotated_matrix = []
    for i in range(len(matrix)):
        rotated_column = shift_list(matrix[i], i-1)
        rotated_matrix.append(rotated_column)
    return rotated_matrix

def invert_column(column):
    return column[::-1]

def invert_matrix(matrix):
    inverted_matrix = []
    for column in matrix:
        inverted_matrix.append(invert_column(column))
    return inverted_matrix

def collapse_list(seq, empty = "."):
    """
    recives a list of strings or Nones
    returns a string
    """
    S = ""
    for elem in seq:
        if elem == None:
            S += empty
        else:
            S += elem
    return S

def collapse_matrix(matrix, empty=".", fence="|"):
    S = ""
    for column in matrix:
        S += collapse_list(column, empty)
        S += fence
    return S[:len(S)-1]

def explode_to_list(S, empty="."):
    L = []
    for letter in S:
        if letter != empty:
            L.append(letter)
        else:
            L.append(None)
    return L

def explode_to_matrix(S, empty=".", fence="|"):
    M = []
    list_S = S.split(fence) ##gives us a list of strings
    for s in list_S:
        M.append(explode_to_list(s))
    return M
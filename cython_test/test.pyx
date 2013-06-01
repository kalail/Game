
cdef int add_number(int number):
    cdef int i
    for i in range(10000000):
        number += 1
    return number

"""
Fall 2016
lanier4@illinois.edu
mradmstr514226508@gmail.com
"""
import time
import numpy as np


def show_matrix(A, n_dec=3):
    """ Display a matrix (nicely) with a fixed number of decimal places.
    """
    format_str = '%' + '0.0%df\t'%(n_dec)
    n_rows = A.shape[0]
    n_cols = 1
    if A.size > sum(A.shape): n_cols = A.shape[1]
    for row in range(0, n_rows):
        s = ''
        for col in range(0, n_cols):
            s = s + format_str%(A[row,col])
        print(s)
    return


def integer_to_alphabet_number(N):
    """ convert integer to spreadsheet column lettering """
    B = 26
    ALPH = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    max_mag = 100
    M = 0

    while (N > B**M) & (M <= max_mag):
        M += 1
        
    S = []
    for nada in range(0, M):
        M -= 1
        D = np.int_(np.floor(N / B**M))
        N = N - D * B**M
        S.append(ALPH[D-1])
    
    alpha_N = ''.join(S)
    
    return alpha_N


def alphabet_number_to_integer(N):
    """ convert spreadsheet column lettering to integer """
    ALPH = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    alphanumeric_dictionary = dict(zip(ALPH, np.arange(1, len(ALPH)+1)))
    N = list(N)[::-1]
    numeric_N = 0
    for p in range(0, len(N)):
        numeric_N += alphanumeric_dictionary[N[p]] * 26**p
    return numeric_N


def delay_time(time_delay=1):
    """ approximate time delay funtion for development stuff - probably accruate to 10 ms """
    step_size = 1000
    t0 = time.time()
    for k in range(0, step_size):
        if k == k: pass
    et_4_1step = time.time() - t0
    time_delay = int(time_delay * step_size / et_4_1step  - et_4_1step)
    for k in range(0, time_delay):
        if k == k: pass
    return

def is_prime(n):
    if n % 2 == 0: return False
    for k in range(3, int(np.sqrt(n))+2, 2):
        if n % k == 0: return False
    return True
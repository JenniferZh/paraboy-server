from Crypto.Util import number
import os


def xgcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0


def mul_inv(b, n):
    g, x, _ = xgcd(b, n)
    if g == 1:
        return x % n


def fast_expmod(b, e, m):
    result = 1
    while e != 0:
        if (e&1) == 1:
            # ei = 1, then mul
            result = (result * b) % m
        e >>= 1
        b = (b*b) % m
    return result


def generate_key_pair():

    p = number.getPrime(128, os.urandom)
    q = number.getPrime(128, os.urandom)

    N = p*q
    T = (p-1)*(q-1)
    E = number.getPrime(16, os.urandom)
    while T % E == 0:
        E = number.getPrime(16, os.urandom)

    D = mul_inv(E, T)
    return E, D, N


def sign(m, D, N):
    c = fast_expmod(m, D, N)
    return c

def verify(c, E, N):
    m2 = fast_expmod(c, E, N)
    return m2


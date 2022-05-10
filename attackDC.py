import subprocess
from sage.all import *


onebit = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

# order
q = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

# secret key
d = 0x9C29EDDAEF2C2B4452052B668B83BE6365004278068884FA1AC3F6D0622875C3

if __name__ == "__main__":
    R = IntegerModRing(q)

    h1 = [0]*32
    cmd = f"./dECDSA {bytes(h1).hex()}"
    sig = subprocess.getoutput(cmd)
    r1 = int(sig[:64], 16)
    s1 = int(sig[64:], 16)

    for u in range(256):
        print(f"{u}/255")
        h2 = list(h1)
        h2[u//8] ^= onebit[u%8]
        cmd = f"./dECDSA {bytes(h2).hex()}"
        sig = subprocess.getoutput(cmd)
        r2 = int(sig[:64], 16)
        s2 = int(sig[64:], 16)

        for v in range(256):
            if u == v and u%8 == v%8:
                continue

            M = []
            b = []
            M.append([r1, -s1, 0, 0])
            b.append(-int.from_bytes(bytes(h1), 'big'))
            M.append([r2, -s2, 0, -s2])
            b.append(-int.from_bytes(bytes(h2), 'big'))


            h3 = list(h1)
            h3[v//8] ^= onebit[v%8]

            h4 = list(h1)
            h4[u//8] ^= onebit[u%8]
            h4[v//8] ^= onebit[v%8]

            cmd = f"./dECDSA {bytes(h3).hex()}"
            sig = subprocess.getoutput(cmd)
            r3 = int(sig[:64], 16)
            s3 = int(sig[64:], 16)
            M.append([r3, 0, -s3, 0])
            b.append(-int.from_bytes(bytes(h3), 'big'))

            cmd = f"./dECDSA {bytes(h4).hex()}"
            sig = subprocess.getoutput(cmd)
            r4 = int(sig[:64], 16)
            s4 = int(sig[64:], 16)
            M.append([r4, 0, -s4, -s4])
            b.append(-int.from_bytes(bytes(h4), 'big'))

            M = Matrix(R, M)
            b = vector(R, b)
            a = M.solve_right(b)
            if a[0] == d:
                print("Bravo!")



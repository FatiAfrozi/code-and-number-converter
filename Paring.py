class ParingEncoder:
    def __init__(self):
        pass

    def encode(self, x, y): 
        if (2 ** x) * ((2 * y) + 1) != 0 :
            return (2 ** x) * ((2 * y) + 1) - 1
        else:
            return (2 ** x) * ((2 * y) + 1)

    def decode(self, z):
        z+=1
        x = 0
        while z % 2 == 0:
            z //= 2
            x += 1
        y = (z - 1) // 2
        return x, y
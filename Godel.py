class GodelEncoder:
    def encode(self, number):
        'Godel Encoding'
        number += 1
        exponents = []
        primes = [2]
        i = 3

        while number > 1:
            count = 0
            while number % primes[-1] == 0:
                number //= primes[-1]
                count += 1
            exponents.append(count)
            if number > 1:
                while True:
                    if all(i % p != 0 for p in primes):
                        primes.append(i)
                        break
                    i += 2

        return exponents

    def decode(self, exponents):
        'Godel Decoding'
        primes = [num for num in range(2, len(exponents)**2 + 1) if all(num % i != 0 for i in range(2, int(num**0.5) + 1))]
        x = 1
        for prime, exponent in zip(primes, exponents):
            x *= prime ** exponent
        return x -1
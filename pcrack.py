from crack import crack
from perm import permutations
import time
from concurrent.futures import ProcessPoolExecutor


class Success:

    def __init__(self):
        self.found = False
        self.plaintext = None

    def callback(self, plaintext):
        self.found = True
        self.plaintext = plaintext
        print("The password was found: " + plaintext)


def crack_process(target, length, charset, hashtype):
    cracker = crack.crack_factory[hashtype]
    brute_str_gen = permutations.Permutations(charset, length)
    brute_str_gen.set_current_length(length)
    brute_str_gen.generate_indexes()
    success = Success()
    while brute_str_gen.has_next() and not success.found:
        cracker(target, brute_str_gen.next(), success.callback).check()
    return success.found, success.plaintext


if __name__ == '__main__':

    # Hash to crack
    test_hash = "$2y$04$DkGR2b2RiWSQyPId/N1pn.K3AC.05fhYFvmIHVgfzwNuMJT6peTKC"

    start = time.time_ns()
    found = False
    max_length = 4
    i = 0
    while not found and i <= max_length:
        i += 1
        found, plaintext = crack_process(test_hash, i, "abcdefghijklmnopqrstuvwxyz", "bcrypt")
    end = time.time_ns()

    print("Single threaded cracking took %d nanoseconds" % (end - start))

    charset = "abcdefghijklmnopqrstuvwxyz"
    max_length = 4
    pool_size = 4
    with ProcessPoolExecutor(pool_size) as pool:
        start = time.time_ns()
        i = 0
        while i <= max_length:
            futures = []
            for a in range(0, pool_size):
                i += 1
                future = pool.submit(crack_process, test_hash, i, charset, "bcrypt")
                futures.append(future)
            for future in futures:
                found, plaintext = future.result()
                if found:
                    end = time.time_ns()
                    print("Multi threaded cracking took %d nanoseconds" % (end - start))
                    exit(0)

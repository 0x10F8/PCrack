from crack import crack
from perm import permutations

# Hash to crack
test_hash = "098F6BCD4621D373CADE4E832627B4F6".lower()

# Select the cracker to use
cracker = crack.crack_factory["md5"]

# Setup the string generator
brute_str_gen = permutations.Permutations("abcdefghijklmnopqrstuvwxyz", 4)

# Single thread of cracking (will make multi threaded in near future
found = False
while brute_str_gen.has_next() and not found:
    crack_attempt = cracker(test_hash, brute_str_gen.next())
    found = crack_attempt.test()
    if found:
        print("Password is " + crack_attempt.plaintext_attempt)

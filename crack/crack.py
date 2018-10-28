from abc import abstractmethod
from hashlib import md5, sha1, sha256, sha512
import bcrypt

UTF8 = "UTF8"


class Crack:
    """
    Abstract Crack class, implements the basic constructor for all cracks. And ensures the test method exists in all
    crack classes.
    """

    def __init__(self, target_hash, plaintext_attempt):
        """
        Initialize the crack

        :param target_hash: The target hash
        :param plaintext_attempt: The current plaintext attempt
        """
        self.target_hash = target_hash
        self.plaintext_attempt = plaintext_attempt

    @abstractmethod
    def test(self):
        """
        Abstract test method, should be implemented for each crack.

        :return:  True if the hashed attempt matched the hash
        """
        pass


class HashLibCrack(Crack):
    """
    HashLibCrack provides a basic digest for the hashlib hashes, you just need to provide the hash function in the
    constructor of any implementation.
    """

    def __init__(self, target_hash, plaintext_attempt, digest):
        """
        Initialize the crack with the target hash, plain text attempt and the hashlib hash function.

        :param target_hash: The target hash
        :param plaintext_attempt: The plain text attempt
        :param digest: The hashlib digest function
        """
        super(HashLibCrack, self).__init__(target_hash, plaintext_attempt)
        self.digest = digest

    def test(self):
        """
        Test the hashed plain text against the target hash

        :return: True if matches else false
        """
        hashed_attempt = self.digest(bytes(self.plaintext_attempt, UTF8)).digest().hex()
        if hashed_attempt == self.target_hash:
            return True
        else:
            return False


class MD5Crack(HashLibCrack):
    """
    MD5 implementation of the hashlib crack
    """

    def __init__(self, target_hash, plaintext_attempt):
        super(MD5Crack, self).__init__(target_hash, plaintext_attempt, md5)


class SHA1Crack(HashLibCrack):
    """
    SHA1 implementation of the hashlib crack
    """

    def __init__(self, target_hash, plaintext_attempt):
        super(SHA1Crack, self).__init__(target_hash, plaintext_attempt, sha1)


class SHA256Crack(HashLibCrack):
    """
    SHA256 implementation of the hashlib crack
    """

    def __init__(self, target_hash, plaintext_attempt):
        super(SHA256Crack, self).__init__(target_hash, plaintext_attempt, sha256)


class SHA512Crack(HashLibCrack):
    """
    SHA512 implementation of the hashlib crack
    """

    def __init__(self, target_hash, plaintext_attempt):
        super(SHA512Crack, self).__init__(target_hash, plaintext_attempt, sha512)


class BCryptCrack(Crack):
    """
    BCrypt Crack implementation
    """

    def test(self):
        return bcrypt.checkpw(bytes(self.plaintext_attempt, UTF8), bytes(self.target_hash, UTF8))


# The Factory
crack_factory = {
    "md5": MD5Crack,
    "sha1": SHA1Crack,
    "sha256": SHA256Crack,
    "sha512": SHA512Crack,
    "bcrypt": BCryptCrack
}

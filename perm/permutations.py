class Permutations:

    def __init__(self, charset, max_length):
        self._charset = charset
        self._max_length = max_length
        self._current_length = 1
        self.__generate_indexes()

    def set_current_length(self, current_length):
        self._current_length = current_length

    def set_current_indexes(self, current_indexes):
        self._current_indexes = current_indexes

    def __generate_indexes(self):
        self._current_indexes = [0] * self._current_length
        self._max_indexes = ''.join([(str(len(self._charset) - 1))] * self._current_length)

    def has_next(self):
        return self._current_length <= self._max_length

    def next(self):
        next_output = ''.join([self._charset[i] for i in self._current_indexes])
        if self.__is_max_indexes():
            self._current_length += 1
            self.__generate_indexes()
        else:
            self.__increment_indexes()
        return next_output

    def __increment_indexes(self):
        for i in range(0, len(self._current_indexes)):
            if self._current_indexes[i] == len(self._charset) - 1:
                self._current_indexes[i] = 0
            else:
                self._current_indexes[i] = self._current_indexes[i] + 1
                return

    def __is_max_indexes(self):
        index_str = ''.join(map(str, self._current_indexes))
        return index_str == self._max_indexes

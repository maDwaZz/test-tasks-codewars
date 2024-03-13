# Did you mean ...?
# https://www.codewars.com/kata/5259510fc76e59579e0009d4/train/python

class Dictionary:
    def __init__(self, words):
        self.words = words

    def find_most_similar(self, term):
        min_edit_distance_list = [self.calculate_min_edit_distance(term, word) for word in self.words]
        most_similar_word_index = min_edit_distance_list.index(min(min_edit_distance_list))

        return self.words[most_similar_word_index]

    @staticmethod
    def calculate_min_edit_distance(str1, str2):
        m = len(str1)
        n = len(str2)
        matrix = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            matrix[i][0] = i
        for j in range(n + 1):
            matrix[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    matrix[i][j] = matrix[i - 1][j - 1]
                else:
                    matrix[i][j] = 1 + min(matrix[i - 1][j], matrix[i][j - 1], matrix[i - 1][j - 1])

        return matrix[m][n]

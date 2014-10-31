# Efficient storage of large matrices
# I'd like to use numpy as well

from jarray import array

class Matrix:
    # typecode is an arrays typecode
    def __init__(self, rows, cols, typecode='i', initialVal=-1):
        self.rows = rows
        self.cols = cols
        self._data = array((initialVal for i in xrange(rows * cols)), typecode)

    def set(self, row, col, val):
        self._data[row * self.cols + col] = val

    def get(self, row, col):
        return self._data[row * self.cols + col]

    def setRow(self, row, value):
        # TODO: do some type checking
        self._data[row*self.cols : (row + 1)*self.cols] = value

    def getRow(self, row):
        return self._data[row*self.cols : (row + 1)*self.cols]

    def getCol(self, col):
        ret = array(typecode)

        for row in xrange(self.rows):
            ret[i] = row * self.cols + col

        return ret

# Efficient storage of large matrices
# I'd like to use numpy as well

from array import array

class Matrix:
    # typecode is an arrays typecode
    def __init__(self, rows, cols, typecode='i', initialVal=-1):
        self.typecode = typecode
        self.initialVal = initialVal
        self.rows = rows
        self.cols = cols
        self._data = array(self.typecode, (initialVal for i in xrange(rows * cols)))

    def set(self, row, col, val):
        self._data[row * self.cols + col] = val

    def get(self, row, col):
        return self._data[row * self.cols + col]

    def setRow(self, row, value):
        if len(value) != self.cols:
            raise IndexError, "incorrect length for row assignment"

        self._data[row*self.cols : (row + 1)*self.cols] = value

    def getRow(self, row):
        return self._data[row*self.cols : (row + 1)*self.cols]

    def getCol(self, col):
        ret = array(self.typecode, (self.initialVal for i in xrange(self.rows)))

        for row in xrange(self.rows):
            ret[row] = self._data[row * self.cols + col]

        return ret

if __name__ == '__main__':
    # automated test
    m = Matrix(5, 5)

    try:
        m.setRow(2, array('i', [1]))
    except IndexError:
        print 'PASS Cannot set invalid row'
    else:
        print 'FAIL set invalid row'

    m.setRow(0, array('i', range(5)))
    m.setRow(2, array('i', range(10, 15)))

    if not m.getCol(0)[3] == 3 or not m.getCol(2)[2] == 12:
        print 'FAIL columns mapped incorrectly'

    m.set(4, 4, 82)

    if not m.get(4,4) == 82:
        print 'FAIL set/get'

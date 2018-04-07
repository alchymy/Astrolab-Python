"""
=============
Pyplot Simple
=============
"""
import matplotlib.pyplot as test

"""
format x , y
"""

test.plot([2017.043,2017.123,2017.205,2017.287,2017.372,2017.454,2017.538,2017.624,2017.707,2017.79,2017.874], [28.1,22,25.4,30.4,18.1,18,18.8,25,42.2,16,7.7], 'ro')
test.axis([2017, 2018, 0, 50])

test.ylabel('some numbers')
test.xlabel('more numbers')
test.show()


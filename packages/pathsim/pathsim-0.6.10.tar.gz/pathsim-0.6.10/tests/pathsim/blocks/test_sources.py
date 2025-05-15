########################################################################################
##
##                                  TESTS FOR 
##                             'blocks.sources.py'
##
##                              Milan Rother 2024
##
########################################################################################

# IMPORTS ==============================================================================

import unittest
import numpy as np

from pathsim.blocks.sources import Source, Constant


# TESTS ================================================================================

class TestConstant(unittest.TestCase):
    """
    Test the implementation of the 'Constant' block class
    """

    def test_init(self):

        C = Constant(value=5)

        self.assertEqual(C.value, 5)
        self.assertEqual(C.outputs[0], 0)


    def test_update(self):

        C = Constant(value=5)

        self.assertEqual(C.outputs[0], 0)

        C.update(0)

        self.assertEqual(C.outputs[0], 5)


    def test_reset(self):

        C = Constant(value=5)

        self.assertEqual(C.outputs[0], 0)

        C.update(0)

        self.assertEqual(C.outputs[0], 5)
        
        C.reset()

        self.assertEqual(C.outputs[0], 0)


class TestSource(unittest.TestCase):
    """
    Test the implementation of the 'Source' block class
    """

    def test_init(self):

        def f(t):
            return np.sin(t)

        S = Source(func=f)

        #test if function works
        self.assertEqual(S.func(1), f(1))
        self.assertEqual(S.func(2), f(2))
        self.assertEqual(S.func(3), f(3))

        #test input validation
        with self.assertRaises(ValueError): 
            S = Source(func=2)


    def test_update(self):
        
        def f(t):
            return np.sin(t)

        S = Source(func=f)

        #update block
        err = S.update(1)

        #test if update was correct
        self.assertEqual(S.outputs[0], f(1))

        #test if error is allways 0
        self.assertEqual(err, 0)

        #update block
        err = S.update(2)

        #test if update was correct
        self.assertEqual(S.outputs[0], f(2))

        #test if error is allways 0
        self.assertEqual(err, 0)

        #update block
        err = S.update(3)

        #test if update was correct
        self.assertEqual(S.outputs[0], f(3))

        #test if error is allways 0
        self.assertEqual(err, 0)


# RUN TESTS LOCALLY ====================================================================

if __name__ == '__main__':
    unittest.main(verbosity=2)
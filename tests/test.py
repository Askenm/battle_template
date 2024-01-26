from ..boilerplate.implementation import is_water_system_efficient
import unittest
from ..SoftwareEngineeringSubmodule.Implementation.backend.DataPersistenceService import DBMS

class Test(unittest.TestCase):
    def test_efficient_system(self):
        grid1 = [
            [0, 1, 0, 2, 2],
            [1, 0, 0, 2, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 0, 0, 2]
        ]
        
        self.assertTrue(is_water_system_efficient(grid1))

        grid2 = [
            [0, 1, 0, 2, 2],
            [1, 0, 0, 2, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0]
        ]
        self.assertTrue(is_water_system_efficient(grid2))

        # Add more test cases for efficient systems

    def test_inefficient_system(self):
        grid1 = [
            [0, 1, 0, 2, 2],
            [1, 0, 0, 2, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 2]
        ]
        self.assertFalse(is_water_system_efficient(grid1))

        grid2 = [
            [0, 1, 0, 2, 2],
            [1, 0, 0, 2, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 2]
        ]
        self.assertFalse(is_water_system_efficient(grid2))

        # Add more test cases for inefficient systems

    def test_empty_grid(self):
        grid = []
        self.assertTrue(is_water_system_efficient(grid))

    def test_single_pump(self):
        grid = [[1]]
        self.assertTrue(is_water_system_efficient(grid))

    def test_single_pipe(self):
        grid = [[2]]
        self.assertFalse(is_water_system_efficient(grid))

    def test_multiple_pumps(self):
        grid = [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]
        ]
        self.assertTrue(is_water_system_efficient(grid))

        grid = [
            [1, 0, 1],
            [0, 0, 0],
            [1, 0, 1]
        ]
        self.assertTrue(is_water_system_efficient(grid))

    def test_no_pumps(self):
        grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.assertFalse(is_water_system_efficient(grid))


def run_tests():
    # Create a test suite and run the tests
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    # Get the number of passes and number of failures
    num_passes = result.testsRun - len(result.failures)
    num_failures = len(result.failures)

    score = round(num_passes/(num_passes+num_failures)*100,2)

    return score


def main():
    
    score = run_tests()

    # UPLOAD RESULTS TO DB
    # Find commit id
    # Find github name of repository holder

    # UPLOAD NOTIFICATION TO MESSAGE BOARD





if __name__ == '__main__':
    main()
    

    

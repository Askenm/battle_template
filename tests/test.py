from boilerplate.implementation import is_water_system_efficient
import unittest
from .support.DataPersitenceService import DBMS
import json

class Test(unittest.TestCase):
    """
    TESTS HERE
    """

def run_tests():
    # Create a test suite and run the tests
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    # Get the number of passes and number of failures
    num_passes = result.testsRun - len(result.failures)
    num_failures = len(result.failures)

    score = round(num_passes/(num_passes+num_failures)*100,2)

    return score

def get_group_name():
    f = json.loads(open('boilerplate/group_info.json','r').read())
    return f['group_name'],f['battle_name']


def main():
    
    score = run_tests()

    # UPLOAD RESULTS TO DB
    # Find commit id
    # Find github name of repository holder

    DBMS_ = DBMS()
    group_name,battle_name = get_group_name()


    df = DBMS_.read('GET_GROUP_ID_FROM_GROUP_NAME',{'_GROUP_NAME_':group_name,
                                                     '_BATTLE_NAME_':battle_name})
    
    gid = df['gid'].values[0]
    bid = df['bid'].values[0]

    submission_info = {'_SCORE_':score,
                       '_GROUP_ID_':gid,
                       '_BATTLE_ID_':bid}
    
    
    DBMS_.write('ASSIGN_AUTOMATIC_SCORE',submission_info)

    # UPLOAD NOTIFICATION TO MESSAGE BOARD
    # TODO put this in backend_main





if __name__ == '__main__':
    main()
    

    

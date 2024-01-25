import os 
import random 
from DataPersistenceService import DBMS

DBMS_ = DBMS()



battle_data = {
            '_BATTLE_NAME_': 'HVAD KÆMPER VI FOR (SEJR)',
            '_BATTLE_DESC_': 'Hvis du kan læse det her så er jeg en big mfing boss',
            '_TOURNAMENT_ID_':'29',
            '_BATTLE_REPO_': 'vinder.com',
            '_BATTLE_CREATOR_': '42',
            '_END_DATE_': '2024-23-04'
        }
DBMS_.write('CREATE_BATTLE',battle_data)

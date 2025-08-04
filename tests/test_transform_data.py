import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import transform_data

def test_join():
    clean_data = transform_data.clean_data()
    print(clean_data)
    
    
if __name__ == "__main__":
    test_join()

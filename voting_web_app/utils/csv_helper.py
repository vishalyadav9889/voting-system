import pandas as pd
import os

DATA_DIR = 'data'

def initialize_csv():
    """Ye function app.py call kar raha hai"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    # Users CSV setup
    user_file = os.path.join(DATA_DIR, 'users.csv')
    if not os.path.exists(user_file):
        df = pd.DataFrame(columns=['username', 'password', 'role', 'has_voted'])
        df.to_csv(user_file, index=False)

    # Candidates CSV setup
    cand_file = os.path.join(DATA_DIR, 'candidates.csv')
    if not os.path.exists(cand_file):
        df = pd.DataFrame(columns=['cid', 'name', 'party', 'vote_count'])
        df.to_csv(cand_file, index=False)

def read_csv(filename):
    return pd.read_csv(os.path.join(DATA_DIR, filename))

def write_csv(filename, df):
    df.to_csv(os.path.join(DATA_DIR, filename), index=False)
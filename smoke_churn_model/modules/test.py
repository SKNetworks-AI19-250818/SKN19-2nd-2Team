import os 
from pathlib import Path
current_path=os.getcwd()
print(os.path.abspath(os.path.join(os.path.join(current_path, 'smoke_churn_model'))))
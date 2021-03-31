import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
  load_dotenv(dotenv_path)
  TOKEN = os.getenv('TOKEN')
  FORLDER_ID = os.getenv('FORLDER_ID')
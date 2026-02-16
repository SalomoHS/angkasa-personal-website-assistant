import os
from dotenv import load_dotenv
load_dotenv()
print("TES: ", os.getenv('GOOGLE_API_KEY'))
print("fsdf: ", os.environ.get("GOOGLE_API_KEY"))

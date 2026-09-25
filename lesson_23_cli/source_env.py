import os
from dotenv import load_dotenv

load_dotenv()


host = os.getenv("DATABASE")

print(host)
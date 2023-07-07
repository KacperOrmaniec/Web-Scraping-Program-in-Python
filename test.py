#Sprawdzanie czy import z .env działaF


import os
from dotenv import load_dotenv

load_dotenv()

PROXY = os.getenv('PROXY')
INPUT_URL = os.getenv('INPUT_URL')
OUTPUT_FILE = os.getenv('OUTPUT_FILE')

print(INPUT_URL)
print(PROXY)
print(OUTPUT_FILE)
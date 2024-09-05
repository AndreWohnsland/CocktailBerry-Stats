import os

from dotenv import load_dotenv

load_dotenv()
is_dev = os.getenv("DEBUG") is not None
CONNECTION_STRING = os.environ["ATLAS_URI"]

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from flaskr.dynamo_handler import clear_user_closet
from flaskr.s3_session import clear_user_directory

if len(sys.argv) < 2:
    print("Usage: python python_script.py <email>")
    sys.exit(1)

# get user email from command line argument
email = os.sys.argv[1]

clear_user_closet(email)
clear_user_directory(email)

print(f"User {email} closet cleared successfully!")

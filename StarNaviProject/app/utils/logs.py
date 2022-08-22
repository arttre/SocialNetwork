import os
from dotenv import load_dotenv, find_dotenv

from datetime import datetime

load_dotenv(find_dotenv())


def compose_user_login_log(user_id: int, login_datetime: datetime):
    return f"[{login_datetime}] {user_id} USER SIGNED IN\n"


def compose_user_service_request_log(user_id: int, last_request_datetime: datetime):
    return f"[{last_request_datetime}] {user_id} USER SENT SERVICE REQUEST\n"


def write_user_logs(user_log: str):
    with open(os.environ['LOGS_FILE_PATH'], 'a') as f:
        f.write(user_log)


def find_user_last_login_log(user_id: int):
    with open(os.environ['LOGS_FILE_PATH'], 'r') as f:
        logs_list = f.read().split('\n')
        logs_list.reverse()
        for line in logs_list:
            if f"{user_id} USER SIGNED IN" in line:
                return line.split("]")[0][1:]


def find_user_last_service_request_log(user_id: int):
    with open(os.environ['LOGS_FILE_PATH'], 'r') as f:
        logs_list = f.read().split('\n')
        logs_list.reverse()
        for line in logs_list:
            if f"{user_id} USER SENT SERVICE REQUEST" in line:
                return line.split("]")[0][1:]

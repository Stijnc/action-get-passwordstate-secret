import os
import sys
from contextlib import redirect_stdout

from dotenv import load_dotenv
from passwordstate import Password, Passwordstate


def main():
    load_dotenv()

    url = os.getenv("INPUT_URL") or sys.argv[1]
    token = os.getenv("INPUT_TOKEN") or sys.argv[2]
    password_list_id = os.getenv("INPUT_PASSWORDLIST_ID") or sys.argv[3]
    secrets = os.getenv("INPUT_SECRET") or sys.argv[4]
    match_field = os.getenv("INPUT_MATCH_FIELD") or sys.argv[5] or "UserName"
    GITHUB_ENV = os.getenv("GITHUB_ENV")

    api = Passwordstate(url=url, token=token)
    secretArray = secrets.split(",")
    for secret in secretArray:
        password = Password(
            api, password_list_id, {"field": match_field, "field_id": secret}
        )
        # set secret, set variable, set output
        print(f"::add-mask::{password.password}")
        print(f"::set-output name={password.title}_username::{password.username}")
        print(f"::set-output name={password.title}_password::{password.password}")
        with open(GITHUB_ENV, "a") as out:
            with redirect_stdout(out):
                print(f"{password.title}_username={password.username}")
                print(f"{password.title}_password={password.password}")


if __name__ == "__main__":
    main()

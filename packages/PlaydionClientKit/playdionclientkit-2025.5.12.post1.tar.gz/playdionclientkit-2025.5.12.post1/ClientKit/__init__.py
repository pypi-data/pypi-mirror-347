from pathlib2 import Path

def info():
    print("Playdion ClientKit v2025.5.12post1")



def check_login():
    accfile = Path("userdata.txt")
    if accfile.is_file():
        with open("userdata.txt", "r") as accfile:
            userid = accfile.read()
            if userid is not None or "":
                return True
            else:
                return False
    else:
        return False


def get_user_id():
    state = check_login()
    if state is True:
        with open("userdata.txt", "r") as accfile:
            userid = accfile.read()
            return userid
    else:
        return False


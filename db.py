import random
import sqlite3
import string
import time
import inspect
from functools import wraps
from configuration import database as db
from configuration import main as cnf
from patterns_handler import validate_data as vd


# database decorator
def db_handle(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = None
        connection = sqlite3.connect(db.filename)
        cursor = connection.cursor()
        try:
            if 'connection' in inspect.getfullargspec(f)[0]:
                result = f(*args, **kwargs, cursor=cursor, connection=connection)
            else:
                result = f(*args, **kwargs, cursor=cursor)
        except sqlite3.Error as error:
            print(f"'\033[96m'|{f.__name__}| SQL error -> ", error, "\033[95m")
        except BaseException as error:
            print(f"'\033[96m'|{f.__name__}| Python error -> ", error, "\033[95m")
        if 'connection' not in inspect.getfullargspec(f)[0]:
            cursor.close()
            connection.commit()
            connection.close()
        return result

    return wrapper


# write token to bd
@db_handle
def commit_token(id: int, token: str, cursor=None):
    print(id, token)
    query = cursor.execute('''insert into Tokens(UserId, Token) VALUES ((?),(?))''', (id, token)).fetchall
    print(query)
    if query == 'None':
        return False
    return True


@db_handle
def validate_token(id: int, token: str, cursor=None):
    query = cursor.execute('''select * from Tokens WHERE Token=(?) and UserId=(?)''', (token, id)).fetchall()
    return bool(query)


# generate token
def generate_token(id, need_save=True):
    part1 = str(hash(time.time()))
    part1 = part1.replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d").replace("5", "e")
    part1 = part1.replace("6", "f").replace("7", "g").replace("8", "h").replace("9", "i")
    part2 = "".join(random.choices(string.digits + string.ascii_lowercase, k=15))
    token = "s.ch." + part1 + "." + part2
    if need_save:
        commit_token(id, token)
    return token


@db_handle
def try_reg(email: str, password: str, cursor=None):
    json_scheme = {
        'value-list': {
            'email': email,
            'password': password
        },
        'error-list': {},
        'already-register': False
    }
    # 'error-list': { 'email': None, 'password': None }

    if vd(email, "email") is not True:
        json_scheme['error-list']['email'] = vd(email, "email")[1]

    if vd(password, "password") is not True:
        json_scheme['error-list']['password'] = vd(password, "password")[1]

    # check registration available
    already_reg = cursor.execute('''select * from General WHERE email = (?)''', (email,)).fetchone()
    if already_reg:
        json_scheme['already-register'] = True

    return json_scheme


# registry user, part 1
@db_handle
def registry(email: str, password: str, cursor=None, connection=None):
    # validating values
    errors = []
    if vd(email, "email") is not True:
        errors.append([1, vd(email, "email")[1]])
    if vd(password, "password") is not True:
        errors.append([2, vd(password, "password")[1]])
    # check registration available
    already_reg = cursor.execute('''select * from General WHERE email = (?)''', (email, )).fetchone()
    if already_reg:
        errors.append([1, "already registered"])

    if errors:
        return False, errors

    # registering in General
    cursor.execute('''insert into General (email, password) VALUES (?, ?)''', (email, password))
    _id = cursor.execute('''select id from General order by id desc limit 1''').fetchone()[0]
    cursor.close()
    connection.commit()
    connection.close()
    token = generate_token(_id)
    return True, _id, token


# registry user, part 2
@db_handle
def registry_2(id: int, firstname: str, lastname: str, avatar, cursor=None):
    # validating errors
    errors = []
    if vd(firstname, "email") is not True:
        errors.append([1, vd(firstname, "email")[1]])
    if vd(lastname, "password") is not True:
        errors.append([2, vd(lastname, "password")[1]])

    if errors:
        return False, errors

    # update General data
    cursor.execute('''UPDATE General SET firstname = (?), lastname = (?) where id=(?)''',
                   (firstname, lastname, id))
    # save avatar
    avatar.save(f'{cnf.path_to_save_pictures}/id{id}')
    print(f'saved file in : {cnf.path_to_save_pictures}/id{id}')


@db_handle
def login(email, password, cursor=None, connection=None):
    reg = cursor.execute('''select * from General WHERE email = (?)''', (email,)).fetchone()
    if reg is None:
        return False, [1, "not registered"]
    print(reg)
    print(f"try: select id from General WHERE email = {email} and password = {password}")
    auth = cursor.execute('''select id from General WHERE
        email = (?) and
        password = (?)''', (email, password)).fetchone()
    if auth is None:
        return False, [2, "password incorrect"]
    id = auth[0]
    cursor.close()
    connection.commit()
    connection.close()
    token = generate_token(id)
    return True, id, token


if __name__ == "__main__":
    print(login('admin@tochno.ru', '1234'))

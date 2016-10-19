import getpass
import re


MINIMUM_PASSWORD_LENGTH = 8

def case_sensitive(password):
    return re.search(r'[A-ZА-Я]', password) is not None \
    and re.search(r'[a-zа-я]', password) is not None

def includes_digits(password):
    return re.search(r'[0-9]', password) is not None

def includes_letters(password):
    return re.search(r'[A-Za-zА-Яа-я]', password) is not None

def includes_special_chars(password):
    return re.search(r'[\W]', password) is not None

def load_blacklist(filepath):
    with open(filepath, 'r') as text_file:
        data = text_file.read()
    return re.findall(r'\w+', data)

def get_blacklist_filepath():
    return input("Введите адрес текстового файла " +
        " cо списком запрещённых паролей\n(можно оставить пустым):\n")

def appears_in_blacklist(password):
    while(True):
        try:
            blacklist_filepath = get_blacklist_filepath()
            if blacklist_filepath:
                return password in load_blacklist(blacklist_filepath)
        except Exception:
            continue
        else:
            break
    return False

def get_length_points(password):
    password_length = len(password)
    points = 0 if password_length < MINIMUM_PASSWORD_LENGTH \
    else round((password_length - MINIMUM_PASSWORD_LENGTH) / 4 + 0.5)
    return points

def calculate_password_strength(password):
    password_strength = 1

    if len(password) < MINIMUM_PASSWORD_LENGTH: return password_strength
    
    if appears_in_blacklist(password): return password_strength

    if includes_letters(password) \
    and includes_digits(password): password_strength += 2

    if case_sensitive(password): password_strength += 2

    if includes_special_chars(password): password_strength += 1

    password_strength += get_length_points(password)
    
    if password_strength > 10: password_strength = 10

    return password_strength


if __name__ == '__main__':
    while True:
        password = getpass.getpass(prompt="Введите пароль для проверки:\n", stream=None)
        if password: break
    password_strength = calculate_password_strength(password)
    print("Оценка пароля:%d/10." % password_strength)

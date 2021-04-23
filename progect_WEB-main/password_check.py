per = {'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', # соответствие латиницы и кирилицы на клавиатуре
       'i': 'ш', 'o': 'щ', 'p': 'з', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а',
       'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', 'z': 'я', 'x': 'ч',
       'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь'}
st = ['1234567890', 'йцукенгшщзхъ', 'фывапролджэё', 'ячсмитьбю'] # ряды цифр и букв на клавиатуре


def sequence(p): # вычисляет есть ли в строке три символа(букв или цифр), стоящих рядом на клавиатуре
    for i in range(len(p) - 2):
        s = ''
        for j in p[i:i + 3]:
            if j in per:
                s += per[j]
            else:
                s += j
        for j in st:
            if s in j:
                return True
    return False


def check_new_password(password): # проверяет подходит ли пароль пользователя требованиям системы
    if len(password) < 8:
        return 'Пароль должен быть длиной не менее 8 символов'
    if password.islower() or password.isupper() or not any(map(str.isalpha, password)):
        return 'В пароле долны быть хоят бы одна буква в верхнем регисте и одна в маленьком'
    if not any(map(str.isdigit, password)):
        return 'В пароле должна быть хотя бы одна цифра'
    if sequence(password.lower()):
        return 'В пароле не должно быть 3 идущих подряд на клавиатуре символа'
    return False

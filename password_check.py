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
    if len(password) < 9:
        return 'Пароль должен быть длиной более 8 символов'
    if password.islower() or password.isupper() or not any(map(str.isalpha, password)):
        return 'В пароле долны быть хоят бы одна буква в верхнем регисте и одна в маленьком'
    if not any(map(str.isdigit, password)):
        return 'В пароле должна быть хотя бы одна цифра'
    if sequence(password.lower()):
        return 'В пароле не должно быть 3 идущих подряд на клавиатуре символа'
    return False
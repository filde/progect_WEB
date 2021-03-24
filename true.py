  def check_new_password(password): # проверяет подходит ли пароль пользователя требованиям системы
    if len(password) < 9:
        raise PasswordError('Пароль должен быть длиной более 8 символов')
    if password.islower() or password.isupper() or not any(map(str.isalpha, password)):
        raise PasswordError('В пароле долны быть хоят бы одна буква в верхнем регисте и одна в маленьком')
    if not any(map(str.isdigit, password)):
        raise PasswordError('В пароле должна быть хотя бы одна цифра')
    if sequence(password.lower()):
        raise PasswordError('В пароле не должно быть 3 идущих подряд на клавиатуре символа')

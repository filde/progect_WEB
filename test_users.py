from requests import get, post, delete, put # Файл для проверки работоспособности API для пользователей


print(get('http://localhost:5000/api/users').json())
print(get('http://localhost:5000/api/users/1').json())
print(get('http://localhost:5000/api/users/99999999').json())
print(get('http://localhost:5000/api/users/fhdskj').json())

# нет никаких данных
print(post('http://localhost:5000/api/users').json())

# не все поля
print(post('http://localhost:5000/api/users',
           json={'name': 'Oleg'}).json())

print(post('http://localhost:5000/api/users',
           json={'surname': 'Ivanov',
                 'name': 'Ivan', 
                 'age': 23,
                 'about': 'colonist',
                 'email': 'ivan@mail.ru',
                 'password': 'ivan'}).json())

print(get('http://localhost:5000/api/users').json())

# не существует пользователя
print(put('http://localhost:5000/api/users/100000000',
        json={'surname': 'Ivanov',
                'name': 'Ivan', 
                'age': 50,
                'about': 'colonist',
                'email': 'ivan@mail.ru',
                'password': 'ivan'}).json())

# нет данных для изменения
print(put('http://localhost:5000/api/users/5').json())

print(put('http://localhost:5000/api/users/5',
          json={'surname': 'Karavaev',
                 'name': 'Oleg', 
                 'age': 50,
                 'about': 'colonist',
                 'email': 'ivan@mail.ru',
                 'password': 'ivan'}).json())

print(get('http://localhost:5000/api/users').json())

# пользователя не существует
print(delete('http://localhost:5000/api/users/999').json())

print(delete('http://localhost:5000/api/users/5').json())

print(get('http://localhost:5000/api/users').json())
from requests import get, post, delete, put # Файл для проверки работоспособности API для проектов


print(get('http://localhost:5000/api/projects').json())
print(get('http://localhost:5000/api/projects/1').json())
print(get('http://localhost:5000/api/projects/99999999').json())
print(get('http://localhost:5000/api/projects/fhdskj').json())

# нет никаких данных
print(post('http://localhost:5000/api/projects').json())

# не все поля
print(post('http://localhost:5000/api/projects',
           json={'title': 'Oleg'}).json())

print(post('http://localhost:5000/api/projects',
           json={'title': 'drfgjhk',
                 'team_lead': 1,
                 'count': 20,
                 'about': '2, 3',
                 'active': False}).json())

print(get('http://localhost:5000/api/projects').json())

# не существует работы
print(put('http://localhost:5000/api/projects/100',
          json={'title': 'drfgjhk',
                'team_lead': 1,
                'count': 70,
                'about': '1, 3',
                'active': False}).json())

# нет данных для изменения
print(put('http://localhost:5000/api/projects/4').json())

print(put('http://localhost:5000/api/projects/4',
          json={'title': 'drfgjhk',
                'team_lead': 1,
                'count': 70,
                'about': '1, 3',
                'active': False}).json())

print(get('http://localhost:5000/api/projects').json())

# работы не существует
print(delete('http://localhost:5000/api/projects/999').json())

print(delete('http://localhost:5000/api/projects/4').json())

print(get('http://localhost:5000/api/projects').json())
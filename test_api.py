from requests import get, post, delete
# создане поста без аргументов
print(post('http://localhost:5000/api/posts').json())
# получение списка постов
print(get('http://localhost:5000/api/posts').json())
# получение конкретного поста по его id
print(get('http://localhost:5000/api/post/24').json())
#создание поста
print(post('http://localhost:5000/api/posts',
           json={'title': 'Заголовsdfок',
                 'content': 'Текст ноsdfsвости',
                 'user_id': 1,
                 'slug': '1234',
                 'is_private': False,
                 'is_published': True}).json())
# удаление поста
print(delete('http://localhost:5000/api/post/25').json())

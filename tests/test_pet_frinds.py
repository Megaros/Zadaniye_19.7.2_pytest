from  api import PetFriends
from settings import mail, password
import os


pf = PetFriends()

def test_get_api_key_for_valid_user(mail = mail, password = password):
    status, result = pf.get_api_key(mail, password)
    assert status== 200
    assert 'key' in result
    print('\n')
    print(result)
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
       Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
       запрашиваем список всех питомцев и проверяем что список не пустой.
       Доступное значение параметра filter - 'my_pets' либо '' """
    _,auth_key = pf.get_api_key(mail, password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status==200
    assert  len(result['pets']) >0

def test_add_new_pet_with_valid_data(name='Шурик', animal_type='кошка',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(mail, password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(mail, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(mail, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_get_api_key_for_no_valid_user(mail = mail, password = "123"):
    '''Проверяем возможность получения ключа с невалидным паролем'''
    status, result = pf.get_api_key(mail, password)
    assert status!= 200
    assert 'key' not in result
    print('\n')
    print('\033[33m{}\033[0m'.format("Ключ не получен, вход не выполнен"))
def test_no_valid_key():
    '''Проверяем поведение запроса при невалидном ключе'''
    # Получаем ключ auth_key
    _,auth_key = pf.get_api_key(mail, password)
    #меняем ключ
    auth_key = '123456'
    #Пытаемся запросить список питьмцев
    try:
        status, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    except:
        print('\n')
        my_pets = None
    assert my_pets == None
    print('\n')
    print('\033[33m{}\033[0m'.format('список не удалось получить\n'))
    print('my_pets =',my_pets)
def test_great_importance_age(name='Мурзик', animal_type='Котэ', age=5000000):
    '''Проверяем поведение запроса при большом значении переменной age'''
    # Получаем ключ auth_key и список питомцев
    _,auth_key = pf.get_api_key(mail, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и возраст питомца соответствует заданному
        assert status == 200
        assert result['age'] == '5000000'
        print('\n')
        print('\033[33m{}\033[0m'.format('Переменная age может быть большим числом\n'))
        print('age =', result['age'])
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_no_data(name='', animal_type='', age= ''):
    '''Проверяем поведение запроса при  отсутствии значения переменной'''
    # Получаем ключ auth_key и список питомцев
    _,auth_key = pf.get_api_key(mail, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его возраст при age=None
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        #  Значения переменных age, name, animal_type
        assert result['age'] != ''
        assert result['name'] != ''
        assert result['animal_type'] != ''
        print('\n')
        print('\033[33m{}\033[0m'.format('Если переменная не имеет значения, то данные на сервере '
                                         'не изменяютя\n'))
        print('age =', result['age'])
        print('name =', result['name'])
        print('animal_type =', result['animal_type'])
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
def test_data_space(name=' ', animal_type=' ', age= ' '):
    '''Проверяем поведение запроса при  значения переменной равной пусто'''
    # Получаем ключ auth_key и список питомцев
    _,auth_key = pf.get_api_key(mail, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его возраст при age=None
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        #  Значения переменных age, name, animal_type
        assert result['age'] == ' '
        assert result['name'] == ' '
        assert result['animal_type'] == ' '
        print('\n')
        print('\033[33m{}\033[0m'.format('Если переменная  имеет значение "пусто", то данные на сервере '
                                         'изменяютя на "пусто"\n'))
        print('age =', result['age'])
        print('name =', result['name'])
        print('animal_type =', result['animal_type'])
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
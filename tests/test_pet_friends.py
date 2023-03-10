import os.path

import requests

from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Лось', animal_type='кот', age='3', pet_photo='images/cat.png'):
    """Проверяем что можно добавить питомца с валидными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Боб", "кот", "5", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Соня', animal_type='кошка', age=7):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

def test_add_new_pet_without_photo_with_valid_data(name='Вася', animal_type='кот', age='10'):
    """Проверяем что можно добавить питомца без фото с валидными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_photo_of_pet_with_valid_data(pet_photo = 'images/cat2.jpg'):
    """Проверяем что можно добавить фото к существующему питомцу"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    if len(my_pets['pets']) == 0:
        pf.add_new_pet_without_photo(auth_key, "Боб", "кот", "5")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']

def test_get_api_key_with_valid_mail_and_invalid_passwor(email=valid_email, password=invalid_password):
    """Проверяем наличие ключа в ответе при запросе
    с валидным email и c невалидным паролем."""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_with_invalid_email_and_valid_password(email=invalid_email, password=valid_password):
    """Проверяем наличие ключа в ответе при запросе
    с невалидным email и c валидным паролем."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result

def test_get_api_key_with_invalid_mail_and_invalid_passwor(email=invalid_email, password=invalid_password):
    """Проверяем наличие ключа в ответе при запросе
    с невалидным email и c невалидным паролем."""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_add_pet_with_invalid_age(name='Bill', animal_type='Кот', age = '-1', pet_photo='images/cat2.jpg'):
    """Проверяем возможность добавления питомца с невалидными данными(отрицательное число) в поле 'age'."""

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    age = float(result['age'])

    assert status == 200
    assert (age < 0)
    print('Добавлен питомец с возрастом меньше 0.')

def test_add_pet_with_invalid_age_2(name='Bill', animal_type='Кот', age = 'abc', pet_photo='images/cat2.jpg'):
    """Проверяем возможность добавления питомца с невалидными данными(буквы) в поле 'age'"""

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert age
    print('Добавлен питомец с нечисловыми данными в поле возраст')

def test_add_pet_with_invalid_data_empty_fields(name='', animal_type='', age=''):
    """Проверяем возможность добаления питомца с пустыми полями."""

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('Добавлен питомец с пустыми значениями')

def test_add_pet_with_invalid_animal_type(name='Bill', animal_type='*?/|<>,.()[]{};:!@#$^&', age='1'):
    """Проверяем возможность добавления питомца с невалидными данными(спецсимволы) в поле 'animal_type'."""

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('Добавлен питомец с невалидными данными в поле animal_type.')

def test_add_pet_with_invalid_name(name='*?/|<>,.()[]{};:!@#$^&', animal_type='кот', age='1'):
    """Проверяем возможность добавления питомца с невалидными данными(спецсимволы) в поле 'name'."""

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('Добавлен питомец с невалидными данными в поле name.')

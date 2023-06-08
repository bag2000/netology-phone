# netology-phone
[main.py](https://github.com/bag2000/netology-phone/blob/main/main.py)  
[Модуль PSApi](https://github.com/bag2000/netology-phone/blob/main/psapi.py)  
  
Api для работы с Postgress  
  
    from psapi import PSApi
    api = PSApi(database='test', user='postgres', password='postgres', host='127.0.0.1')  
  
    Параметры:  
    :param database: название базы данных  
    :param user: имя пользователя  
    :param password: пароль  
    :param host: сервер  
  
    Функции:  
    drop_tables(self): удаление таблиц phonenumber и client.  
    make_tables(self): создание таблиц phonenumber и client.  
    add_client(self, fistname, lastname, email, phonenumber=None): позволяет добавить нового клиента.  
    get_id_client(self, email): позволяет получить id клиента по почте.  
    get_id_phonenumber(self, phonenumber): позволяет получить id клиента по номеру телефона.  
    add_phone_to_exist_client(self, email, phonenumber): позволяет добавить телефон для существующего клиента.  
    update_data(self, email, firstname=None, lastname=None, phonenumber=None, change_phonenumber=None):  
        позволяет изменить данные о клиенте.  
    update_email(self, email, change_email): позволяет изменить почту клиента.  
    del_phone(self, phonenumber): позволяет удалить телефон для существующего клиента.  
    del_client(self, email): позволяет удалить существующего клиента.  
    search_client(self, firstname=None, lastname=None, email=None, phonenumber=None):  
        позволяет найти клиента по его данным: имени, фамилии, email или телефону.  

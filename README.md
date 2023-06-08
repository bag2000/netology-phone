# netology-phone
Модуль PSApi  
Api для работы с Postgress  
  
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

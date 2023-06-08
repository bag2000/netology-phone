import psycopg2


class PSApi:
    """
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
    """

    def __init__(self, database: str, user: str, password: str, host: str):
        self.database = database
        self.user = user
        self.password = password
        self.host = host

    def make_conn(self):
        """
        Функция для установления подключения к базе данных
        :return: объект psycopg2.connect
        """
        conn = psycopg2.connect(database=self.database,
                                user=self.user,
                                password=self.password,
                                host=self.host)
        return conn

    def drop_tables(self):
        """
        Функция для удаление таблиц phonenumber и client
        """

        conn = self.make_conn()

        with conn.cursor() as cur:
            cur.execute("""
            DROP TABLE IF EXISTS phonenumber;
            DROP TABLE IF EXISTS client;
            """)
        conn.commit()
        print('Удалены таблицы phonenumber и client')

    def make_tables(self):
        """
        Функция для создания таблиц phonenumber и client
        """
        conn = self.make_conn()

        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS phonenumber(
                phone_number_id SERIAL PRIMARY KEY,
                phone_number DECIMAL NOT NULL UNIQUE,
                client_id INTEGER REFERENCES client(client_id)
                
            );
            """)
        conn.commit()
        print('Созданы таблицы client, phonenumber')

    def add_client(self, fistname, lastname, email, phonenumber=None):
        """
        Функция, позволяющая добавить нового клиента.
        :param fistname: имя
        :param lastname: фамилия
        :param email: почта
        :param phonenumber: телефонный номер, опционально
        """
        conn = self.make_conn()

        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    INSERT INTO client(first_name, last_name, email) VALUES('{fistname}', '{lastname}', '{email}');
                """)
            conn.commit()
            print(f'Добавлен новый клиент {fistname} {lastname} {email}')
        except Exception as e:
            if type(e).__name__ == 'UniqueViolation':
                print(f'Запись с почтой {email} уже существует!')
            return e

        if phonenumber is not None:
            self.add_phone_to_exist_client(email=email, phonenumber=phonenumber)

    def get_id_client(self, email):
        """
        Функция позволяющая получить id клиента по почте
        :param email: электронная почта
        :return: кортеж с id клиента или None (если клиент не найден)
        """

        conn = self.make_conn()

        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT c.client_id FROM client c WHERE c.email=%s;
            """, (f'{email}',))
            return cur.fetchone()

    def get_id_phonenumber(self, phonenumber):
        """
        Функция позволяющая получить id телефона по номеру телефона
        :param phonenumber: телефонный номер
        :return: кортеж с id номера или None (если номер не найден))
        """
        conn = self.make_conn()

        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT p.phone_number_id FROM phonenumber p WHERE p.phone_number=%s;
            """, (f'{phonenumber}',))
            return cur.fetchone()

    def add_phone_to_exist_client(self, email, phonenumber):
        """
        Функция, позволяющая добавить телефон для существующего клиента.
        :param email: электронная почта
        :param phonenumber: телефонный номер
        """
        conn = self.make_conn()

        client_id = self.get_id_client(email)
        if client_id is not None:
            try:
                with conn.cursor() as cur:
                    cur.execute(f"""
                        INSERT INTO phonenumber(phone_number, client_id) VALUES('{phonenumber}', '{client_id[0]}');
                    """)
                conn.commit()
                print(f'Добавлен номер телефона {phonenumber} клиенту, с почтовым адресом {email}')
            except Exception as e:
                if type(e).__name__ == 'UniqueViolation':
                    print(f'Телефонный номер {phonenumber} уже существует!')
                else:
                    return e
        else:
            print(f'Клиент с почтой {email} не существует!')

    def update_data(self, email, firstname=None, lastname=None, phonenumber=None, change_phonenumber=None):
        """
        Функция, позволяющая изменить данные о клиенте.
        :param email: действующий почтовый адрес
        :param firstname: новое имя
        :param lastname: новая фамилия
        :param phonenumber: номер телефона который нужно заменить
        :param change_phonenumber: новый номер телефона
        """
        conn = self.make_conn()

        client_id = self.get_id_client(email)

        if client_id is not None:
            if firstname is not None:
                with conn.cursor() as cur:
                    cur.execute(f"""
                        UPDATE client SET first_name=%s WHERE client_id=%s;
                    """, (firstname, client_id[0]))
                conn.commit()
                print(f'Изменено имя на {firstname} у клиента с почтой {email}')

            if lastname is not None:
                with conn.cursor() as cur:
                    cur.execute(f"""
                        UPDATE client SET last_name=%s WHERE client_id=%s;
                    """, (lastname, client_id[0]))
                conn.commit()
                print(f'Изменена фамилия на {lastname} у клиента с почтой {email}')

            if phonenumber is not None:
                phonenumber_id = self.get_id_phonenumber(phonenumber)
                if phonenumber_id is not None:
                    if change_phonenumber is not None:
                        with conn.cursor() as cur:
                            cur.execute(f"""
                                UPDATE phonenumber SET phone_number=%s WHERE phone_number_id=%s;
                            """, (change_phonenumber, phonenumber_id[0]))
                        conn.commit()
                        print(f'Изменен телефон на {change_phonenumber} у клиента с почтой {email}')
                    else:
                        print('Необходимо ввести новый телефон, change_phonenumber=\'\'')
                else:
                    print(f'Номер телефона {phonenumber} не найден!')
        else:
            print(f'Клиент с почтовым адресом {email} не найден')

    def update_email(self, email, change_email):
        """
        Функция, позволяющая изменить почту клиента.
        :param email: действующая почта
        :param change_email: новая почта
        """
        conn = self.make_conn()

        client_id = self.get_id_client(email)
        if client_id is not None:
            if change_email is not None:
                with conn.cursor() as cur:
                    cur.execute(f"""
                        UPDATE client SET email=%s WHERE client_id=%s;
                    """, (change_email, client_id[0]))
                conn.commit()
                print(f'Изменена почта на {change_email} у клиента с почтой {email}')
            else:
                print('Необходимо ввести новую почту, change_email=\'\'')
        else:
            print(f'Клиент с почтовым адресом {email} не найден')

    def del_phone(self, phonenumber):
        """
        Функция, позволяющая удалить телефон для существующего клиента.
        :param phonenumber: телефонный номер
        """

        conn = self.make_conn()

        phone_id = self.get_id_phonenumber(phonenumber)

        if phone_id is not None:
            with conn.cursor() as cur:
                cur.execute(f"""
                    DELETE FROM phonenumber WHERE phone_number_id=%s;
                """, (phone_id[0],))
            conn.commit()
            print(f'Удален номер телефона {phonenumber}')
        else:
            print(f'Номер телефона {phonenumber} не найден!')

    def del_client(self, email):
        """
        Функция, позволяющая удалить существующего клиента.
        :param email:
        """
        conn = self.make_conn()

        client_id = self.get_id_client(email=email)

        if client_id is not None:
            with conn.cursor() as cur:
                cur.execute(f"""
                    DELETE FROM phonenumber WHERE client_id=%s;
                """, (client_id[0],))
            conn.commit()

            with conn.cursor() as cur:
                cur.execute(f"""
                    DELETE FROM client WHERE client_id=%s;
                """, (client_id[0],))
            conn.commit()
            print(f'Удален клиент с почтой {email}')
        else:
            print(f'Клиент с почтой {email} не найден!')

    def search_client(self, firstname=None, lastname=None, email=None, phonenumber=None):
        """
        Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
        :param firstname: имя, опционально
        :param lastname: фамилия, опционально
        :param email: почта, опционально
        :param phonenumber: телефонный номер, опционально
        :return: fetchall(), список кортежей с данными о найденых клиентах
        """

        count_msg = 0  # количество элементов для поиска, для того чтобы добавить в комманду - AND
        command = ''  # команда для отправки в SQL для поиска

        conn = self.make_conn()

        if firstname is not None:
            if count_msg == 0:
                command = command + f' c.first_name=\'{firstname}\''
                count_msg += 1
            else:
                command = command + f' AND c.first_name=\'{firstname}\''

        if lastname is not None:
            if count_msg == 0:
                command = command + f' c.last_name=\'{lastname}\''
                count_msg += 1
            else:
                command = command + f' AND c.last_name=\'{lastname}\''

        if email is not None:
            if count_msg == 0:
                command = command + f' c.email=\'{email}\''
                count_msg += 1
            else:
                command = command + f' AND c.email=\'{email}\''

        if phonenumber is not None:
            if count_msg == 0:
                command = command + f' p.phone_number=\'{phonenumber}\''
                count_msg += 1
            else:
                command = command + f' AND p.phone_number=\'{phonenumber}\''

        with conn.cursor() as cur:
            cur.execute(f"""
                SELECT c.first_name, c.last_name, c.email, p.phone_number
                FROM client c LEFT JOIN phonenumber p
                ON c.client_id = p.client_id
                WHERE{command};
            """)
            return cur.fetchall()

from psapi import PSApi


if __name__ == "__main__":
    # api = PSApi(database='test', user='postgres', password='postgres', host='127.0.0.1')
    # api.drop_tables()
    # api.make_tables()
    # api.add_client(fistname='Roman', lastname='Polyakov', email='polyakov.r.v@yandex.ru', phonenumber='79266828586')
    # api.add_client(fistname='Roman2', lastname='Polyakov2', email='polyakov.r.v@yandex.ru2')
    # api.add_phone_to_exist_client(email='polyakov.r.v@yandex.ru2', phonenumber='79266828587')
    # api.update_data(email='polyakov.r.v@yandex.ru', firstname='Romeo',
    #                 phonenumber='79266828587', change_phonenumber='79266828588')
    # api.update_email(email='polyakov.r.v@yandex.ru', change_email='polyakov_change.r.v@yandex.ru')
    # api.del_phone('79266828586')
    # api.del_client(email='polyakov.r.v@yandex.ru2')
    # print(api.search_client(firstname='Romeo'))

    print(PSApi.__doc__)

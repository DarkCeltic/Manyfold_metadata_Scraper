import configparser

import psycopg2

config = configparser.ConfigParser()
# Read the configuration file
config.read('config.ini')

# Access values from the configuration file
db_name = config.get('Database', 'database')
db_host = config.get('Database', 'host')
db_port = config.get('Database', 'port')
db_password = config.get('Database', 'password')
db_user = config.get('Database', 'user')

conn = psycopg2.connect(database=db_name,
                        user=db_user,
                        host=db_host,
                        password=db_password,
                        port=db_port)

cur = conn.cursor()


def get_model_info_from_db(filename):
    cur.execute(
        'SELECT m.id, creator_id, license, array(select url FROM public.links where linkable_type = \'Model\' '
        'and linkable_id = m.id) as model_urls, (select name from public.creators c where c.id = m.creator_id), '
        'array(select url FROM public.links where linkable_type = \'Creator\' and linkable_id = m.creator_id) as '
        'creator_urls FROM public.models m where path like (\'%' + filename + '\');')
    # TODO add a check here if larger than one should throw error
    return turn_sql_to_dict()


def get_model_links_from_db(model_id):
    cur.execute('SELECT url ' +
                'FROM links where linkable_id =' + str(model_id) + ' and linkable_type = \'Model\';')
    return cur.fetchall()


def get_creator_links_from_db(creator_id):
    cur.execute('SELECT url ' +
                'FROM links where linkable_id =' + str(creator_id) + ' and linkable_type = \'Creator\';')
    return cur.fetchall()


def get_creator(creator_id: str):
    cur.execute(
        'SELECT name FROM creators where id = ' + creator_id + ';')
    return cur.fetchall()[0][0]


def check_if_creator_exist(creator_name: str, creator_url: str):
    cur.execute(
        'SELECT id, name, created_at, updated_at, notes, caption, slug, public_id, name_lower FROM public.creators ' +
        'where name like \'' + creator_name + '\' or id in (select linkable_id from links where url like \'' + creator_url + '\');')
    return turn_sql_to_dict()


def add_missing_creator_to_db(creator_name, creator_id):
    cur.execute(
        'INSERT INTO creators (id, name, created_at, updated_at, slug) values(' + creator_id + ', \'' + creator_name +
        '\',current_timestamp,current_timestamp,\'' + str.lower(creator_name) + '\');')
    conn.commit()


def create_creator(creator_name, public_id):
    cur.execute('SELECT id ' +
                'FROM creators where name = \'' + creator_name + '\';')
    result = cur.fetchall()
    if len(result) != 0:
        return result[0]
    cur.execute(
        'INSERT INTO creators (name, created_at, updated_at, slug, public_id) values(\'' + creator_name +
        '\',current_timestamp,current_timestamp,\'' + str.lower(creator_name) + '\', \'' + public_id + '\');')
    conn.commit()
    cur.execute('SELECT id ' +
                'FROM creators where name = \'' + creator_name + '\';')
    return cur.fetchall()


def add_creator_to_links_table(creator_id, creator_url):
    try:
        cur.execute(
            'INSERT INTO links (url,linkable_type, linkable_id, created_at, updated_at) values (\'' + creator_url +
            '\',\'Creator\',' + str(creator_id) + ',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)')
    except psycopg2.errors.SyntaxError as d:
        print(d)
    except Exception as e:
        print(e)
    conn.commit()


def add_creator_to_model(creator_id, model_id):
    try:
        cur.execute('UPDATE models set creator_id = ' + str(creator_id) + ' where id = ' + str(model_id) + ';')
    except psycopg2.errors.SyntaxError as d:
        print(d)
    except Exception as e:
        print(e)
    conn.commit()


def add_model_to_links_table(model_url, model_id):
    cur.execute(
        'INSERT INTO links (url,linkable_type, linkable_id, created_at, updated_at) values (\'' + model_url +
        '\',\'Model\',' + str(model_id) + ',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP)')
    conn.commit()


def add_license_to_model(model_id, model_license):
    cur.execute('UPDATE models set license = \'' + str(model_license) + '\' where id = ' + str(model_id) + ';')
    conn.commit()


def turn_sql_to_dict():
    desc = cur.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row))
            for row in cur.fetchall()]
    return data


def close_connection():
    cur.close()
    conn.close()

import json


# function use for fixing reserved keywords
# here we have only key "user" which is reserved but iam just writing it in more generic form.
def fix_key(key):
    return '"' + key + '"'


# insert data into table
def inset_data(json_file):
    # get table name from json file name
    table_name = str(json_file).split("/")[-1][:-6]

    # because user is reserved keys word in postgres
    # so we have to add "" around that name
    if table_name == 'user':
        table_name = fix_key(table_name)

    # open file to read data from it
    with open(json_file) as json_data:
        record_list = json.load(json_data)

    # get the column names from the first record
    columns = [list(x.keys()) for x in record_list][0]

    # again fixing reserved keyword
    for i, j in enumerate(columns):
        if j == 'user':
            columns[i] = fix_key(j)

    # writing query for creating table
    sql_string = create_table(table_name, columns)

    # writing query of insert of data
    sql_string = sql_string + 'INSERT INTO {} '.format(table_name)
    sql_string += "(" + ', '.join(columns) + ")\nVALUES "

    # enumerate over the record
    for i, record_dict in enumerate(record_list):

        # iterate over the values of each record dict object
        values = []
        for col_names, val in record_dict.items():
            if type(val) == str:
                val = val.replace("'", "''")
                val = "'" + val + "'"

            values += [str(val)]
        # join the list of values and enclose record in parenthesis
        sql_string += "(" + ', '.join(values) + "),\n"

    # remove the last comma and end statement with a semicolon
    sql_string = sql_string[:-2] + ";"

    # So that is our final query which will drop table if it already exists and then insert data into that table
    # print(sql_string)
    return sql_string


# creating table dynamically with table name and columns.
def create_table(table_name, columns):
    # writing query for droping table if it already exists
    create_sql = "DROP TABLE IF EXISTS {}".format(table_name) + ';\n'

    # creating table
    create_sql += 'CREATE TABLE {} '.format(table_name) + "( "
    for i in columns:
        if "id" in i:
            # making first column as PRIMARY KEY if its name is id.
            # just make it by looking at data
            create_sql += i + " VARCHAR(255) PRIMARY KEY,"
        elif "Date" in i:
            create_sql += i + " timestamp,"
        else:
            create_sql += i + " VARCHAR(255),"
    create_sql = create_sql[:-1] + ');\n'
    return create_sql

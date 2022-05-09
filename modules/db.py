# import json, json_config
# from mysql.connector import (connection)
# from mysql.connector import Error


# config = json_config.connect('./config/config.json')

# create_table_query = """CREATE TABLE IF NOT EXISTS `userTable` (
# 	`tg_id` INT(255) NOT NULL UNIQUE,
# 	`user_name` VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
# 	`sub_flag` BOOLEAN NOT NULL DEFAULT '0',
# 	PRIMARY KEY (`tg_id`)
# ) ENGINE=InnoDB;"""


# class BotDatabase:

#     def __init__(self) -> None:
#         self.cnx = connection.MySQLConnection(
#             user = config['db_user'],
#             password = config['db_pass'],
#             host = config['db_host'],
#             database = config['db_base']
#         )
#         self.cursor = self.cnx.cursor()
        

#     def create_table(self):
#         try: 
#             self.cursor.execute(create_table_query)
#             print('Создана или загружена таблица для базы данных ')
#         except Error as e:
#             print(e)


#     def get(self, tg_id: int):
#         query = "SELECT * FROM userTable WHERE tg_id = {}".format(tg_id)
#         try:
#             self.cursor.execute(query)
#             result = self.cursor.fetchall()
#             if len(result) != 0:
#                 response = json.dumps(
#                     {
#                         "id": result[0][0],
#                         "name": result[0][1],
#                         "flag": result[0][2]
#                     }, indent=4, ensure_ascii=False
#                 )
#                 return response
#             if len(result) == 0:
#                 print('Не существует в базе данных или не найден')
#                 return 0
#         except Error as e:
#             print(e)
#             return 0

#     def set(self, tg_id: int, name: str):
#         query = "INSERT INTO userTable (tg_id, user_name) VALUES (%s, %s)"
#         val = (tg_id, name)
#         try:
#             self.cursor.execute(query, val)
#             self.cnx.commit()
#             print(f'id{tg_id} добавлен в базу данных')
#         except Error as e:
#             print(e)
#             return 0


#     def updateFlag(self, tg_id: int):
#         query = "UPDATE userTable SET sub_flag  = 1 WHERE tg_id = {}".format(tg_id)
#         try:
#             self.cursor.execute(query)
#             self.cnx.commit()
#             print("Флаг изменен")
#         except Error as e:
#             print(e)
    
#     def deleteFlag(self, tg_id: int):
#         query = "UPDATE userTable SET sub_flag  = 0 WHERE tg_id = {}".format(tg_id)
#         try:
#             self.cursor.execute(query)
#             self.cnx.commit()
#             print("Флаг изменен")
#         except Error as e:
#             print(e)

#     def getFlag(self, tg_id: int):
#         query = "SELECT sub_flag FROM userTable WHERE tg_id = {}".format(tg_id)
#         try:
#             self.cursor.execute(query)
#             result = self.cursor.fetchall()
#             flag = int(result[0][0])
#             return flag
#         except Error as e:
#             print(e)
#             return False


#     def disconnect(self):
#         return self.cnx.close()

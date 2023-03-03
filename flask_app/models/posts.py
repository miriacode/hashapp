from re import S
from flask_app.config.mysqlconnection import SqlConnection
from flask import flash

class Post:
    conexion = SqlConnection()

    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.owner_id = data['owner_id']
        #Recibira una instancia de User

        self.users = []


    #CREATE ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def create_post(cls, data):
        query = "INSERT INTO posts (content, owner_id) VALUES (%(content)s, %(owner_id)s)"
        if not cls.conexion.ejecutar(query, data):
            cls.conexion.rollback()
            return False
        query = f'select id from posts order by id desc'
        ids = cls.conexion.consulta_asociativa(query)
        if ids:
            return ids[0]['id']
        return False



    #READ (ALL) -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # @classmethod
    # def get_all_posts(cls):
    #     query = "SELECT * FROM posts"
    #     result = SqlConnection('hashapp_schema').query_db(query)
    #     posts = []
    #     for r in result:
    #         post = cls(r)
    #         posts.append(post)
    #     return posts

    @classmethod
    def get_all_posts_with_info(cls):
        query = "SELECT posts.id, name, username, profile_image, content, posts.created_at, owner_id FROM users INNER JOIN posts ON users.id = owner_id ORDER BY posts.id DESC;"
        result = cls.conexion.consulta_asociativa(query)
        print('////////////////////////////////////////////')
        print(result)
        return result

    #VALIDATE -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def validate_post(post):
        is_valid = True
        #Validar que mi nombre de la receta sea mayor a 3 caracteres
        if len(post['content']) < 1:
            flash('Content should have at least one character', 'post')
            is_valid = False
        return is_valid


    #READ (One) (by ID)
    # @classmethod
    # def get_post_with_info_by_id(cls, data):
    #     #data = {"id": "1"}
    #     print(data)
    #     query = "SELECT name, username, content, posts.created_at FROM users LEFT JOIN posts ON users.id = owner_id WHERE posts.id = %(id)s"
    #     result = SqlConnection('hashapp_schema').query_db(query, data)
    #     print(result)
    #     #tttttttttttttt     pt = result[0]
    #     #Changing date format
    #     #rcp['date_made'] = rcp['date_made'].strftime("%B, %d, %Y")
    #     #tttttttttttttt  post = cls(pt)
    #     return result


    #READ (One) (by ID)
    @classmethod
    def get_post_by_id(cls, data):
        #data = {"id": "1"}
        print(data)
        query = "SELECT * FROM posts WHERE id = %(id)s"
        result = cls.conexion.consulta_asociativa(query, data)
        print(result)
        pt = result[0]
        #Changing date format
        #rcp['date_made'] = rcp['date_made'].strftime("%B, %d, %Y")
        post = cls(pt)
        return post
from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask import flash



class User:
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.bio = data['bio']
        self.profile_image = data['profile_image']
        self.bg_image = data['bg_image']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.posts = []    
        
    #FOR REGISTER------------------------------------------------------------------------------------------------------------
    #CREATE
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (name, username, email, password, bio, profile_image, bg_image) VALUES (%(name)s, %(username)s, %(email)s, %(password)s, %(bio)s, %(profile_image)s, %(bg_image)s)"
        new_user_id = connectToMySQL('hashapp_schema').query_db(query, data)
        return new_user_id


    #VALIDATE
    @staticmethod
    def validate_user(user):
        #METERLE AJAX!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        is_valid = True
        #Check if the first name has more than 2 characters
        if len(user['name']) < 2:
            flash('First name should have at least 2 characters', 'register')
            is_valid = False
        #Check if the last name has more than 2 characters
        if len(user['username']) < 2:
            flash('User name should have at least 2 characters', 'register')
            is_valid = False
        #Validate email with regex
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email', 'register')
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match", 'register')
            is_valid = False
        #Check if the email already exists
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('hashapp_schema').query_db(query, user)
        if len(results) >= 1:
            flash('Email has been already registered', 'register')
            is_valid = False
        #Check if the username is in use
        query = "SELECT * FROM users WHERE username = %(username)s"
        results = connectToMySQL('hashapp_schema').query_db(query, user)
        if len(results) >= 1:
            flash('Username is already in use', 'register')
            is_valid = False

        return is_valid

    #FOR LOGIN ------------------------------------------------------------------------------------------------------------
    #READ (ONE) (By email) 
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('hashapp_schema').query_db(query, data)
        if len(result) < 1:
            return False
        else :
            usr = result[0]
            user = cls(usr)
            return user

    #FOR DASHBOARD ------------------------------------------------------------------------------------------------------------
    #READ (ONE) (By ID)
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('hashapp_schema').query_db(query, data)
        usr = result[0]
        user = cls(usr)
        return user

    @classmethod
    def get_all_users(cls):
        query =" SELECT * FROM users"
        results = connectToMySQL('hashapp_schema').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users


    @classmethod
    def get_user_by_username(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s"
        result = connectToMySQL('hashapp_schema').query_db(query, data)
        usr = result[0]
        user = cls(usr)
        return user



    #UPDATE 
    @classmethod
    def update_user(cls, form):
        query = "UPDATE users SET name=%(name)s, bio=%(bio)s, bg_image=%(bg_image)s, profile_image=%(profile_image)s WHERE users.id=%(id)s"
        result = connectToMySQL('hashapp_schema').query_db(query, form)
        return result
    #READ
    # @classmethod
    # def get_ninjas_by_dojo_id(cls, data):
    #     query = "SELECT * FROM ninjas WHERE dojo_id = %(dojo_id)s"
    #     results = connectToMySQL('dojos_y_ninjas').query_db(query,data)
    #     ninjas =[]
    #     print(results)
    #     for n in results:
    #         #Lo obligo a que sea instancia de ninjas, ahora tenemos un ninj relleno en todos los campos, pero con un self.dojo= None
    #         ninj = cls(n)
    #         data = {
    #             "id": ninj.dojo_id
    #         }
    #         returnedDojo = Dojo.get_dojo_by_id(data)
    #         ninj.dojo = returnedDojo
    #         #Ya esta listo y se inserta a la lista
    #         ninjas.append(cls(n))
        
    #     return ninjas
import os

class Config:
    SECRET_KEY = os.urandom(24)
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'  # Tu usuario de MySQL
    MYSQL_PASSWORD = ''  # Tu contraseña de MySQL
    MYSQL_DB = 'tienda'  # Nombre de tu base de datos

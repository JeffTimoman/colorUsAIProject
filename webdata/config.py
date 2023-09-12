

class Config:
    def __init__(self):
        self.DB_PLATFORM = 'mysql+pymysql'
        self.DB_SERVER = 'localhost'
        self.DB_NAME = 'colorus'
        self.DB_USERNAME = 'root'
        self.DB_PASSWORD = ''
        self.DB_PORT = '3306'
        self.UPLOAD_FOLDER = 'webdata/static/uploads'
        self.API_KEY = 'isi sendiri ya'
        
        self.SECRET_KEY = 'This is a secret key'
        
        self.DB_URL = f"{self.DB_PLATFORM}://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}"
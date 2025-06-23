# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:q@localhost:5432/buku'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
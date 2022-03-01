class Config:
    # CSRF secret key
    SECRET_KEY = 'WO_ist_DIE_SPEISEKARTE'

    # location of database
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

    # setting tracking of modification on the terminal to false
    SQLALCHEMY_TRACK_MODIFICATIONS = False

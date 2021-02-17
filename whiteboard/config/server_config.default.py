import os

SECRET_KEY = 'p9Bv<3Eid9%$i01'

""" Use pymysql instead MySQLdb, because MySQLdb is not supported by Python3 """
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:12@whiteboard_db/whiteboard_db'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test_test_test:123456@localhost/test_test_db'

GOOGLE_ID = "501008858890-hpf8bmp9j35nf23u6hep2etfqstt0uof.apps.googleusercontent.com"
GOOGLE_SECRET = "9Xu_XQwDPvDHk9URVkfu0Sne"

s_key = os.urandom(66)

# TOKEN_SECRET= str(s_key)
TOKEN_SECRET = "asdasd"

"""######################### COURSE PICTURE DIR CONFIG ######################"""
B_DATA_FILES_DIR = "/b_data/"
UPLOAD_FOLDER = "/courses_data/"
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
HOST = "http://lvh.me:8081/"

"""######################### PRESENTATION DIR CONFIG ########################"""
PRESENT_ALLOWED_EXTENSIONS = set(["ppt", "otp", "odp"])
# PRESENT_UPLOAD_FOLDER = "/home/peio_jr/projects/whiteboard_project/whiteboard/static/presentations/"
# PRESEND_HANDLER_HOST = "http://127.0.0.1:5501/api/pHandler"

"""########################### ADMIN LOGIN CONFIG ###########################"""
BASIC_AUTH_USERNAME = 'john'
BASIC_AUTH_PASSWORD = '1'

"""######################### MODERATOR LOGIN CONFIG #########################"""
MODERATOR_TOKEN_SECRET = "sdba"

"""############################## EMAIL CONFIG ##############################"""
FROM_ADDR = "whiteboard.me.team@gmail.com"
EMAIL_PASS = "wh1tebo@rd"
SMTP_SERVER = "smtp.gmail.com"
SMTP_SERVER_PORT = 587

"""######################## STRIP CONFIGS (PAYMENTS) ########################"""
STRIPE_SECRET_KEY = 'sk_test_5pLcFkNbWW5TNDEphOKlxBzu'
STRIPE_PUBLISHABLE_KEY = 'pk_test_HPJgXc0TcHkXr6XGuE7T3TFL'

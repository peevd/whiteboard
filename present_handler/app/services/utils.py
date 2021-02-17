from flask_restful import reqparse


"""+++++++++++++++++++++++   AUTHENTICATION CHECK   ++++++++++++++++++++++++"""


parser = reqparse.RequestParser()
parser.add_argument("Authorization",
                    location="headers", required=True)

"""+++++++++++++++++++++++++++   FILE CHECK/GET   +++++++++++++++++++++++++++"""


# Check is file extension is in allowed register
def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


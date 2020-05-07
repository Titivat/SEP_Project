from server.model import user

class AuthController(object):

    @staticmethod
    def validate_credentials(username, password):
        u = user.User.query.filter(user.User.username==username).first()
        if not u:
            return False
        return u.verify_password(password)

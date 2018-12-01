import bcrypt

class PasswordUtility():
    def getHashedPassword(password):
        return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    def checkHashedPassword(password, hashedPassword):
        return bcrypt.checkpw(password.encode('utf8'), hashedPassword)

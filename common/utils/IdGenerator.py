import string
import random

'''Genrates Random IDs'''
class IdGenerator():

    '''Generates a random ID'''
    def generate():
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        size = 16
        return ''.join(random.choice(chars) for _ in range(size))

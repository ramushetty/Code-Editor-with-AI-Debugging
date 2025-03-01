import random
import string

def generate_room_number(length=6):
    """Generate a random alphanumeric room number."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
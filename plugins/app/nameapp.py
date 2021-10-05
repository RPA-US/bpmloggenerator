import random
from plugins.string.random_text_lorem import generate_words


def generate_app_demo():
    """Generate a random word with a random number as app name
    """
    # Generate a random word with a random number as app name
    return generate_words()+str(random.randint(0,1000))

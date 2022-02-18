import random
from plugins.text.random_text_lorem import generate_words


def generate_app_demo(args):
    """Generate a random word with a random number as app name
    """
    # Generate a random word with a random number as app name
    apps = ["Firefox", "Safari", "Chrome", "Word", "Excel", "PowerPoint", "Internet Explorer", "Edge", "LibreOffice", "Adobe Acrobat Reader", "Teams", "Thunderbird", "Microsoft Visual Code", "Zoom", "CRM"]
    random_item = random.choice(apps)
    return random_item

def generate_lorem_app_demo(args):
    """Generate a random word with a random number as app name
    """
    # Generate a random word with a random number as app name
    return generate_words([])+str(random.randint(0,1000))
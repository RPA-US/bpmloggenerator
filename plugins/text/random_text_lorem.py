from lorem_text import lorem
import random
from bpmloggenerator.settings import sep


# nombres = ["Sofía", "Juan", "María", "Luis", "Ana", "Carlos", "Lucía", "José", "Camila", "Diego", "Elena", "Gabriel", "Isabel", "Fernando", "Julia", "Héctor", "Irene", "Javier", "Laura", "Kevin", "Marta", "Leonardo", "Nuria", "Óscar", "Patricia", "Raúl", "Silvia", "Tomás", "Úrsula", "Víctor", "Yolanda", "Xavier", "Zoe", "Aarón", "Beatriz", "César", "Daniela", "Eduardo", "Fátima", "Gustavo", "Helena", "Iván", "Joana", "Kike", "Lidia", "Manuel", "Noa", "Olivia", "Pablo", "Queralt", "Ricardo", "Sara", "Toni", "Ubaldo", "Valeria", "Waldo", "Xenia", "Yago", "Zaira", "Adrián", "Blanca", "Cristian", "Diana", "Ernesto", "Flora", "Silvia", "Gerardo", "Hilda", "Ian", "Jana", "Kai", "Leonor", "Matías", "Nadia", "Omar", "Paloma", "Quim", "Rebeca", "Sergio", "Tania", "Ursula", "Vanesa", "Wilfredo", "Ximena", "Yeray", "Zara", "Alicia", "Borja", "Clara", "Damián", "Eva", "Félix", "Gloria", "Hugo", "Inés", "Joel", "Karen", "Leo", "Mireia", "Néstor", "Olga", "Pepe", "Raquel", "Samuel", "Teresa", "Úrsula", "Violeta", "Wilson", "Xilena", "Yuri", "Zacarías", "Amalia", "Bernardo", "Carmen", "David", "Esther", "Fabián", "Gracia", "Ignacio", "Jessica", "Kurt", "Luna", "Miguel", "Nicolás", "Octavio", "Paula", "Ramón", "Susana", "Teo", "Verónica", "Wendy", "Xander", "Yasmina", "Zeno", "Ariadna", "Bruno", "Carla", "Daniel", "Elisa", "Felipe", "Gema", "Héctor", "Iris", "Jon", "Kristina", "Lorenzo", "Melissa", "Norberto", "Oriol", "Penélope", "Rubén", "Sofía", "Tristán", "Úrsula", "Valentín", "Wanda", "Xavier", "Yolanda", "Zac", "Alba", "Benjamín", "Celia", "Dario", "Elsa", "Fausto", "Gisela", "Hilario", "India", "Jordi", "Kiara", "Liam", "Mónica", "Nolan", "Odette", "Pau", "Rita", "Salvador", "Tatiana", "Uriel", "Vega", "Wilma", "Xilo", "Yvette", "Zurich"]
nombres_sin_acentos = [
    "Sofia", "Juan", "Maria", "Luis", "Ana", "Carlos", "Lucia", "Jose", "Camila", "Diego",
    "Elena", "Gabriel", "Isabel", "Fernando", "Julia", "Hector", "Irene", "Javier", "Laura", "Kevin",
    "Marta", "Leonardo", "Nuria", "Oscar", "Patricia", "Raul", "Silvia", "Tomas", "Ursula", "Victor",
    "Yolanda", "Xavier", "Zoe", "Aaron", "Beatriz", "Cesar", "Daniela", "Eduardo", "Fatima", "Gustavo",
    "Helena", "Ivan", "Joana", "Kike", "Lidia", "Manuel", "Noa", "Olivia", "Pablo", "Queralt",
    "Ricardo", "Sara", "Toni", "Ubaldo", "Valeria", "Waldo", "Xenia", "Yago", "Zaira", "Adrian",
    "Blanca", "Cristian", "Diana", "Ernesto", "Flora", "Silvia", "Gerardo", "Hilda", "Ian", "Jana", "Kai",
    "Leonor", "Matias", "Nadia", "Omar", "Paloma", "Quim", "Rebeca", "Sergio", "Tania", "Ursula",
    "Vanesa", "Wilfredo", "Ximena", "Yeray", "Zara", "Alicia", "Borja", "Clara", "Damian", "Eva",
    "Felix", "Gloria", "Hugo", "Ines", "Joel", "Karen", "Leo", "Mireia", "Nestor", "Olga", "Pepe",
    "Raquel", "Samuel", "Teresa", "Ursula", "Violeta", "Wilson", "Xilena", "Yuri", "Zacarias", "Amalia",
    "Bernardo", "Carmen", "David", "Esther", "Fabian", "Gracia", "Ignacio", "Jessica", "Kurt", "Luna",
    "Miguel", "Nicolas", "Octavio", "Paula", "Ramon", "Susana", "Teo", "Veronica", "Wendy", "Xander",
    "Yasmina", "Zeno", "Ariadna", "Bruno", "Carla", "Daniel", "Elisa", "Felipe", "Gema", "Hector",
    "Iris", "Jon", "Kristina", "Lorenzo", "Melissa", "Norberto", "Oriol", "Penelope", "Ruben", "Sofia",
    "Tristan", "Ursula", "Valentin", "Wanda", "Xavier", "Yolanda", "Zac", "Alba", "Benjamin", "Celia",
    "Dario", "Elsa", "Fausto", "Gisela", "Hilario", "India", "Jordi", "Kiara", "Liam", "Monica",
    "Nolan", "Odette", "Pau", "Rita", "Salvador", "Tatiana", "Uriel", "Vega", "Wilma", "Xilo", "Yvette",
    "Zurich"
]

apellidos = [
    "Garcia", "Martinez", "Rodriguez", "Lopez", "Hernandez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Cruz",
    "Flores", "Gomez", "Morales", "Vazquez", "Diaz", "Reyes", "Mendoza", "Torres", "Ortiz", "Gutierrez",
    "Jimenez", "Ruiz", "Alvarez", "Moreno", "Castillo", "Romero", "Herrera", "Medina", "Aguilar", "Castro",
    "Ramos", "Fernandez", "Guzman", "Munoz", "Mendez", "Salazar", "Soto", "Delgado", "Pacheco", "Vega",
    "Dominguez", "Contreras", "Silva", "Macias", "Avila", "Salinas", "Rojas", "Serrano", "Nunez", "Maldonado",
    "Valdez", "Cortes", "Padilla", "Acosta", "Galvan", "Santos", "Reynoso", "Guerrero", "Franco", "Escobar",
    "Barrera", "Navarro", "Molina", "Solis", "Luna", "Juarez", "Cabrera", "Rivas", "Santiago", "Rosales",
    "Campos", "Ponce", "Lara", "Villanueva", "Zamora", "Cardenas", "Navarrete", "Arias", "Velasco", "Martines",
    "Granados", "Cano", "Fuentes", "Cervantes", "Bautista", "Villegas", "Sandoval", "Ortega", "Marquez",
    "Zuniga", "Rangel", "Orozco", "Tovar", "Montes", "Trevino", "Valencia", "Tellez", "Varela", "Rios",
    "Rosas", "Enriquez", "Pineda", "Saldana", "Marin", "Gallegos", "Vera", "Andrade", "Rincon", "Ochoa",
    "Palacios", "Guerra", "Castañeda", "De la Cruz", "Villarreal", "Quezada", "Peralta", "Salgado", "Vargas",
    "Benitez", "Montoya", "Estrada", "Valenzuela", "Mora", "Delacruz", "Guillen", "Alvarado", "Cerda", "Rocha",
    "Venegas", "Zarate", "Ojeda", "Bravo", "Aguirre", "Paz", "Solano", "Esquivel", "Guevara", "Mejia",
    "Arellano", "Marroquin", "Lugo", "Pena", "Palacio", "Guajardo", "Uribe", "Limon", "Ledesma", "Barajas",
    "Lazaro", "Sosa", "Zavala", "Miranda", "Mata", "Romo", "Peña", "Duran", "Vasquez", "Saucedo", "Barraza",
    "Becerra", "Cordero", "Espinoza", "Robles", "Olivares", "Maldonado", "Regalado", "Gil", "Valle",
    "Camacho", "Salas", "Olvera", "Galindo", "Mares", "Chavez", "Aguilera", "Merino", "Tirado", "Colin",
    "Valles", "Villalobos", "Arroyo", "Cazares", "Nava", "Yanez", "Quintana", "Leon", "Leyva", "Alcaraz",
    "Puga", "Rueda", "Vidal", "Benavides", "Alonso", "Huerta", "Blanco", "Quiroz", "Varas", "Aragon",
    "Corona", "Villa", "Madero", "Rendon", "Cano", "Puentes", "Ley", "Tamayo", "Sotelo", "Olivas",
    "Calderon", "Galvez", "Herrero", "Zepeda", "Sierra", "Godoy", "Aguayo", "Villagomez", "Zaragoza"
]


# Not in the populate
def generate_words(args):
    '''
    Generate words. The argument is the number of words to generate.
    args:
        words: number of words to be generated. The default argument is 1 word.
    '''
    if args  == []:
        words=1
    else:
        words = int(args[0])
    text = lorem.words(words)
    return text


# Not in the populate
def generate_sentence(args):
    '''
    Generate one sentence.
    '''
    text =  lorem.sentence()
    return text

# Not in the populate
def generate_paragraph(args):
    '''
    Generate paragraphs. The argument is the number of paragraphs to generate.
    args:
        para: number of paragraphs to be generated
    '''
    if args  == []:
        para=1
    else:
        para = int(args[0])
    text =  lorem.paragraphs(para)
    return text

# Not in the populate
def generate_path(args):
    '''
    Generate path. The argument is the level of path and the extension
    args:
        ext: the extension if is the path of a file 
        value: number of levels of the path
    '''
    if args  == []:
        value=1
        ext=None
    else:
        value=int(args[1])
        ext=str(args[0])
    res = "C:"+sep+generate_words()
    for i in range(1,value):        
        res += sep+generate_words()
    if ext is not None:
        res += ext
    return res

# Not in the populate
def generate_random_entity(args):
    '''
    Generate a word with first letter capital 
    '''
    if args == []:
        words=1
    else:
        words = int(args[0])
    text = lorem.words(words).capitalize() 
    return text

# Not in the populate
def generate_clipboard_content(args):
    '''
    Generate text or paths for the paperclip content.
    '''
    res = None
    value = random.randint(1,0)
    if value == 1:
        res = generate_sentence()
    else:
        res = generate_path()
    return res

#   Function digits_text, generate a random number with the number of digits specified in the arguments.
def digits_text(args):
    '''
    Generate a number with the number of digits specified in the arguments.
    args:
        digits: number of digits of the number to be generated
    '''
    if args == []:
        digits = 1
    else:
        digits = int(args["number_of_digits"])
    value = random.randint(10**(digits-1),10**digits-1)
    return str(value)

#  Function generate_DNI, generate a spanish id card number
def generate_DNI(args):
    '''
    Generate spanish number identification.
    '''
    DNI = 0
    value = random.randint(1,99999999)
    number_control = value%23
    value = str(value)
    letters = {0:"T",1:"R",2:"W",3:"A",4:"G",5:"M",6:"Y",7:"F",8:"P",9:"D",10:"X", 11:"B",12:"N",13:"J",14:"Z",15:"S",16:"Q",17:"V",18:"H",19:"L",20:"C",21:"K",22:"E"}
    for i in range(0,(8-len(value))): value="0"+value
    DNI = str(value)+letters[number_control]
    return DNI

def person_name_text(args):
    '''
    Generate a person name.
    '''
    global nombres_sin_acentos
    number_of_names = int(args["text_number_of_names"])
    number_of_surnames = int(args["text_number_of_surnames"])
    res = [random.choice(nombres_sin_acentos) for _ in range(number_of_names)]
    res += [random.choice(apellidos) for _ in range(number_of_surnames)]
    return ' '.join(res)
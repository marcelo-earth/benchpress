"""Build the hard 50 item Spanish set (iteration 2, pre-registered 2026-10-14).

Same format as build_pilot.py. Writes pilot_hard_50.json (key and
justification) and pilot_hard_blind.json (what the labeler sees).
"""

import json

# (category, question, correct, [distractors], justification)
ITEMS = [
    ("lengua", "Completa: «No es mi hermano, ___ mi primo».", "sino", ["si no", "sí no", "si nó"], "Sino es la conjunción adversativa que contrapone a «no es mi hermano»."),
    ("lengua", "¿Cuál de estas palabras es esdrújula?", "Océano", ["Camión", "Árbol", "Cortés"], "Océano lleva el acento en la antepenúltima sílaba."),
    ("lengua", "¿Qué figura retórica hay en «Tus ojos son dos luceros»?", "Metáfora", ["Símil", "Hipérbole", "Ironía"], "Identifica ojos con luceros sin usar «como»."),
    ("lengua", "En «Se vendieron todas las entradas», ¿cuál es el sujeto?", "Todas las entradas", ["Se", "Vendieron todas", "No tiene sujeto"], "Es una pasiva refleja: el sujeto es lo vendido y concuerda con el verbo en plural."),
    ("lengua", "¿Cuál de estas palabras NO lleva tilde?", "Examen", ["Interés", "Lápiz", "Árbol"], "Examen es grave terminada en n, por lo que no se tilda; las otras sí."),
    ("lengua", "¿Qué significa la locución «a la vera de»?", "Al lado de", ["En contra de", "A causa de", "Lejos de"], "Vera significa orilla o borde."),
    ("lengua", "¿Cuál es la tercera persona del singular del pretérito perfecto simple de «andar»?", "Anduvo", ["Andó", "Anduvió", "Andaba"], "Andar tiene pretérito irregular: anduve, anduviste, anduvo."),
    ("lengua", "¿Cuál es un sinónimo de «prístino»?", "Inmaculado", ["Deteriorado", "Oscuro", "Confuso"], "Prístino significa original y sin mancha."),
    ("lengua", "¿Cuál de estas oraciones contiene un error de concordancia?", "Hubieron muchos problemas en la reunión.", ["Hubo muchos problemas en la reunión.", "Hay muchos problemas en la reunión.", "Habrá muchos problemas en la reunión."], "Haber impersonal va en singular: hubo."),
    ("lengua", "¿Cuál es el plural correcto de «régimen»?", "Regímenes", ["Régimenes", "Regimenes", "Régimens"], "Cambia la posición del acento: regímenes."),
    ("ciencia", "¿Por qué se ve azul el cielo despejado?", "La atmósfera dispersa más la luz de menor longitud de onda", ["Refleja el color del océano", "El ozono absorbe la luz roja", "La contaminación tiñe la luz del Sol"], "Es la dispersión de Rayleigh, que crece al disminuir la longitud de onda."),
    ("ciencia", "Si la temperatura absoluta de un gas ideal se duplica a presión constante, su volumen:", "se duplica", ["se reduce a la mitad", "se mantiene", "se cuadruplica"], "Ley de Charles: V es proporcional a T a presión constante."),
    ("ciencia", "Además del núcleo, ¿qué orgánulo de las células animales contiene su propio ADN?", "La mitocondria", ["El ribosoma", "El aparato de Golgi", "El lisosoma"], "La mitocondria tiene ADN propio, heredado de la madre."),
    ("ciencia", "¿Cuál es el elemento más abundante en la corteza terrestre?", "Oxígeno", ["Silicio", "Aluminio", "Hierro"], "El oxígeno representa cerca del 46 % de la masa de la corteza."),
    ("ciencia", "¿Qué partícula transmite la interacción electromagnética?", "El fotón", ["El gluón", "El bosón W", "El gravitón"], "El fotón es el bosón mediador del electromagnetismo."),
    ("ciencia", "En el vacío, sin fricción, ¿qué cae más rápido, una pluma o un martillo soltados a la vez desde la misma altura?", "Caen al mismo tiempo", ["El martillo", "La pluma", "Depende de la masa de cada uno"], "Sin resistencia del aire, todos los cuerpos caen con la misma aceleración."),
    ("ciencia", "¿Qué tipo de enlace une los átomos dentro de una molécula de agua?", "Covalente", ["Iónico", "Metálico", "Puente de hidrógeno"], "El puente de hidrógeno actúa entre moléculas, no dentro de ellas."),
    ("ciencia", "¿Cuántos cromosomas tiene una célula somática humana normal?", "46", ["23", "44", "48"], "Son 23 pares; 23 es el número de los gametos."),
    ("ciencia", "¿Qué vitamina sintetiza la piel al exponerse a la luz solar?", "Vitamina D", ["Vitamina C", "Vitamina A", "Vitamina K"], "La radiación UVB convierte un derivado del colesterol en vitamina D."),
    ("historia", "¿Qué tratado de 1494 repartió el Nuevo Mundo entre España y Portugal?", "Tordesillas", ["Utrecht", "Westfalia", "Versalles"], "Se firmó en Tordesillas, Valladolid."),
    ("historia", "¿Quién fue el principal líder inicial de la Revolución haitiana?", "Toussaint Louverture", ["Simón Bolívar", "Miguel Hidalgo", "José Martí"], "Louverture lideró la insurrección de esclavos desde 1791."),
    ("historia", "¿En qué año se aprobó la Constitución española vigente?", "1978", ["1975", "1981", "1986"], "Se aprobó en referéndum el 6 de diciembre de 1978."),
    ("geografia", "¿Cuál es la capital de Kazajistán?", "Astaná", ["Almaty", "Taskent", "Biskek"], "Astaná es la capital desde 1997; en 2022 recuperó ese nombre."),
    ("geografia", "Además de Paraguay, ¿qué país de Sudamérica no tiene costa?", "Bolivia", ["Ecuador", "Uruguay", "Colombia"], "Bolivia perdió su salida al mar en 1884."),
    ("geografia", "¿Qué estrecho separa Asia de América del Norte?", "Estrecho de Bering", ["Estrecho de Gibraltar", "Estrecho de Magallanes", "Estrecho de Ormuz"], "El estrecho de Bering une el mar de Bering y el océano Ártico."),
    ("historia", "¿Qué emperador romano dividió el imperio entre sus hijos Arcadio y Honorio?", "Teodosio I", ["Constantino", "Diocleciano", "Justiniano"], "Teodosio murió en 395 y dejó el Oriente a Arcadio y el Occidente a Honorio."),
    ("historia", "¿Qué batalla naval de 1805 consolidó el dominio británico sobre las flotas de Francia y España?", "Trafalgar", ["Lepanto", "Actium", "Midway"], "Nelson venció en Trafalgar, frente a la costa de Cádiz."),
    ("geografia", "¿Cuál es el lago más profundo del mundo?", "Baikal", ["Titicaca", "Superior", "Tanganica"], "El Baikal supera los 1600 m de profundidad."),
    ("historia", "¿Qué país fue el primero en conceder el voto a las mujeres a nivel nacional, en 1893?", "Nueva Zelanda", ["Reino Unido", "Estados Unidos", "Finlandia"], "Nueva Zelanda aprobó el sufragio femenino en 1893."),
    ("arte", "¿Quién escribió «Rayuela»?", "Julio Cortázar", ["Jorge Luis Borges", "Ernesto Sabato", "Adolfo Bioy Casares"], "Cortázar la publicó en 1963."),
    ("arte", "¿A qué movimiento artístico se asocia a Salvador Dalí?", "Surrealismo", ["Cubismo", "Impresionismo", "Expresionismo"], "Dalí fue una figura central del surrealismo."),
    ("arte", "¿Quién es el autor de «La ciudad y los perros»?", "Mario Vargas Llosa", ["Carlos Fuentes", "Roberto Bolaño", "Ernesto Sabato"], "Vargas Llosa la publicó en 1963."),
    ("arte", "¿Qué pintor realizó «Las Meninas»?", "Diego Velázquez", ["Francisco de Goya", "El Greco", "Bartolomé Murillo"], "Velázquez la pintó en 1656."),
    ("arte", "¿Quién escribió el «Romancero gitano»?", "Federico García Lorca", ["Rafael Alberti", "Miguel Hernández", "Antonio Machado"], "Lorca lo publicó en 1928."),
    ("razonamiento", "Se lanzan dos dados justos. ¿Cuál es la probabilidad de que sumen 7?", "1/6", ["1/12", "1/36", "7/36"], "Hay 6 combinaciones de 36 que suman 7."),
    ("razonamiento", "¿De cuántas maneras se pueden ordenar las letras de la palabra AMOR?", "24", ["12", "16", "120"], "4 letras distintas: 4! = 24."),
    ("razonamiento", "Un artículo cuesta 80 euros después de un descuento del 20 %. ¿Cuál era su precio original?", "100 euros", ["96 euros", "90 euros", "120 euros"], "El precio original p cumple 0,8p = 80, así que p = 100."),
    ("razonamiento", "Un precio sube un 10 % y luego baja un 10 %. Respecto al precio original, el final es:", "Un 1 % menor", ["Igual", "Un 1 % mayor", "Un 10 % menor"], "1,1 × 0,9 = 0,99."),
    ("razonamiento", "¿Cuál es el siguiente número de la serie 2, 6, 12, 20, 30, …?", "42", ["36", "40", "44"], "Los términos son n(n+1) y las diferencias crecen de 2 en 2: 30 + 12 = 42."),
    ("razonamiento", "En una isla, los caballeros siempre dicen la verdad y los bribones siempre mienten. A dice: «Los dos somos bribones». ¿Qué son A y B?", "A es bribón y B es caballero", ["A es caballero y B es bribón", "Ambos son bribones", "Ambos son caballeros"], "Si A fuera caballero, su frase sería verdadera y A sería bribón: absurdo. Luego A miente, así que no son ambos bribones y B es caballero."),
    ("razonamiento", "Hace 5 años Luis tenía el triple de la edad de su hijo. Hoy tiene el doble. ¿Qué edad tiene hoy el hijo?", "10 años", ["5 años", "15 años", "20 años"], "L - 5 = 3(s - 5) y L = 2s dan s = 10."),
    ("razonamiento", "Dos trenes salen a la vez, uno a 60 km/h y otro a 90 km/h, desde ciudades separadas 300 km y se acercan. ¿Cuánto tardan en cruzarse?", "2 horas", ["3 horas", "4 horas", "5 horas"], "Se acercan a 150 km/h: 300 / 150 = 2."),
    ("razonamiento", "Ocho personas se saludan todas entre sí con un apretón de manos, una vez por pareja. ¿Cuántos apretones hay?", "28", ["56", "64", "32"], "C(8,2) = 28."),
    ("razonamiento", "Todos los A son B y ningún B es C. ¿Qué se deduce con certeza?", "Ningún A es C", ["Algunos A son C", "Todos los C son A", "Todos los B son A"], "Como A está dentro de B y B no comparte nada con C, A tampoco."),
    ("razonamiento", "Un grifo llena una piscina en 6 horas y otro en 3 horas. ¿Cuánto tardan juntos?", "2 horas", ["4,5 horas", "3 horas", "9 horas"], "1/6 + 1/3 = 1/2 de piscina por hora."),
    ("razonamiento", "¿Cuál es la mediana de los datos 3, 7, 7, 2, 9?", "7", ["5,6", "3", "9"], "Ordenados 2, 3, 7, 7, 9: el valor central es 7; la media es 5,6."),
    ("razonamiento", "Una bolsa tiene 3 bolas rojas y 2 azules. Se sacan 2 sin devolverlas. ¿Cuál es la probabilidad de que ambas sean rojas?", "3/10", ["9/25", "3/5", "6/25"], "(3/5) × (2/4) = 3/10."),
    ("razonamiento", "En una familia, cada hermano tiene tantas hermanas como hermanos, y cada hermana tiene el doble de hermanos que de hermanas. ¿Cuántos hijos hay?", "7", ["5", "6", "8"], "Con b hijos y g hijas: g = b - 1 y b = 2(g - 1), que da b = 4 y g = 3."),
    ("razonamiento", "En una carrera adelantas al segundo. ¿En qué lugar vas?", "Segundo", ["Primero", "Tercero", "Cuarto"], "Al adelantar al segundo ocupas su puesto."),
    ("razonamiento", "María tiene el doble de libros que Pablo. Si Pablo le da 3 libros a María, ella tiene el triple que él. ¿Cuántos libros tenía Pablo?", "12", ["9", "15", "18"], "Con p libros de Pablo: 2p + 3 = 3(p - 3), que da p = 12."),
]

LETTERS = "ABCD"
gold, blind = [], []
for i, (cat, q, correct, wrong, why) in enumerate(ITEMS):
    pos = i % 4
    opts = list(wrong)
    opts.insert(pos, correct)
    choices = [f"{LETTERS[k]}) {o}" for k, o in enumerate(opts)]
    gold.append({"id": i + 1, "category": cat, "question": q, "choices": choices, "answer": LETTERS[pos], "justification": why})
    blind.append({"id": i + 1, "question": q, "choices": choices})

assert len(ITEMS) == 50, len(ITEMS)
json.dump(gold, open("pilot_hard_50.json", "w"), ensure_ascii=False, indent=1)
json.dump(blind, open("pilot_hard_blind.json", "w"), ensure_ascii=False, indent=1)
print(len(gold), {c: sum(1 for g in gold if g["answer"] == c) for c in LETTERS})

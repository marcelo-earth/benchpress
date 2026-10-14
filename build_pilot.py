"""Build the 50 question Spanish pilot (pre-registered 2026-10-14).

Each item lists the correct option first; positions are then assigned in a
fixed cycle so the answer key is balanced across A to D. Writes pilot_50.json
(with gold and justification) and pilot_blind.json (what the labeler sees).
"""

import json

# (category, question, correct, [distractors], justification)
ITEMS = [
    ("geografia", "¿Cuál es el océano más grande del mundo?", "Pacífico", ["Atlántico", "Índico", "Ártico"], "El Pacífico cubre cerca de un tercio de la superficie del planeta."),
    ("geografia", "¿En qué continente se encuentra el desierto del Sahara?", "África", ["Asia", "Oceanía", "América"], "El Sahara ocupa el norte de África."),
    ("geografia", "¿Cuál es la capital de Australia?", "Canberra", ["Sídney", "Melbourne", "Perth"], "Canberra es la capital federal desde 1913."),
    ("geografia", "¿Cuál es el río más caudaloso del mundo?", "Amazonas", ["Nilo", "Misisipi", "Yangtsé"], "El Amazonas tiene el mayor caudal medio de todos los ríos."),
    ("geografia", "¿Cuál es la cordillera más larga del mundo sobre tierra firme?", "Los Andes", ["Los Alpes", "El Himalaya", "Las Rocosas"], "Los Andes se extienden unos 7000 km por Sudamérica."),
    ("geografia", "¿Qué país tiene forma de bota en el mapa de Europa?", "Italia", ["España", "Grecia", "Portugal"], "La península itálica tiene forma de bota."),
    ("geografia", "¿En qué ciudad se encuentra la Torre Eiffel?", "París", ["Londres", "Roma", "Madrid"], "La Torre Eiffel está en París, Francia."),
    ("geografia", "¿Cuál es el idioma oficial de Brasil?", "Portugués", ["Español", "Inglés", "Francés"], "Brasil fue colonia portuguesa y su idioma oficial es el portugués."),
    ("historia", "¿En qué año cayó el Muro de Berlín?", "1989", ["1985", "1991", "1993"], "El muro se abrió el 9 de noviembre de 1989."),
    ("historia", "¿Qué civilización construyó Machu Picchu?", "Inca", ["Maya", "Azteca", "Olmeca"], "Machu Picchu fue una ciudadela inca del siglo XV."),
    ("historia", "¿Quién fue el primer presidente de Estados Unidos?", "George Washington", ["Thomas Jefferson", "Abraham Lincoln", "John Adams"], "Washington presidió de 1789 a 1797."),
    ("historia", "¿En qué año comenzó la Primera Guerra Mundial?", "1914", ["1904", "1918", "1939"], "Estalló en julio de 1914 tras el asesinato de Francisco Fernando."),
    ("historia", "¿En qué siglo ocurrió la Revolución francesa?", "Siglo XVIII", ["Siglo XVII", "Siglo XIX", "Siglo XX"], "Comenzó en 1789."),
    ("historia", "¿Qué país regaló la Estatua de la Libertad a Estados Unidos?", "Francia", ["Reino Unido", "España", "Italia"], "Francia la entregó en 1886 como símbolo de amistad."),
    ("ciencia", "¿Cuál es el símbolo químico del oro?", "Au", ["Ag", "Gd", "Or"], "Au viene del latín aurum."),
    ("ciencia", "¿Cuántos planetas tiene el sistema solar?", "Ocho", ["Siete", "Nueve", "Diez"], "Desde 2006 Plutón se clasifica como planeta enano, quedan ocho."),
    ("ciencia", "¿Qué gas absorben las plantas durante la fotosíntesis?", "Dióxido de carbono", ["Oxígeno", "Nitrógeno", "Hidrógeno"], "La fotosíntesis consume CO2 y libera oxígeno."),
    ("ciencia", "¿Cuál es la unidad básica de la herencia genética?", "El gen", ["La célula", "El átomo", "El tejido"], "El gen es el segmento de ADN que codifica un rasgo hereditario."),
    ("ciencia", "¿Cuál es el hueso más largo del cuerpo humano?", "Fémur", ["Húmero", "Tibia", "Peroné"], "El fémur es el hueso del muslo y el más largo."),
    ("ciencia", "¿Qué órgano bombea la sangre por el cuerpo?", "El corazón", ["El hígado", "El pulmón", "El riñón"], "El corazón impulsa la sangre por el sistema circulatorio."),
    ("ciencia", "¿Cuál es el planeta más cercano al Sol?", "Mercurio", ["Venus", "Marte", "Tierra"], "Mercurio orbita a unos 58 millones de km del Sol."),
    ("ciencia", "¿Qué tipo de animal es una ballena?", "Mamífero", ["Pez", "Reptil", "Anfibio"], "Las ballenas respiran aire y amamantan a sus crías."),
    ("ciencia", "¿Cuál es la fórmula química del agua?", "H2O", ["CO2", "O2", "NaCl"], "Dos átomos de hidrógeno y uno de oxígeno."),
    ("ciencia", "¿Cuál es el único metal que es líquido a temperatura ambiente?", "Mercurio", ["Plomo", "Aluminio", "Cobre"], "El mercurio funde a unos -39 °C."),
    ("ciencia", "¿Cuántos huesos tiene aproximadamente el cuerpo de un adulto?", "206", ["106", "306", "406"], "El esqueleto adulto tiene 206 huesos."),
    ("ciencia", "¿Qué instrumento se usa para medir la temperatura?", "Termómetro", ["Barómetro", "Higrómetro", "Anemómetro"], "El barómetro mide presión, el higrómetro humedad y el anemómetro viento."),
    ("ciencia", "¿Cuál es el mayor mamífero del mundo?", "Ballena azul", ["Elefante africano", "Jirafa", "Tiburón ballena"], "La ballena azul supera las 100 toneladas; el tiburón ballena es un pez."),
    ("ciencia", "¿Cuál es el animal terrestre más rápido?", "Guepardo", ["León", "Caballo", "Antílope"], "El guepardo alcanza cerca de 110 km/h."),
    ("arte", "¿Quién pintó La Gioconda (Mona Lisa)?", "Leonardo da Vinci", ["Miguel Ángel", "Rafael", "Botticelli"], "Leonardo la pintó a comienzos del siglo XVI."),
    ("arte", "¿Quién compuso la Novena Sinfonía, que incluye el «Himno a la alegría»?", "Beethoven", ["Mozart", "Bach", "Chopin"], "Beethoven la estrenó en 1824."),
    ("arte", "¿Cuál es la moneda oficial de Japón?", "Yen", ["Yuan", "Won", "Rupia"], "El yen es la moneda de Japón; el yuan es chino y el won coreano."),
    ("literatura", "¿Quién escribió «Don Quijote de la Mancha»?", "Miguel de Cervantes", ["Lope de Vega", "Francisco de Quevedo", "Pedro Calderón de la Barca"], "Cervantes publicó la primera parte en 1605."),
    ("literatura", "¿Quién es el autor de «Pedro Páramo»?", "Juan Rulfo", ["Octavio Paz", "Mario Benedetti", "Julio Cortázar"], "Rulfo, escritor mexicano, la publicó en 1955."),
    ("literatura", "¿Quién es el autor de «Veinte poemas de amor y una canción desesperada»?", "Pablo Neruda", ["Gabriela Mistral", "Jorge Luis Borges", "Octavio Paz"], "Neruda lo publicó en 1924."),
    ("lengua", "¿Cuál de estas palabras es aguda?", "Canción", ["Árbol", "Mesa", "Lápiz"], "Canción lleva el acento en la última sílaba; las otras son graves."),
    ("lengua", "¿Cuál es el plural correcto de «lápiz»?", "Lápices", ["Lápizes", "Lapíces", "Lápiz's"], "Las palabras terminadas en z cambian a c ante es."),
    ("lengua", "¿Cuál de estas palabras está escrita correctamente?", "Haber", ["Haver", "Aver", "Aber"], "Haber se escribe con h y con b."),
    ("lengua", "¿Cuál es el antónimo de «efímero»?", "Duradero", ["Breve", "Pasajero", "Fugaz"], "Efímero significa de corta duración; lo contrario es duradero."),
    ("razonamiento", "¿Cuánto es el 15 % de 200?", "30", ["15", "20", "45"], "200 × 0,15 = 30."),
    ("razonamiento", "Un tren viaja a 60 km/h durante 2,5 horas. ¿Cuántos kilómetros recorre?", "150 km", ["120 km", "140 km", "180 km"], "60 × 2,5 = 150."),
    ("razonamiento", "¿Cuál es el siguiente número de la serie 2, 4, 8, 16, …?", "32", ["24", "30", "36"], "Cada término duplica al anterior."),
    ("razonamiento", "Ana es mayor que Beto y Beto es mayor que Carla. ¿Quién es la más joven?", "Carla", ["Ana", "Beto", "No se puede saber"], "Por transitividad, Ana > Beto > Carla."),
    ("razonamiento", "Todas las aves tienen plumas y el colibrí es un ave. ¿Qué afirmación se deduce con certeza?", "El colibrí tiene plumas", ["Todos los animales con plumas son colibríes", "El colibrí es el único animal con plumas", "Los colibríes no pueden volar"], "Si todas las aves tienen plumas y el colibrí es un ave, el colibrí tiene plumas."),
    ("razonamiento", "Un libro y un lápiz cuestan 11 euros en total. El libro cuesta 10 euros más que el lápiz. ¿Cuánto cuesta el lápiz?", "0,50 euros", ["1 euro", "0,10 euros", "1,10 euros"], "Lápiz = x, libro = x + 10, 2x + 10 = 11, x = 0,50."),
    ("razonamiento", "Si hoy es miércoles, ¿qué día de la semana será dentro de 10 días?", "Sábado", ["Viernes", "Domingo", "Lunes"], "10 días son una semana y 3 días; miércoles + 3 = sábado."),
    ("razonamiento", "¿Cuántos lados tiene un hexágono?", "Seis", ["Cinco", "Siete", "Ocho"], "Hexa significa seis."),
    ("razonamiento", "¿Cuál es el resultado de 7 × 8?", "56", ["54", "58", "64"], "7 × 8 = 56."),
    ("razonamiento", "¿Cuántos huevos son una docena y media?", "18", ["12", "15", "24"], "12 + 6 = 18."),
    ("razonamiento", "Si 3 máquinas hacen 3 piezas en 3 minutos, ¿cuántos minutos tardan 100 máquinas en hacer 100 piezas?", "3 minutos", ["1 minuto", "33 minutos", "100 minutos"], "Cada máquina hace una pieza en 3 minutos, así que 100 máquinas hacen 100 en 3."),
    ("razonamiento", "¿Cuál es el valor de x en 3x + 5 = 20?", "5", ["3", "7", "15"], "3x = 15, x = 5."),
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

assert len(ITEMS) == 50
json.dump(gold, open("pilot_50.json", "w"), ensure_ascii=False, indent=1)
json.dump(blind, open("pilot_blind.json", "w"), ensure_ascii=False, indent=1)
print(len(gold), {c: sum(1 for g in gold if g["answer"] == c) for c in LETTERS})

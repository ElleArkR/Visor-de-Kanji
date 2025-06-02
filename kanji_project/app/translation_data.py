# kanji_project/app/translation_data.py

# Processed dictionary to ensure unique English keys, keeping the first encountered translation.
TRANSLATIONS_DICT = {
    # --- Original entries ---
    'big': 'grande',
    'small': 'pequeño',
    'middle': 'medio',
    'long': 'largo',
    'four': 'cuatro',
    'short': 'corto',
    'sun': 'sol',
    'moon': 'luna',
    'fire': 'fuego',
    'water': 'agua',
    'tree': 'árbol',
    'gold': 'oro',
    'earth': 'tierra',
    'one': 'uno',
    'two': 'dos',
    'three': 'tres',
    'ten': 'diez',
    'person': 'persona',
    'enter': 'entrar',
    'exit': 'salir',
    'see': 'ver',
    'eat': 'comer',
    'drink': 'beber',
    'learn': 'aprender',
    'go': 'ir',
    'come': 'venir',
    'year': 'año',
    'day': 'día',
    'mouth': 'boca',
    'eye': 'ojo',
    'hand': 'mano',
    'foot': 'pie',
    'power': 'fuerza', # también podría ser 'poder'
    'flower': 'flor',
    'rain': 'lluvia',
    'new': 'nuevo',
    'old': 'viejo',
    'good': 'bueno',
    'bad': 'malo',
    'white': 'blanco',
    'black': 'negro',
    'red': 'rojo',
    'blue': 'azul',
    'left': 'izquierda',
    'right': 'derecha',
    'up': 'arriba',
    'down': 'abajo',
    'east': 'este',
    'west': 'oeste',
    'south': 'sur',
    'north': 'norte',
    'name': 'nombre',
    'word': 'palabra',
    'book': 'libro',
    'read': 'leer',
    'write': 'escribir',
    'speak': 'hablar',
    'say': 'decir',
    'buy': 'comprar',
    'sell': 'vender',
    'friend': 'amigo', # 'amiga' para femenino
    'mother': 'madre',
    'father': 'padre',
    'child': 'niño', # 'niña' para femenino, 'hijo/hija'
    'morning': 'mañana', # (parte del día)
    'evening': 'tarde', # (parte del día)
    'night': 'noche',
    'week': 'semana',
    'month': 'mes',
    'time': 'tiempo', # también 'vez'
    'hour': 'hora',
    'minute': 'minuto',
    'second': 'segundo',
    'now': 'ahora',
    'before': 'antes',
    'after': 'después',
    'high': 'alto',
    'low': 'bajo',
    'hot': 'caliente',
    'cold': 'frío',
    'country': 'país',
    'king': 'rey',
    'queen': 'reina',
    'rice': 'arroz',
    'tea': 'té',
    'meat': 'carne',
    'fish': 'pescado', # como alimento, 'pez' como animal vivo
    'bird': 'pájaro', # también 'ave'
    'dog': 'perro',
    'cat': 'gato',
    'house': 'casa',
    'school': 'escuela',
    'shop': 'tienda',
    'station': 'estación',
    'car': 'coche', # también 'auto', 'carro'
    'road': 'camino', # también 'carretera', 'vía'
    'mountain': 'montaña',
    'river': 'río',
    'sky': 'cielo',
    'world': 'mundo',
    'paper': 'papel',
    'music': 'música',
    'doctor': 'doctor', # también 'médico'
    'medicine': 'medicina', # también 'medicamento'
    'body': 'cuerpo',
    'head': 'cabeza',
    'face': 'cara', # también 'rostro'
    'hair': 'pelo', # también 'cabello'
    'heart': 'corazón',
    'spirit': 'espíritu', # también 'alma'
    'color': 'color',
    'light': 'luz',
    'dark': 'oscuro',
    'study': 'estudiar',
    'make': 'hacer', # también 'fabricar', 'crear'
    'use': 'usar', # también 'utilizar'
    'think': 'pensar',
    'know': 'saber', # también 'conocer'
    'live': 'vivir',
    'die': 'morir',
    'love': 'amar', # también 'amor' (sustantivo)
    'war': 'guerra',
    'peace': 'paz',
    'god': 'dios', # 'diosa' para femenino
    'way': 'camino', # también 'manera', 'método', 'vía'
    'true': 'verdadero', # también 'verdad' (sustantivo)
    'false': 'falso',
    'correct': 'correcto',
    'wrong': 'incorrecto', # también 'equivocado'
    'city': 'ciudad',
    'village': 'pueblo', # también 'aldea'
    'capital': 'capital',
    'sea': 'mar',
    'ocean': 'océano',
    'island': 'isla',
    'forest': 'bosque',
    'field': 'campo', # también 'prado'
    'store': 'tienda',
    'front': 'frente', # también 'delante'
    'back': 'espalda', # también 'detrás', 'atrás'
    'inside': 'dentro',
    'outside': 'fuera',
    'spring': 'primavera',
    'summer': 'verano',
    'autumn': 'otoño',
    'winter': 'invierno',
    'bright': 'brillante', # también 'claro'
    'darkness': 'oscuridad',
    'early': 'temprano',
    'late': 'tarde', # (adverbio de tiempo)
    'easy': 'fácil',
    'difficult': 'difícil',
    'strong': 'fuerte',
    'weak': 'débil',
    'beautiful': 'hermoso', # también 'bello', 'bonito'
    'ugly': 'feo',
    'happy': 'feliz', # también 'alegre'
    'sad': 'triste',
    'angry': 'enfadado', # también 'enojado'
    'kind': 'amable', # también 'bondadoso'
    'polite': 'educado', # también 'cortés'
    'new year': 'año nuevo',
    'to cut': 'cortar',
    'to wear': 'vestir', # también 'usar ropa', 'llevar puesto'
    'to arrive': 'llegar',
    'to send': 'enviar', # también 'mandar'
    'to wash': 'lavar',
    'to sing': 'cantar',
    'to dance': 'bailar',
    'to play': 'jugar', # también 'tocar' (un instrumento)
    'to meet': 'conocer', # también 'encontrarse con', 'reunirse'
    'to wait': 'esperar',
    'to rest': 'descansar',
    'to work': 'trabajar',
    'to begin': 'empezar', # también 'comenzar', 'iniciar'
    'to end': 'terminar', # también 'acabar', 'finalizar'
    'to listen': 'escuchar',
    'to teach': 'enseñar',
    'to remember': 'recordar',
    'to forget': 'olvidar',
    'to stand': 'estar de pie', # también 'ponerse de pie'
    'to sit': 'sentarse',
    'to open': 'abrir',
    'to close': 'cerrar',
    'to return': 'volver', # también 'regresar', 'devolver'
    'to give': 'dar',
    'to receive': 'recibir',
    'to understand': 'entender', # también 'comprender'
    'to explain': 'explicar',
    'to ask': 'preguntar', # también 'pedir'
    'to answer': 'responder', # también 'contestar'
    'to help': 'ayudar',
    'to protect': 'proteger',
    'to believe': 'creer',
    'to travel': 'viajar',
    'to swim': 'nadar',
    'to run': 'correr',
    'to walk': 'caminar', # también 'andar'
    'to fly': 'volar',
    'to count': 'contar',
    'to compare': 'comparar',
    'to choose': 'elegir', # también 'escoger'
    'to decide': 'decidir',
    'to win': 'ganar', # (una competencia)
    'to lose': 'perder',
    'to stop': 'parar', # también 'detener'
    'to continue': 'continuar', # también 'seguir'
    'to change': 'cambiar',
    'to grow': 'crecer', # también 'cultivar'
    'to build': 'construir',
    'to break': 'romper',
    'to fall': 'caer',
    'to feel': 'sentir',
    'to want': 'querer', # también 'desear'
    'to need': 'necesitar',
    'to try': 'intentar', # también 'probar'
    'to put': 'poner', # también 'colocar'
    'to take': 'tomar', # también 'coger', 'llevar'
    'to show': 'mostrar', # también 'enseñar'
    'to become': 'convertirse en', # también 'llegar a ser', 'volverse'
    'to call': 'llamar',
    'to pay': 'pagar',
    'to lend': 'prestar',
    'to borrow': 'pedir prestado',
    'to agree': 'estar de acuerdo',
    'to disagree': 'no estar de acuerdo', # también 'discrepar'
    'to prepare': 'preparar',
    'to order': 'ordenar', # también 'pedir' (en un restaurante)
    'to serve': 'servir',
    'to invite': 'invitar',
    'to visit': 'visitar',
    'to hope': 'esperar', # (tener esperanza)
    'to dream': 'soñar',
    'to laugh': 'reír',
    'to cry': 'llorar',
    'to smile': 'sonreír',
    'to worry': 'preocuparse',
    'to fear': 'temer', # también 'tener miedo'
    'to respect': 'respetar',
    'to kill': 'matar',
    'to save': 'salvar', # también 'guardar', 'ahorrar'
    'to search': 'buscar',
    'to find': 'encontrar',
    # --- Additional N5 Kanji related terms (examples) ---
    'five': 'cinco',
    'six': 'seis',
    'seven': 'siete',
    'eight': 'ocho',
    'nine': 'nueve',
    'hundred': 'cien',
    'thousand': 'mil',
    'ten thousand': 'diez mil',
    'yen': 'yen',
    'woman': 'mujer',
    'man': 'hombre',
    'teacher': 'profesor', # también 'maestro'
    'student': 'estudiante',
    'university': 'universidad',
    'primary school': 'escuela primaria',
    'middle school': 'escuela secundaria',
    'food': 'comida',
    'language': 'idioma', # también 'lengua'
    'what': 'qué',
    'I': 'yo',
    'this': 'esto', # 'este', 'esta'
    'that': 'eso', # 'ese', 'esa', 'aquel', 'aquella'
    'here': 'aquí',
    'there': 'allí', # también 'ahí'
    'who': 'quién',
    'when': 'cuándo',
    'where': 'dónde',
    'why': 'por qué',
    'how': 'cómo',
    'every day': 'todos los días',
    'every week': 'todas las semanas',
    'every month': 'todos los meses',
    'every year': 'todos los años',
    'half': 'mitad',
    'noon': 'mediodía',
    'rest': 'descanso', # también 'descansar' (verbo)
    'electricity': 'electricidad',
    'train': 'tren',
    'company': 'empresa', # también 'compañía'
    'bank': 'banco',
    'hospital': 'hospital',
    'illness': 'enfermedad', # también 'mal'
    'park': 'parque',
    'garden': 'jardín',
    'meat': 'carne', # Duplicate entry, already present
    'sky': 'cielo', # Duplicate entry, already present
    'mountain': 'montaña', # Duplicate entry, already present
    'river': 'río', # Duplicate entry, already present
    'weather': 'tiempo', # (clima)
    # --- Additional N4 Kanji related terms (examples) ---
    'bad luck': 'mala suerte',
    'peaceful': 'pacífico', # 'tranquilo'
    'dark': 'oscuro', # Duplicate entry, already present
    'doctor': 'doctor', # Duplicate entry, already present
    'meaning': 'significado',
    'to raise': 'criar', # también 'levantar'
    'member': 'miembro',
    'to drink': 'beber', # Duplicate entry, already present
    'luck': 'suerte',
    'to swim': 'nadar', # Duplicate entry, already present
    'english': 'inglés',
    'park': 'parque', # Duplicate entry, already present
    'horizontal': 'horizontal',
    'hot water': 'agua caliente',
    'change': 'cambio', # también 'cambiar' (verbo)
    'world': 'mundo', # Duplicate entry, already present
    'open': 'abrir', # también 'abierto' (adjetivo)
    'floor': 'piso', # también 'suelo'
    'cold': 'frío', # Duplicate entry, already present
    'feeling': 'sentimiento', # también 'sensación'
    'Chinese character': 'kanji', # también 'carácter chino'
    'building': 'edificio',
    'shore': 'orilla', # también 'costa'
    'to get up': 'levantarse',
    'period': 'período', # también 'época'
    'guest': 'invitado', # también 'huésped'
    'research': 'investigación',
    'urgent': 'urgente',
    'ball': 'pelota', # también 'balón'
    'to leave': 'irse', # también 'dejar', 'salir'
    'bridge': 'puente',
    'business': 'negocio', # también 'asunto'
    'to bend': 'doblar', # también 'curvar'
    'post office': 'oficina de correos',
    'ward': 'distrito', # (de una ciudad)
    'suffering': 'sufrimiento', # también 'dolor'
    'tool': 'herramienta',
    'you': 'tú', # también 'usted', 'vosotros', 'ustedes'
    'connection': 'conexión', # también 'relación'
    'light': 'ligero', # (peso), también 'luz' (iluminación)
    'blood': 'sangre',
    'to decide': 'decidir', # Duplicate entry, already present
    'research institute': 'instituto de investigación',
    'prefecture': 'prefectura',
    'warehouse': 'almacén',
    'lake': 'lago',
    'to face': 'enfrentar', # también 'mirar hacia'
    'happiness': 'felicidad',
    'harbor': 'puerto',
    'number': 'número',
    'root': 'raíz',
    'festival': 'festival', # también 'fiesta'
    'plate': 'plato', # también 'lámina'
    'to serve': 'servir', # (a alguien), también 'funcionar'
    'death': 'muerte',
    'to use': 'usar', # Duplicate entry, already present
    'to begin': 'empezar', # Duplicate entry, already present
    'finger': 'dedo',
    'tooth': 'diente',
    'poem': 'poema',
    'next': 'siguiente', # también 'próximo'
    'thing': 'cosa', # también 'asunto'
    'to hold': 'sostener', # también 'tener'
    'room': 'habitación', # también 'cuarto', 'espacio'
    'company': 'empresa', # Duplicate entry, already present
    'weak': 'débil', # Duplicate entry, already present
    'neck': 'cuello',
    'autumn': 'otoño', # Duplicate entry, already present
    'week': 'semana', # Duplicate entry, already present
    'to find a job': 'encontrar trabajo',
    'to pick up': 'recoger',
    'inn': 'posada', # también 'mesón'
    'master': 'maestro', # también 'amo', 'dueño'
    'to protect': 'proteger', # Duplicate entry, already present
    'to take': 'tomar', # Duplicate entry, already present
    'hand': 'mano', # Duplicate entry, already present
    'sake': 'sake', # (bebida alcohólica japonesa)
    'to receive': 'recibir', # Duplicate entry, already present
    'province': 'provincia',
    'to gather': 'reunir', # también 'recoger'
    'to live': 'vivir', # Duplicate entry, already present
    'heavy': 'pesado',
    'place': 'lugar', # también 'sitio'
    'hot': 'caliente', # (clima, objeto)
    'to help': 'ayudar', # Duplicate entry, already present
    'Showa era': 'era Showa',
    'to disappear': 'desaparecer',
    'trade': 'comercio',
    'chapter': 'capítulo',
    'victory': 'victoria', # también 'ganar'
    'to ride': 'montar', # (a caballo, en bicicleta, etc.)
    'to plant': 'plantar',
    'to say': 'decir', # (humilde)
    'body': 'cuerpo', # Duplicate entry, already present
    'deep': 'profundo',
    'to advance': 'avanzar', # también 'progresar'
    'forest': 'bosque', # Duplicate entry, already present
    'to arrange': 'arreglar', # también 'organizar', 'disponer'
    'old times': 'tiempos antiguos', # también 'antaño'
    'whole': 'entero', # también 'todo'
    'mutual': 'mutuo', # también 'recíproco'
    'to send': 'enviar', # Duplicate entry, already present
    'thought': 'pensamiento',
    'breath': 'aliento', # también 'respiración'
    'fast': 'rápido',
    'family': 'familia',
    'other': 'otro',
    'to hit': 'golpear', # también 'pegar'
    'opposite': 'opuesto', # también 'contrario'
    'to wait': 'esperar', # Duplicate entry, already present
    'to replace': 'reemplazar', # también 'sustituir'
    'stand': 'puesto', # (de venta), también 'soporte', 'estar de pie'
    'first': 'primero',
    'subject': 'tema', # también 'asunto', 'asignatura'
    'charcoal': 'carbón vegetal',
    'short': 'corto', # Duplicate entry, already present
    'conversation': 'conversación',
    'to wear': 'vestir', # Duplicate entry, already present
    'to pour': 'verter', # también 'echar'
    'pillar': 'pilar', # también 'columna'
    'notebook': 'cuaderno', # también 'libreta'
    'to investigate': 'investigar',
    'to chase': 'perseguir',
    'fixed': 'fijo', # también 'determinado'
    'garden': 'jardín', # Duplicate entry, already present
    'flute': 'flauta',
    'iron': 'hierro',
    'to turn': 'girar', # también 'volver', 'convertir'
    'capital': 'capital', # Duplicate entry, already present
    'degree': 'grado',
    'to throw': 'lanzar', # también 'tirar', 'arrojar'
    'beans': 'frijoles', # también 'judías', 'habichuelas'
    'island': 'isla', # Duplicate entry, already present
    'hot water': 'agua caliente', # Duplicate entry, already present
    'lamp': 'lámpara',
    'suitable': 'adecuado', # también 'apropiado', 'conveniente'
    'answer': 'respuesta',
    'head': 'cabeza', # Duplicate entry, already present
    'same': 'mismo',
    'road': 'camino', # Duplicate entry, already present
    'to work': 'trabajar', # Duplicate entry, already present
    'special': 'especial',
    'poison': 'veneno',
    'hot': 'caliente', # (temperatura)
    'wish': 'deseo', # también 'desear' (verbo)
    'wave': 'ola', # también 'onda'
    'to distribute': 'distribuir',
    'double': 'doble',
    'box': 'caja',
    'field': 'campo cultivado', # (畑)
    'to depart': 'partir', # también 'salir'
    'contrary': 'contrario',
    'slope': 'pendiente', # también 'cuesta', 'ladera'
    'board': 'tabla', # también 'tablero', 'junta'
    'skin': 'piel',
    'sad': 'triste', # Duplicate entry, already present
    'beautiful': 'hermoso', # Duplicate entry, already present
    'nose': 'nariz',
    'writing brush': 'pincel de escritura',
    'ice': 'hielo',
    'surface': 'superficie',
    'second': 'segundo', # (unidad de tiempo)
    'illness': 'enfermedad', # Duplicate entry, already present
    'goods': 'bienes', # también 'mercancías', 'artículos'
    'to lose': 'perder', # Duplicate entry, already present
    'part': 'parte',
    'clothes': 'ropa',
    'happiness': 'felicidad', # Duplicate entry, already present
    'flat': 'plano', # también 'llano'
    'to return': 'devolver', # (algo)
    'study': 'estudio', # también 'estudiar' (verbo)
    'to release': 'liberar', # también 'soltar'
    'taste': 'sabor', # también 'gusto'
    'life': 'vida',
    'face': 'cara', # Duplicate entry, already present
    'question': 'pregunta',
    'useful': 'útil',
    'medicine': 'medicina', # Duplicate entry, already present
    'reason': 'razón', # también 'motivo'
    'oil': 'aceite', # también 'petróleo'
    'to exist': 'existir',
    'to play': 'jugar', # Duplicate entry, already present
    'plan': 'plan', # también 'proyecto'
    'polite form': 'forma cortés',
    'ocean': 'océano', # Duplicate entry, already present
    'positive': 'positivo',
    'leaf': 'hoja', # (de árbol)
    'to dance': 'bailar', # Duplicate entry, already present
    'to flow': 'fluir',
    'trip': 'viaje',
    'both': 'ambos',
    'green': 'verde',
    'gratitude': 'gratitud', # también 'agradecimiento'
    'line': 'línea', # también 'fila', 'renglón'
    'to practice': 'practicar', # también 'ejercitar'
    'road': 'camino', # Duplicate entry, already present (道 vs 路)
    'harmony': 'armonía', # también 'paz'
    # --- N3 Samples (actual N3 would be much more extensive) ---
    'government': 'gobierno',
    'discussion': 'discusión', # también 'debate'
    'people': 'gente', # también 'pueblo' (nación)
    'to connect': 'conectar',
    'election': 'elección',
    'rice (USA)': 'arroz (EE.UU.)', # Assuming differentiation from general rice if needed
    'fruit': 'fruta',
    'truth': 'verdad',
    'prefectural office': 'oficina prefectural',
    # --- N2 Samples ---
    'resources': 'recursos',
    'international': 'internacional',
    'general': 'general',
    'to establish': 'establecer',
    'to protect': 'proteger', # Duplicate entry, already present
    'political party': 'partido político',
    'to nominate': 'nominar', # también 'proponer'
    'to respond': 'responder',
    'inspection': 'inspección',
    'rights': 'derechos',
    # --- N1 Samples (very few, just for structure) ---
    'beautiful': 'hermoso', # Duplicate, but N1 'rei' can mean exquisite beauty
    'crane': 'grulla',
    'foot of a mountain': 'pie de la montaña', # también 'falda de la montaña'
    'elegant': 'elegante',
    'I (imperial)': 'yo (imperial)',
    'imperial seal': 'sello imperial',
    'account book': 'libro de cuentas',
    'to make clear': 'aclarar', # también 'esclarecer'
    'to go upstream': 'ir río arriba', # también 'remontar'
    'temple': 'templo',
    'moment': 'momento' # Added from user example, 刹 (setsu) can mean moment/instant
} 
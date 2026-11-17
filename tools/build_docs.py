"""Genera los dos PDF de docs/ a partir de la información oficial de EAFIT consultada el 17-nov-2026.

Solo hace falta para regenerar los documentos (requiere `pip install reportlab`).
Uso:  python tools/build_docs.py
"""
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

DOCS = Path(__file__).resolve().parent.parent / "docs"
ss = getSampleStyleSheet()
H1 = ParagraphStyle("h1", parent=ss["Heading1"], fontSize=15, spaceAfter=8)
H2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=12, spaceBefore=8, spaceAfter=4)
P = ParagraphStyle("p", parent=ss["BodyText"], fontSize=10, leading=13.5, spaceAfter=6)
NOTE = ParagraphStyle("n", parent=P, fontSize=9, textColor="#444444")


def build(name, pages):
    story = []
    for n, page in enumerate(pages):
        if n:
            story.append(PageBreak())
        for kind, text in page:
            story.append(Paragraph(text, {"h1": H1, "h2": H2, "p": P, "n": NOTE}[kind]))
    SimpleDocTemplate(str(DOCS / name), pagesize=letter, leftMargin=2.2*cm, rightMargin=2.2*cm,
                      topMargin=2*cm, bottomMargin=2*cm, title=name).build(story)
    print("+", name, f"({len(pages)} páginas)")


# ----------------------------------------------------------------------------------------------
# 1. Reglamento: resumen por artículo
# ----------------------------------------------------------------------------------------------
REG_URL = "https://www.eafit.edu.co/institucional/reglamentos"
reg = [
 [("h1", "Reglamento académico de los programas de pregrado - Universidad EAFIT"),
  ("h2", "Resumen por artículos (artículos 1 a 90)"),
  ("n", "Documento de trabajo elaborado por el equipo del proyecto final de SI3003 a partir del Reglamento "
        "académico de los programas de pregrado de la Universidad EAFIT (aprobado por el Consejo Académico en el "
        "acta 019 del 24 de noviembre de 2020, con modificaciones hasta el acta 01 del 1 de febrero de 2024), "
        "consultado el 17 de noviembre de 2026. Fuente oficial: " + REG_URL + ". Es un resumen: cada regla se "
        "presenta con el número de su artículo para poder verificarla en el texto oficial, que es el único con "
        "validez. Este resumen cubre los artículos 1 a 90; no incluye los capítulos posteriores (por ejemplo, "
        "requisitos de grado y régimen disciplinario)."),
  ("h2", "Plan de estudios, créditos y prerrequisitos"),
  ("p", "Artículo 8. Plan de estudios. El plan de estudios es el esquema estructurado de áreas de conocimiento, "
        "períodos, créditos y demás requisitos académicos de un pregrado. Se organiza en núcleos de formación: "
        "humanística y científica (Núcleo de Formación Institucional), básica y científica, profesional, de "
        "énfasis y de libre configuración. Los planes de estudio los aprueba el Consejo Académico, previa "
        "recomendación del Consejo de Escuela."),
  ("p", "Artículo 9. Prerrequisitos y correquisitos. Un prerrequisito es una asignatura que es indispensable "
        "haber aprobado para matricular otra de nivel superior. Un correquisito es una asignatura que debe "
        "cursarse de forma simultánea con otra. Cualquier excepción al régimen de prerrequisitos y correquisitos "
        "debe autorizarla el jefe del programa de pregrado. La excepción solo procede si el estudiante cumple "
        "alguna de estas condiciones: promedio crédito acumulado en el percentil 90 o superior de su programa; "
        "compromisos previos con entidades externas (práctica, investigación o condonación de becas); estar "
        "activo en doble programa de pregrado; razones de salud o cognitivas certificadas; razones de seguridad "
        "certificadas; o condiciones análogas validadas por la decanatura. El estudiante debe justificar cómo "
        "demostrará las competencias de la asignatura que pide exceptuar. Si no cumple ninguna condición, la "
        "solicitud se rechaza de plano."),
  ("p", "Artículo 11. Duración de los pregrados. La duración de los pregrados se define en créditos académicos. "
        "Un crédito académico equivale a 48 horas de trabajo académico del estudiante en un período académico, "
        "repartidas entre trabajo acompañado por el profesor y trabajo independiente. La duración en semestres "
        "que se anuncia es una estimación y puede variar según los créditos que matricule el estudiante."),
  ("p", "Artículo 12. Tipos de créditos. Los créditos pueden ser obligatorios, electivos (de énfasis, "
        "complementarios o de libre configuración) y de Formación Humanística y Científica - Núcleo de Formación "
        "Institucional. El Núcleo de Formación Institucional tiene como máximo 18 créditos del plan de estudios, "
        "salvo excepciones del Consejo Académico. Si el estudiante registra una línea de énfasis, queda obligado "
        "a completarla para optar al título."),
  ("p", "Artículo 13. Límite de créditos. Cada programa de pregrado define el límite máximo de créditos que un "
        "estudiante puede matricular por período académico."),
  ("p", "Artículo 15. Práctica estudiantil. La práctica estudiantil no puede ser inferior al 10 % del total de "
        "créditos del pregrado. Sus modalidades se regulan en el Reglamento de Experiencias de Talento."),
  ("p", "Artículo 18. Trabajo de grado. En los programas que lo contemplan, el trabajo de grado es una "
        "asignatura de créditos obligatorios. Hay un plazo adicional para entregarlo, sin costo: el período "
        "académico siguiente a aquel en que se matriculó, previa carta avalada por el jefe de programa y el "
        "asesor. Si no se entrega en ese plazo adicional, la calificación es reprobatoria."),
  ("p", "Artículo 27. Asesor académico. Todo estudiante cuenta con un profesor asesor académico que lo orienta "
        "en la matrícula, la selección de asignaturas y los trámites académicos."),
 ],
 [("h2", "Reingreso, reintegro, transferencia y homologación"),
  ("p", "Artículo 34. Definiciones. Reingreso: solicitud de quien perdió la calidad de estudiante por no cumplir "
        "las normas académicas o disciplinarias; si fue por razones académicas la analiza el jefe del programa, "
        "y si fue por razones disciplinarias la analiza el Comité de Casos del Consejo Académico. Reintegro: "
        "solicitud de quien fue estudiante regular y se retiró voluntariamente. Transferencia interna: paso de "
        "un programa de pregrado de EAFIT a otro. Transferencia externa: solicitud de quien viene de otra "
        "institución de educación superior. Todas se hacen dentro de las fechas del calendario académico."),
  ("p", "Artículo 35. Homologación de créditos. Es el reconocimiento, como parte del plan de estudios, de "
        "créditos aprobados en un pregrado de EAFIT, en un pregrado de otra institución de educación superior, "
        "en el Programa de Estudios Generales o en microcredenciales de EAFIT. También pueden reconocerse "
        "asignaturas con base en certificaciones de bachillerato internacional (Cambridge, College Board o IB)."),
  ("p", "Artículo 36. Homologación entre programas de EAFIT. Se hace con base en la tabla de equivalencias "
        "vigente, elaborada por el Comité del Programa de Pregrado y revisada cada tres años o cuando haya una "
        "reforma académica. El estudiante queda ubicado en el plan de estudios vigente al momento del cambio."),
  ("p", "Artículo 37. Homologación de créditos de otra institución. La resuelve el jefe del programa de "
        "pregrado, teniendo en cuenta el programa detallado de la asignatura, sus objetivos, la intensidad "
        "horaria, el año de aprobación, la calificación obtenida y la calidad académica del programa y de la "
        "institución de origen (la acreditación de alta calidad puede ser un criterio). La homologación solo "
        "tiene lugar en el momento de la admisión, con los documentos aportados en el proceso de ingreso; no se "
        "homologa con documentos presentados después de la matrícula, salvo los casos de movilidad estudiantil, "
        "que define el Comité del Programa. Para optar al título, todo estudiante debe cursar y aprobar en "
        "EAFIT no menos del 60 % de los créditos del programa. La homologación puede exigir el pago de derechos "
        "pecuniarios."),
  ("h2", "Matrícula"),
  ("p", "Artículo 38. Matrícula. La matrícula vale por un solo período académico y debe renovarse antes del "
        "siguiente. No se puede renovar matrícula con calificaciones pendientes ni sin estar a paz y salvo con "
        "la Universidad. La matrícula se perfecciona con el pago de los derechos pecuniarios."),
  ("p", "Artículo 40. Matrícula extraordinaria. La matrícula que se hace por fuera de las fechas ordinarias es "
        "extraordinaria y causa un recargo del 20 % sobre el valor de los derechos de matrícula."),
  ("p", "Artículo 42. Condición de estudiante. Se obtiene al pagar la matrícula u obtener su financiación antes "
        "del plazo. Vencido el plazo se acepta el pago con recargo sin pasar de la segunda semana de clase; si "
        "al terminar la segunda semana no se ha pagado, la matrícula se revierte y el estudiante es retirado de "
        "las listas de clase."),
  ("p", "Artículo 48. Suspensión del período académico. Por razones de salud o de seguridad certificadas, el "
        "estudiante puede pedir por escrito la suspensión del período en curso; la resuelve el decano de la "
        "Escuela. Debe continuar en el período siguiente y matricula sin costo las asignaturas que quedaron "
        "pendientes por la suspensión."),
 ],
 [("h2", "Cancelación de créditos, pérdida de asignaturas y permanencia"),
  ("p", "Artículo 49. Cancelación de créditos académicos. Durante cada período académico el estudiante puede "
        "cancelar créditos matriculados con estas reglas. (a) La cancelación parcial no puede superar el 50 % "
        "de los créditos totales matriculados en el período; además, la asignatura no puede haber sido evaluada "
        "en más del 75 % (lo verifica el profesor) y no se puede pasar de la fecha límite de cancelación que "
        "fija el Consejo Académico en el calendario académico de cada año. (b) Los créditos de la práctica "
        "estudiantil no se pueden cancelar, salvo fuerza mayor o caso fortuito comprobado ante el Comité de "
        "Casos. (c) Cancelar todos los créditos matriculados en un período termina el contrato de servicios "
        "educativos e implica la pérdida de la condición de estudiante; para volver hay que hacer el trámite de "
        "reintegro y la readmisión es potestativa de la Universidad. (d) El estudiante con matrícula "
        "condicional no puede cancelar ninguno de los créditos matriculados, salvo fuerza mayor o caso fortuito "
        "comprobado."),
  ("p", "Artículo 50. Efectos económicos de la cancelación. La cancelación total o parcial puede originar o no "
        "una devolución o saldo a favor, según lo previsto en el Reglamento Económico."),
  ("p", "Artículo 52. Pérdida de asignaturas. El estudiante que pierde una o más asignaturas, sin perder la "
        "condición de estudiante regular, puede escoger el período académico en el que las repite, siempre que "
        "cumpla los prerrequisitos y correquisitos de su plan de estudios. El artículo no establece un número "
        "máximo de veces que se puede repetir una asignatura."),
  ("p", "Artículo 53. Pérdida de la condición de estudiante. Se pierde, al finalizar el período, por una "
        "infracción académica o disciplinaria que lo amerite; por terminar el período con matrícula condicional "
        "sin cumplir sus requisitos; por recibir una consecuencia disciplinaria estando con matrícula "
        "condicional; por incumplir el Reglamento de Experiencias de Talento; o por incumplir los trámites de "
        "matrícula."),
  ("p", "Artículo 54. Retiro por rendimiento académico. También se pierde la condición de estudiante de un "
        "programa en estos casos: (a) quien al finalizar su primera matrícula obtiene un promedio crédito "
        "semestral inferior a 2.5; (b) quien ha tenido hasta tres matrículas semestrales y al finalizar el "
        "último período registra promedio crédito semestral inferior a 2.8 y promedio crédito acumulado "
        "inferior a 2.8; (c) quien ha tenido cuatro o más matrículas semestrales y registra promedio crédito "
        "semestral inferior a 3.0 y promedio crédito acumulado inferior a 3.0. Quien es retirado por los "
        "literales (a) o (b) puede inscribirse en el período siguiente en cualquier pregrado y no queda con "
        "matrícula condicional. Para (a) y (b) no cuentan las matrículas canceladas dentro de las dos primeras "
        "semanas del semestre."),
  ("p", "Artículo 55. Matrícula condicional. Es la figura con la que reingresa, por decisión del jefe del "
        "programa, el estudiante con cuatro o más matrículas cuyo promedio semestral y acumulado quedó por "
        "debajo de 3.0. Debe acogerse al plan vigente, cursar todas las asignaturas acordadas con el asesor "
        "académico, hacer el programa de acompañamiento pedagógico y obtener promedio crédito semestral y "
        "acumulado igual o superior a 3.0 al terminar ese período."),
  ("h2", "Doble programa de pregrado"),
  ("p", "Artículos 56 a 61. Doble programa. EAFIT permite cursar dos pregrados a la vez y homologar créditos "
        "entre ellos. Requisitos de inscripción (artículo 59): ser estudiante activo de un pregrado, haber "
        "aprobado 30 créditos como estudiante regular y tener un promedio crédito acumulado mínimo de 3.4. Los "
        "promedios son independientes para cada programa (artículo 58). Si es retirado por rendimiento de uno "
        "de los programas puede seguir en el otro; si es retirado por sanción disciplinaria no puede seguir en "
        "ninguno. Pierde la condición de doble programa quien se retira o abandona uno de los dos (artículo 61)."),
 ],
 [("h2", "Evaluaciones"),
  ("p", "Artículo 65. Programación de las evaluaciones. En la primera clase el profesor presenta el programa de "
        "la asignatura, con las evaluaciones, sus porcentajes y sus fechas. Esa programación no puede "
        "modificarse sin el consentimiento de todos los estudiantes matriculados, salvo fuerza mayor."),
  ("p", "Artículo 66. Tipos de evaluaciones. Las evaluaciones parciales valen entre el 15 % y el 25 % de la "
        "calificación total de la asignatura. La evaluación final no puede valer más del 30 %. Las evaluaciones "
        "supletorias reemplazan parciales o finales que no se pudieron presentar por fuerza mayor o caso "
        "fortuito comprobado, o por estar representando a la Universidad, al municipio, al departamento o a la "
        "nación en una actividad académica, deportiva o cultural."),
  ("p", "Artículo 69. Inasistencia a las evaluaciones. Quien no presenta una actividad evaluativa en la fecha y "
        "hora fijadas obtiene una calificación de 0.0, salvo fuerza mayor o caso fortuito comprobado."),
  ("p", "Artículo 70. Evaluaciones supletorias. Deben presentarse a más tardar dentro de los diez días "
        "calendario siguientes a la terminación de la causa que motivó el aplazamiento, previa solicitud al "
        "profesor por el sistema de información y con los soportes. Si el profesor la niega, el estudiante "
        "puede acudir al jefe del programa. Deben tener la misma forma, dificultad y tema que la evaluación que "
        "reemplazan y no causan pago de derechos (artículo 72)."),
  ("p", "Artículo 71. Exámenes de validación. Acreditan el conocimiento de una asignatura sin cursarla. Los "
        "autoriza el jefe de programa, se matriculan y pagan como créditos, y se presentan ante un jurado de "
        "dos o tres profesores. Constan de una prueba oral y una escrita en días distintos; la nota definitiva "
        "es el promedio de ambas y no admite segundo calificador. No se puede validar una asignatura que ya se "
        "reprobó, y cada asignatura solo se puede validar una única vez. Si se reprueba, queda como asignatura "
        "cursada y perdida."),
  ("p", "Artículo 73. Revisión de las evaluaciones. El estudiante tiene derecho a la realimentación y a conocer "
        "su calificación a más tardar quince días calendario después de la evaluación, y tres días calendario "
        "en el caso de los exámenes finales. Para reclamar por una calificación puede pedir la revisión en el "
        "momento de la realimentación o por escrito al profesor dentro de los tres días hábiles siguientes; el "
        "profesor tiene cinco días hábiles para responder."),
  ("p", "Artículo 74. Segundo calificador. Si el estudiante no está de acuerdo con la decisión del profesor, "
        "puede pedir por escrito un segundo calificador al jefe del núcleo o al jefe del pregrado, dentro de "
        "los tres días hábiles siguientes a la realimentación. El segundo calificador se designa en dos días "
        "hábiles, recalifica en tres días hábiles, actúa de forma anónima y su decisión es definitiva."),
  ("h2", "Calificaciones"),
  ("p", "Artículo 76. Escala de calificaciones. Las calificaciones van de 0.0 a 5.0 con una sola cifra decimal. "
        "Las centésimas se aproximan: de 5 a 9 sube la décima (2.95 queda en 3.0) y de 0 a 4 se mantiene (2.94 "
        "queda en 2.9). Una asignatura se aprueba con calificación definitiva de 3.0 o superior, o con la "
        "calificación cualitativa A (Aprobada), que no entra en el cálculo del promedio. El promedio crédito "
        "semestral y el acumulado no se aproximan."),
  ("h2", "Reconocimientos"),
  ("p", "Artículos 81 y 82. Matrícula de honor. Exonera del pago de los créditos del período siguiente. Se "
        "otorga a quien obtiene el máximo promedio crédito del período en su pregrado, siempre que sea superior "
        "a 4.5, haya cursado mínimo 18 créditos en el período, no esté repitiendo ninguna asignatura y no esté "
        "optando al título en ese período. Se concede una por cada 400 estudiantes del programa. Una "
        "consecuencia disciplinaria en el período hace perder el reconocimiento."),
  ("p", "Artículo 83. Mención de honor por promedio crédito acumulado. Se otorga al mejor graduando de pregrado "
        "de cada Escuela, con promedio crédito acumulado mínimo de 4.5 y sin consecuencias disciplinarias. El "
        "reconocimiento es el pago de la matrícula de un posgrado de EAFIT (no doctorados ni programas en "
        "convenio), que debe iniciarse en un plazo máximo de dos años."),
  ("p", "Artículo 84. Mención de honor al trabajo de grado. Requiere, entre otros criterios, calificación de "
        "5.0 en el trabajo de grado y promedio crédito acumulado igual o superior a 4.0."),
 ],
]

# ----------------------------------------------------------------------------------------------
# 2. Plan de estudios de Ingeniería de Sistemas 2025-1 (semestres 1 a 6)
# ----------------------------------------------------------------------------------------------
PLAN_URL = "https://www.eafit.edu.co/pregrado-ingenieria-de-sistemas-2025/plan-de-estudio"
# (nombre, código, créditos, UMES, núcleo, prerrequisitos, correquisitos)
plan = {
 1: [("Inducción", "BU0009", "0", "0", "Inducción y Bienestar Universitario", [], []),
     ("Bienestar Universitario", "BU0011", "1", "1", "Inducción y Bienestar Universitario", [], ["Taller de Salud (BU0600)"]),
     ("Taller de Salud", "BU0600", "0", "0", "Inducción y Bienestar Universitario", [], []),
     ("Expresión Gráfica", "CI1001", "3", "4", "Básicas en Ingeniería (ECAI)", [], []),
     ("Cálculo I", "NM1001", "3", "4", "Matemáticas y Ciencias Básicas", [], []),
     ("Matemáticas para la computación", "NM1008", "3", "4", "Matemáticas y Ciencias Básicas", [], []),
     ("Proyecto Escuela", "CI1002", "3", "4", "Básicas en Ingeniería (ECAI)", [], []),
     ("Pensamiento computacional (NFI 1)", "", "3", "", "Plan de estudios del programa", [], []),
     ("Ciudadanía y Democracia (NFI 2)", "", "3", "", "Formación Institucional (ECAI)", [], [])],
 2: [("Prueba de Lectura 1", "LE0001", "", "", "Plan de estudios del programa", [], []),
     ("Prueba de Escritura 1", "LE0002", "", "", "Plan de estudios del programa", [], []),
     ("Física I", "NC1001", "3", "5", "Matemáticas y Ciencias Básicas", ["Cálculo I (NM1001)"], []),
     ("Cálculo II", "NM1002", "3", "4", "Matemáticas y Ciencias Básicas", [], ["Cálculo I (NM1001)"]),
     ("Álgebra Lineal", "NM1003", "3", "4", "Matemáticas y Ciencias Básicas", [], []),
     ("Teoría de la computación", "SI1001", "3", "4", "Asignaturas disciplinares", ["Matemáticas para la computación (NM1008)"], []),
     ("Lenguajes y Paradigmas de Programación", "SI1002", "3", "4", "Asignaturas disciplinares", ["NFI - Pensamiento Computacional (FH1037)"], []),
     ("NFI 3", "", "3", "", "Formación Institucional (ECAI)", [], [])],
 3: [("Cálculo III", "NM2001", "3", "4", "Matemáticas y Ciencias Básicas", ["Cálculo II (NM1002)", "Álgebra Lineal (NM1003)"], []),
     ("Probabilidad y Estadística", "NM2002", "3", "4", "Matemáticas y Ciencias Básicas", ["Cálculo II (NM1002)"], []),
     ("Estructura de datos y algoritmos", "SI2001", "3", "4", "Asignaturas disciplinares", ["Lenguajes y Paradigmas de Programación (SI1002)"], []),
     ("Lenguajes formales", "SI2002", "3", "4", "Asignaturas disciplinares", ["Teoría de la computación (SI1001)"], []),
     ("Sistemas de gestión de datos", "SI2003", "3", "5", "Asignaturas disciplinares",
      ["Lenguajes y Paradigmas de Programación (SI1002)", "Prueba de Lectura 1 (LE0001)", "Prueba de Escritura 1 (LE0002)"], []),
     ("Talento I - Escuela de Ciencias Aplicadas e Ingeniería", "TA2003", "0", "0", "Núcleo de Formación Institucional", ["Física I (NC1001)"], []),
     ("NFI 4", "", "3", "", "Formación Institucional (ECAI)", [], [])],
 4: [("Prueba de Lectura 2", "LE0003", "", "", "Plan de estudios del programa", ["Prueba de Lectura 1 (LE0001)"], []),
     ("Prueba de Escritura 2", "LE0004", "", "", "Plan de estudios del programa", ["Prueba de Escritura 1 (LE0002)"], []),
     ("Física II", "NC2001", "3", "5", "Matemáticas y Ciencias Básicas", ["Física I (NC1001)"], ["Cálculo II (NM1002)"]),
     ("Sistemas operativos", "SI2004", "3", "5", "Asignaturas disciplinares", ["Estructura de datos y algoritmos (SI2001)", "Cumplimiento A1 Bilingüismo"], []),
     ("Ingeniería de Software", "SI2005", "3", "5", "Asignaturas disciplinares",
      ["Sistemas de gestión de datos (SI2003)", "Talento I - Escuela de Ciencias Aplicadas e Ingeniería (TA2003)"], []),
     ("Organización de computadores", "SI2007", "3", "4", "Asignaturas disciplinares", ["Estructura de datos y algoritmos (SI2001)"], []),
     ("Sistemas de información", "SI2008", "3", "4", "Asignaturas disciplinares", [], ["Ingeniería de Software (SI2005)"]),
     ("Proyecto integrador 1", "ST0251", "3", "4", "Plan de estudios del programa", ["Cumplimiento A1 Bilingüismo"], ["Ingeniería de Software (SI2005)"]),
     ("Electiva matemáticas 1", "", "3", "4", "Matemáticas y Ciencias Básicas", [], [])],
 5: [("Arquitectura de Software", "SI3001", "3", "4", "Asignaturas disciplinares", ["Ingeniería de Software (SI2005)"], []),
     ("Internet, Arquitectura y Protocolos", "SI3002", "3", "5", "Asignaturas disciplinares", ["Sistemas operativos (SI2004)"], []),
     ("Inteligencia Artificial", "SI3003", "3", "4", "Asignaturas disciplinares", ["Estructura de datos y algoritmos (SI2001)"],
      ["Análisis y Diseño de Algoritmos (SI3005)", "Arquitectura de Software (SI3001)"]),
     ("Proyecto II", "SI3004", "3", "5", "Línea de Proyectos",
      ["Ingeniería de Software (SI2005)", "Proyecto integrador 1 (ST0251)", "Proyecto de Escuela (CI1002)"], []),
     ("Análisis y Diseño de Algoritmos", "SI3005", "3", "4", "Asignaturas disciplinares", ["Estructura de datos y algoritmos (SI2001)"], []),
     ("Electiva matemáticas 2", "", "3", "4", "Matemáticas y Ciencias Básicas", [], [])],
 6: [("Ciberseguridad", "SI3006", "3", "4", "Asignaturas disciplinares", ["Internet, Arquitectura y Protocolos (SI3002)"], []),
     ("Trayectoria 1 Curso 1", "", "3", "", "Plan de estudios del programa", [], ["Trayectoria 1 Curso 2"]),
     ("Trayectoria 1 Curso 2", "", "3", "", "Plan de estudios del programa", [], ["Trayectoria 1 Curso 3"]),
     ("Trayectoria 2 Curso 1", "", "3", "", "Plan de estudios del programa", [], ["Trayectoria 2 Curso 2"]),
     ("Trayectoria Flexible 1", "", "", "", "Trayectorias flexibles (ECAI)", [], []),
     ("NFI 5", "", "3", "", "Formación Institucional (ECAI)", [], [])],
}


def course_text(sem, c):
    name, code, cred, umes, nucleo, pre, co = c
    s = f"<b>{name}</b>" + (f" (código {code})" if code else " (sin código publicado)") + f". Semestre {sem}. "
    s += (f"{cred} créditos" if cred else "Créditos no indicados en la página") + (f", {umes} UMES. " if umes else ". ")
    s += f"Núcleo o clasificación: {nucleo}. "
    s += ("Prerrequisitos: " + "; ".join(pre) + ". ") if pre else "Prerrequisitos: ninguno publicado. "
    s += ("Correquisitos: " + "; ".join(co) + ".") if co else "Correquisitos: ninguno publicado."
    return s


plan_pages = []
for sem, courses in plan.items():
    page = []
    if sem == 1:
        page += [("h1", "Plan de estudios de Ingeniería de Sistemas - Universidad EAFIT"),
                 ("h2", "Plan vigente a partir de 2025-1 (estudiantes nuevos). Semestres 1 a 6"),
                 ("n", "Documento de trabajo elaborado por el equipo del proyecto final de SI3003 con la información "
                       "publicada por la Universidad EAFIT en " + PLAN_URL + ", consultada el 17 de noviembre de 2026. "
                       "El programa tiene una duración de 9 semestres. Este documento incluye los semestres 1 a 6; los "
                       "semestres 7, 8 y 9 no se pudieron consultar y no están incluidos, por lo que no contiene el total "
                       "de créditos del programa. Las asignaturas sin código son espacios que el estudiante elige "
                       "(NFI: Núcleo de Formación Institucional; trayectorias; electivas). UMES es la unidad que la "
                       "página muestra junto a los créditos. La malla oficial en PDF está enlazada en esa misma página.")]
    total = sum(int(c[2]) for c in courses if c[2])
    extra = " (sin contar las asignaturas cuyos créditos no aparecen publicados)" if any(not c[2] for c in courses) else ""
    page.append(("h2", f"Semestre {sem} de Ingeniería de Sistemas (plan 2025-1)"))
    page.append(("p", f"El semestre {sem} del plan 2025-1 de Ingeniería de Sistemas tiene {len(courses)} asignaturas "
                      f"que suman {total} créditos{extra}."))
    page += [("p", course_text(sem, c)) for c in courses]
    plan_pages.append(page)

if __name__ == "__main__":
    DOCS.mkdir(exist_ok=True)
    build("reglamento-academico-pregrado-eafit-resumen.pdf", reg)
    build("plan-estudios-ingenieria-sistemas-2025-1.pdf", plan_pages)

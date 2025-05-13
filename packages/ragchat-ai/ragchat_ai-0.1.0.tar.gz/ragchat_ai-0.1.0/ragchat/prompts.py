from ragchat.definitions import Prompt, Translations, Example

MSG_CLASSIFICATION = Prompt(prompt_type="system", prompt=Translations(

en="""
Task: Classify the INPUT as 'statement', 'question', 'none'.

Definitions:
- statement: A declaration, assertion or instruction.
- question: An interrogative message seeking information.
- none: The input is incoherent, empty or does not fit into any category.

Instructions:
- Don't answer questions or provide explanations, just classify the message.
- Write 'statement' or 'question' or 'none'
""",

es="""
Tarea: Clasifica la ENTRADA como 'statement', 'question' o 'none'.

Definiciones:
- statement: Una declaración, afirmación o instrucción.
- question: Un mensaje interrogativo que busca información.
- none: La entrada es incoherente, está vacía o no encaja en ninguna categoría.

Instrucciones:
- No respondas preguntas ni des explicaciones, solo clasifica el mensaje.
- Escribe 'statement' o 'question' o 'none'
""",

fr="""
Tâche : Classifier l'ENTRÉE comme 'statement', 'question' ou 'none'.

Définitions :
- statement : Une déclaration, une affirmation ou une instruction.
- question : Un message interrogatif cherchant à obtenir des informations.
- none : L'entrée est incohérente, vide ou ne correspond à aucune catégorie.

Instructions :
- Ne répondez pas aux questions et ne donnez pas d'explications, classez simplement le message.
- Écrivez 'statement', 'question' ou 'none'
""",

de="""
Aufgabe: Klassifiziere die EINGABE als 'statement', 'question' oder 'none'.

Definitionen:
- statement: Eine Aussage, Behauptung oder Anweisung.
- question: Eine Frage, die nach Informationen sucht.
- none: Die Eingabe ist unzusammenhängend, leer oder passt in keine Kategorie.

Anweisungen:
- Beantworte keine Fragen und gib keine Erklärungen, sondern klassifiziere nur die Nachricht.
- Schreibe 'statement', 'question' oder 'none'
""",

), examples=[

Example(flow="chat", example_input=Translations(
en="""Is it true that the Kingdom of Italy was proclaimed in 1861, while the French Third Republic was established in 1870 and therefore Italy is technically older?""",
es="""¿Es cierto que el Reino de Italia fue proclamado en 1861, mientras que la Tercera República Francesa se estableció en 1870 y por lo tanto Italia es técnicamente más antigua?""",
fr=""""Est-il vrai que le Royaume d'Italie a été proclamé en 1861, tandis que la Troisième République française a été établie en 1870 et que l'Italie est donc techniquement plus ancienne?""",
de="""Stimmt es, dass das Königreich Italien 1861 ausgerufen wurde, während die Dritte Französische Republik 1870 gegründet wurde und Italien somit technisch älter ist?""",
),
example_output=Translations(
en="question",
es="question",
fr="question",
de="question",
)),

Example(flow="chat", example_input=Translations(
en="""Paris is the capital of France. Rome is the capital of Italy.""",
es="""París es la capital de Francia. Roma es la capital de Italia.""",
fr=""""Paris est la capitale de la France. Rome est la capitale de l'Italie.""",
de="""Paris ist die Hauptstadt Frankreichs. Rom ist die Hauptstadt Italiens.""",
),
example_output=Translations(
en="statement",
es="statement",
fr="statement",
de="statement",
)),

Example(flow="chat", example_input=Translations(
en="""Florp wizzlebop cronkulated the splonk! Zizzleflap {}[]()<>:;"/|,.<>? drumblesquanch, but only if the quibberflitz jibberflops. Blorp???""",
es="""¡Florp wizzlebop cronkuleó el splonk! ¡Zizzleflap {}[]()<>:;"/|,.<>? drumblecuancha, pero solo si el quibberflitz jibberflops! ¡Blorp???""",
fr="""Florp wizzlebop a cronkulé le splonk ! Zizzleflap {}[]()<>:;"/|,.<>? drumblecuancha, mais seulement si le quibberflitz jibberflops. Blorp ???""",
de="""Florp wizzlebop hat den Splonk cronkuliert! Zizzleflap {}[]()<>:;"/|,.<>? drumblecuancha, aber nur wenn der quibberflitz jibberflops. Blorp???""",
),
example_output=Translations(
en="none",
es="none",
fr="none",
de="none",
)),
])

TOPICS = Prompt(prompt_type="system", prompt=Translations(

en="""
Task: Extract distinctive topics.

Instructions:
- Extract topics from the INPUT text
- The topics should be concise and serve as differentiators from similar texts
- If the INPUT is incoherent or invalid, list 'None'
- No explanations, just output in markdown format:
## Distinctive topics
- [topic]
""",

es="""
Tarea: Extraer temas distintivos.

Instrucciones:
- Extraer temas del texto INPUT
- Los temas deben ser concisos y servir como diferenciadores de textos similares
- Si el INPUT es incoherente o inválido, listar 'None'
- Nada de explicaciones, solo escribe en formato markdown:
## Temas distintivos
- [tema]
""",

fr="""
Tâche : Extraire des sujets distinctifs.

Instructions :
- Extraire les sujets du texte INPUT
- Les sujets doivent être concis et servir de différenciateurs par rapport à des textes similaires
- Si l'INPUT est incohérent ou invalide, lister 'None'
- Pas d'explications, juste la sortie au format markdown :
## Sujets distinctifs
- [sujet]
""",

de="""
Aufgabe: Unterscheidende Themen extrahieren.

Anweisungen:
- Themen aus dem INPUT Text extrahieren
- Die Themen sollten prägnant sein und als Unterscheidungsmerkmale zu ähnlichen Texten dienen
- Wenn der INPUT inkohärent oder ungültig ist, 'None' auflisten
- Keine Erklärungen, nur die Ausgabe im Markdown-Format:
## Unterscheidende Themen
- [Thema]
"""
), examples=[

Example(flow="chat", example_input=Translations(
en="""
I had dinner with my family last night. My husband cooked lasagna, which is my daughter's favorite dish. Our son brought his girlfriend, who we met for the first time. She brought a lovely bottle of wine that paired perfectly with the meal.

Optional topics:
- Family dinner
- Breakfast with friends
""",
es="""
Cené con mi familia anoche. Mi esposo cocinó lasaña, que es el plato favorito de mi hija. Nuestro hijo trajo a su novia, a quien conocimos por primera vez. Ella trajo una botella de vino estupenda que maridó perfectamente con la comida.

Temas opcionales:
- Cena familiar
- Desayuno con amigos
""",
fr="""
J'ai dîné avec ma famille hier soir. Mon mari a cuisiné des lasagnes, qui est le plat préféré de ma fille. Notre fils a amené sa petite amie, que nous rencontrions pour la première fois. Elle a apporté une jolie bouteille de vin qui s'est parfaitement accordée avec le repas.

Sujets optionnels:
- Dîner en famille
- Petit-déjeuner entre amis
""",
de="""
Ich habe gestern Abend mit meiner Familie zu Abend gegessen. Mein Mann hat Lasagne gekocht, was das Lieblingsgericht meiner Tochter ist. Unser Sohn hat seine Freundin mitgebracht, die wir zum ersten Mal kennenlernten. Sie hat eine schöne Flasche Wein mitgebracht, die perfekt zum Essen passte.

Optionale Themen:
- Familienessen
- Frühstück mit Freunden
""",
), example_output=Translations(
en="""
## Distinctive topics
- Family dinner
- Meeting son's girlfriend (first time)
""",
es="""
## Temas distintivos
- Cena familiar
- Conocer a la novia del hijo (primera vez)
""",
fr="""
## Sujets distinctifs
- Dîner en famille
- Rencontrer la petite amie du fils (première fois)
""",
de="""
## Unterscheidende Themen
- Familienessen
- Die Freundin des Sohnes kennenlernen (erstes Mal)
""",
)),

Example(flow="file", example_input=Translations(
en="""
Eukaryotic cells, the building blocks of complex life, are thought to have evolved from simpler prokaryotic cells through a process called endosymbiosis, where one prokaryotic cell engulfed another, leading to the development of membrane-bound organelles.
Eukaryotic cells have internal organization with a plasma membrane, cytoplasm containing organelles like mitochondria (energy), endoplasmic reticulum (synthesis), and a nucleus (genetic information) enclosed by a nuclear envelope.

Optional topics:
- Prokaryotic Cells
- Evolution of Eukaryotic Cells (early evolution from Prokaryotes)
""",
es="""
Se cree que las células eucariotas, los bloques de construcción de la vida compleja, evolucionaron a partir de células procariotas más simples a través de un proceso llamado endosimbiosis, donde una célula procariota engulló a otra, lo que llevó al desarrollo de orgánulos unidos a la membrana.
Las células eucariotas tienen organización interna con una membrana plasmática, citoplasma que contiene orgánulos como las mitocondrias (energía), retículo endoplasmático (síntesis) y un núcleo (información genética) encerrado por una envoltura nuclear.

Temas opcionales:
- Células procariotas
- Evolución de las células eucariotas (evolución temprana a partir de procariotas)
""",
fr="""
Les cellules eucaryotes, les éléments constitutifs de la vie complexe, sont considérées comme ayant évolué à partir de cellules procaryotes plus simples par un processus appelé endosymbiose, où une cellule procaryote en a englouti une autre, conduisant au développement d'organites liés à la membrane.
Les cellules eucaryotes ont une organisation interne avec une membrane plasmique, un cytoplasme contenant des organites comme les mitochondries (énergie), le réticulum endoplasmique (synthèse), et un noyau (information génétique) entouré d'une enveloppe nucléaire.

Sujets optionnels:
- Cellules procaryotes
- Évolution des cellules eucaryotes (évolution précoce à partir des procaryotes)
""",
de="""
Eukaryotische Zellen, die Bausteine komplexen Lebens, sollen sich aus einfacheren prokaryotischen Zellen durch einen Prozess namens Endosymbiose entwickelt haben, bei dem eine prokaryotische Zelle eine andere verschlang, was zur Entwicklung membranumhüllter Organellen führte.
Eukaryotische Zellen haben eine innere Organisation mit einer Plasmamembran, Zytoplasma, das Organellen wie Mitochondrien (Energie), endoplasmatisches Retikulum (Synthese) und einen Zellkern (genetische Information), umschlossen von einer Kernhülle, enthält.

Optionale Themen:
- Prokaryotische Zellen
- Evolution der Eukaryotischen Zellen (frühe Evolution aus Prokaryoten)
""",
), example_output=Translations(
en="""
## Distinctive topics
- Evolution of Eukaryotic Cells (early evolution from Prokaryotes)
- Eukaryotic Cells
""",
es="""
## Temas distintivos
- Evolución de las células eucariotas (evolución temprana a partir de procariotas)
- Células eucariotas
""",
fr="""
## Sujets distinctifs
- Évolution des cellules eucaryotes (évolution précoce à partir des procaryotes)
- Cellules eucaryotes
""",
de="""
## Unterscheidende Themen
- Evolution der Eukaryotischen Zellen (frühe Evolution aus Prokaryoten)
- Eukaryotische Zellen
""",
)),
])

TOPIC_FACTS = Prompt(prompt_type="system", prompt=Translations(

en="""
Task: Extract all topics and facts.

Instructions:
- Strictly use the topics from INPUT as headings, do not modify them, do not add new ones
- Extract all facts from the INPUT, facts should be concise and unambiguous
- List the facts under their respective topic, facts may repeat across topics
- Use names instead of pronouns
- If the INPUT is incoherent or invalid, list 'None'
- No explanations, just output in markdown format:
## [topic]
- [fact]
""",

es="""
Tarea: Extraer todos los temas y hechos.

Instrucciones:
- Utiliza estrictamente los temas del INPUT como encabezados, no los modifiques, no añadas nuevos
- Extrae todos los hechos del INPUT, los hechos deben ser concisos y no ambiguos
- Lista los hechos bajo su tema respectivo, los hechos pueden repetirse entre temas
- Usa nombres en lugar de pronombres
- Si el INPUT es incoherente o inválido, lista 'None'
- Nada de explicaciones, solo escribe en formato markdown:
## [tema]
- [hecho]
""",

fr="""
Tâche: Extraire tous les sujets et faits.

Instructions:
- Utilise strictement les sujets de l'INPUT comme titres, ne les modifie pas, n'en ajoute pas de nouveaux
- Extrais tous les faits de l'INPUT, les faits doivent être concis et non ambigus
- Liste les faits sous leur sujet respectif, les faits peuvent se répéter entre les sujets
- Utilise des noms au lieu de pronoms
- Si l'INPUT est incohérent ou invalide, liste 'None'
- Pas d'explications, juste la sortie au format markdown :
## [sujet]
- [fait]
""",

de="""
Aufgabe: Extrahieren Sie alle Themen und Fakten.

Anweisungen:
- Verwenden Sie strikt die Themen aus dem INPUT als Überschriften, ändern Sie sie nicht, fügen Sie keine neuen hinzu
- Extrahieren Sie alle Fakten aus dem INPUT, Fakten sollten prägnant und eindeutig sein
- Listen Sie die Fakten unter ihrem jeweiligen Thema auf, Fakten können sich über Themen hinweg wiederholen
- Verwenden Sie Namen anstelle von Pronomen
- Wenn der INPUT inkohärent oder ungültig ist, listen Sie 'None' auf
- Keine Erklärungen, geben Sie nur die Ausgabe im Markdown-Format aus:
## [Thema]
- [Fakt]
""",

), examples=[

Example(flow="chat", example_input=Translations(
en="""
current timestamp: 2023-02-12 13:30

# Topics
## Family dinner
## Meeting son's girlfriend (first time)

I had dinner with my family last night. My husband cooked lasagna, which is my daughter's favorite dish. Our son brought his girlfriend, who we were meeting for the first time. She brought a lovely bottle of wine that paired perfectly with the meal.
""",
es="""
current timestamp: 2023-02-12 13:30

# Temas
## Cena familiar
## Conocer a la novia del hijo (primera vez)

Anoche cené con mi familia. Mi esposo cocinó lasaña, que es el plato favorito de mi hija. Nuestro hijo trajo a su novia, a quien conocíamos por primera vez. Ella trajo una botella de vino encantadora que maridó perfectamente con la comida.
""",
fr="""
current timestamp: 2023-02-12 13:30

# Sujets
## Dîner en famille
## Rencontrer la petite amie du fils (première fois)

J'ai dîné avec ma famille hier soir. Mon mari a cuisiné des lasagnes, qui est le plat préféré de ma fille. Notre fils a amené sa petite amie, que nous rencontrions pour la première fois. Elle a apporté une charmante bouteille de vin qui s'est parfaitement accordée avec le repas.
""",
de="""
current timestamp: 2023-02-12 13:30

# Themen
## Familienessen
## Die Freundin des Sohnes kennenlernen (erstes Mal)

Gestern Abend habe ich mit meiner Familie zu Abend gegessen. Mein Mann hat Lasagne gekocht, das Lieblingsgericht meiner Tochter. Unser Sohn hat seine Freundin mitgebracht, die wir zum ersten Mal trafen. Sie hat eine schöne Flasche Wein mitgebracht, die perfekt zum Essen passte.
""",
), example_output=Translations(
en="""
## Family dinner
- The user had dinner with the user's family (last night from 2023-02-12 13:30).
- The user's husband cooked lasagna.
- Lasagna is the user's daughter's favorite dish.
- The user's son brought his girlfriend to the family dinner.
- The girlfriend brought a lovely bottle of wine.
- The wine paired perfectly with the meal.
## Meeting son's girlfriend (first time)
- The user met the user's son's girlfriend (first time).
- The user's son brought his girlfriend to the family dinner.
- The girlfriend brought a lovely bottle of wine.
""",
es="""
## Cena familiar
- El usuario/a cenó con su familia (anoche, desde el 12-02-2023 13:30).
- El marido del usuario/a cocinó lasaña.
- La lasaña es el plato favorito de la hija del usuario/a.
- El hijo del usuario/a trajo a su novia a la cena familiar.
- La novia trajo una botella de vino encantadora.
- El vino maridó perfectamente con la comida.
## Conocer a la novia del hijo (primera vez)
- El usuario/a conoció a la novia de su hijo (primera vez).
- El hijo del usuario/a trajo a su novia a la cena familiar.
- La novia trajo una botella de vino encantadora.
""",
fr="""
## Dîner de famille
- L'utilisateur/trice a dîné avec sa famille (hier soir à partir du 12-02-2023 13:30).
- Le mari de l'utilisateur/trice a cuisiné des lasagnes.
- Les lasagnes sont le plat préféré de la fille de l'utilisateur/trice.
- Le fils de l'utilisateur/trice a amené sa petite amie au dîner de famille.
- La petite amie a apporté une charmante bouteille de vin.
- Le vin s'est parfaitement accordé avec le repas.
## Rencontre avec la petite amie du fils (première fois)
- L'utilisateur/trice a rencontré la petite amie de son fils (première fois).
- Le fils de l'utilisateur/trice a amené sa petite amie au dîner de famille.
- La petite amie a apporté une charmante bouteille de vin.
""",
de="""
## Familienessen
- Der Benutzer/in hat mit seiner Familie zu Abend gegessen (gestern Abend ab 13:30 Uhr am 12.02.2023).
- Der Ehemann des Benutzer/in hat Lasagne gekocht.
- Lasagne ist das Lieblingsgericht der Tochter des Benutzer/in.
- Der Sohn des Benutzer/in hat seine Freundin zum Familienessen mitgebracht.
- Die Freundin hat eine schöne Flasche Wein mitgebracht.
- Der Wein passte perfekt zum Essen.
## Treffen mit der Freundin des Sohnes (erstes Mal)
- Der Benutzer/in hat die Freundin seines/ihres Sohnes getroffen (erstes Mal).
- Der Sohn des Benutzer/in hat seine Freundin zum Familienessen mitgebracht.
- Die Freundin hat eine schöne Flasche Wein mitgebracht.
""",
)),

Example(flow="file", example_input=Translations(
en="""
source: "Eukaryotes, Origin of". Encyclopedia of Biodiversity. Vol. 2.

# Topics
## Evolution of Eukaryotic Cells (early evolution from Prokaryotes)
## Eukaryotic Cells

Eukaryotic cells, the building blocks of complex life, are thought to have evolved from simpler prokaryotic cells through a process called endosymbiosis, where one prokaryotic cell engulfed another, leading to the development of membrane-bound organelles.
Eukaryotic cells have internal organization with a plasma membrane, cytoplasm containing organelles like mitochondria (energy), endoplasmic reticulum (synthesis), and a nucleus (genetic information) enclosed by a nuclear envelope.
""",
es="""
fuente: "Eucariotas, Origen de". Enciclopedia de la Biodiversidad. Vol. 2.

# Temas
## Evolución de las Células Eucariotas (evolución temprana a partir de Procariotas)
## Células Eucariotas

Las células eucariotas, los componentes básicos de la vida compleja, se cree que evolucionaron a partir de células procariotas más simples a través de un proceso llamado endosimbiosis, donde una célula procariota engulló a otra, lo que llevó al desarrollo de orgánulos unidos a membranas.
Las células eucariotas tienen organización interna con una membrana plasmática, citoplasma que contiene orgánulos como mitocondrias (energía), retículo endoplasmático (síntesis) y un núcleo (información genética) encerrado por una envoltura nuclear.
""",
fr="""
source : "Eucaryotes, Origine des". Encyclopédie de la Biodiversité. Vol. 2.

# Sujets
## Évolution des Cellules Eucaryotes (évolution précoce à partir des Procaryotes)
## Cellules Eucaryotes

Les cellules eucaryotes, les éléments constitutifs de la vie complexe, sont censées avoir évolué à partir de cellules procaryotes plus simples par un processus appelé endosymbiose, où une cellule procaryote en a englouti une autre, conduisant au développement d'organites liés à une membrane.
Les cellules eucaryotes ont une organisation interne avec une membrane plasmique, un cytoplasme contenant des organites comme les mitochondries (énergie), le réticulum endoplasmique (synthèse) et un noyau (information génétique) entouré d'une enveloppe nucléaire.
""",
de="""
Quelle: "Eukaryoten, Ursprung der". Enzyklopädie der Biodiversität. Bd. 2.

# Themen
## Evolution der Eukaryotischen Zellen (frühe Evolution aus Prokaryoten)
## Eukaryotische Zellen

Eukaryotische Zellen, die Bausteine komplexen Lebens, sollen sich aus einfacheren prokaryotischen Zellen durch einen Prozess namens Endosymbiose entwickelt haben, bei dem eine prokaryotische Zelle eine andere verschlang, was zur Entwicklung membrangebundener Organellen führte.
Eukaryotische Zellen haben eine innere Organisation mit einer Plasmamembran, Zytoplasma, das Organellen wie Mitochondrien (Energie), endoplasmatisches Retikulum (Synthese) und einen von einer Kernhülle umschlossenen Zellkern (genetische Information) enthält.
""",
), example_output=Translations(
en="""
## Evolution of Eukaryotic Cells (early evolution from Prokaryotes)
- Eukaryotic cells are thought to have evolved from simpler prokaryotic cells through a process called endosymbiosis.
- In endosymbiosis, one prokaryotic cell engulfed another.
- Endosymbiosis led to the development of membrane-bound organelles.
## Eukaryotic Cells
- Eukaryotic cells are the building blocks of complex life.
- Eukaryotic cells have internal organization with a plasma membrane and cytoplasm.
- Cytoplasm contains organelles like mitochondria (energy), endoplasmic reticulum (synthesis) and nucleus (genetic information).
- The nucleus is enclosed by a nuclear envelope.
""",
es="""
## Evolución de las Células Eucariotas (evolución temprana a partir de Procariotas)
- Se cree que las células eucariotas evolucionaron a partir de células procariotas más simples a través de un proceso llamado endosimbiosis.
- En la endosimbiosis, una célula procariota engulló a otra.
- La endosimbiosis condujo al desarrollo de orgánulos unidos a membranas.
## Células Eucariotas
- Las células eucariotas son los componentes básicos de la vida compleja.
- Las células eucariotas tienen organización interna con una membrana plasmática y citoplasma.
- El citoplasma contiene orgánulos como mitocondrias (energía), retículo endoplasmático (síntesis) y núcleo (información genética).
- El núcleo está rodeado por una envoltura nuclear.
""",
fr="""
## Évolution des Cellules Eucaryotes (évolution précoce à partir des Procaryotes)
- On pense que les cellules eucaryotes ont évolué à partir de cellules procaryotes plus simples par un processus appelé endosymbiose.
- Dans l'endosymbiose, une cellule procaryote en a englouti une autre.
- L'endosymbiose a conduit au développement d'organites liés à des membranes.
## Cellules Eucaryotes
- Les cellules eucaryotes sont les éléments constitutifs de la vie complexe.
- Les cellules eucaryotes ont une organisation interne avec une membrane plasmique et un cytoplasme.
- Le cytoplasme contient des organites comme les mitochondries (énergie), le réticulum endoplasmique (synthèse) et le noyau (information génétique).
- Le noyau est entouré d'une enveloppe nucléaire.
""",
de="""
## Evolution der Eukaryotischen Zellen (frühe Evolution aus Prokaryoten)
- Es wird angenommen, dass sich eukaryotische Zellen aus einfacheren prokaryotischen Zellen durch einen Prozess namens Endosymbiose entwickelt haben.
- Bei der Endosymbiose verschlang eine prokaryotische Zelle eine andere.
- Die Endosymbiose führte zur Entwicklung von membranumschlossenen Organellen.
## Eukaryotische Zellen
- Eukaryotische Zellen sind die Bausteine komplexen Lebens.
- Eukaryotische Zellen haben eine innere Organisation mit einer Plasmamembran und Zytoplasma.
- Das Zytoplasma enthält Organellen wie Mitochondrien (Energie), Endoplasmatisches Retikulum (Synthese) und den Zellkern (genetische Information).
- Der Zellkern ist von einer Kernhülle umschlossen.
""",
)),
])

FACT_ENTITIES = Prompt(prompt_type="system", prompt=Translations(

en="""
Task: Extract facts and their corresponding entities.

Instructions:
- Strictly use the INPUT facts as headings, do not change them, do not add new ones
- For each fact, extract every entity (i.e. subjects, objects, events, concepts, etc.)
- Entities must be written with format: `name (type)`
- Entities may repeat across facts
- Use names instead of pronouns
- No explanations, just output in markdown format:
## [fact]
- name (type)
- name (type)
""",

es="""
Tarea: Extraer hechos y sus entidades correspondientes.

Instrucciones:
- Usar estrictamente los hechos del INPUT como encabezados, no cambiarlos, no añadir nuevos
- Para cada hecho, extraer cada entidad (es decir, sujetos, objetos, eventos, conceptos, etc.)
- Las entidades deben escribirse con el formato: `nombre (tipo)`
- Las entidades pueden repetirse entre hechos
- Usar nombres en lugar de pronombres
- Nada de explicaciones, solo escribe en formato markdown:
## [hecho]
- nombre (tipo)
- nombre (tipo)
""",

fr="""
Tâche: Extraire les faits et leurs entités correspondantes.

Instructions:
- Utiliser strictement les faits de l'INPUT comme titres, ne pas les modifier, ne pas en ajouter de nouveaux
- Pour chaque fait, extraire chaque entité (c'est-à-dire sujets, objets, événements, concepts, etc.)
- Les entités doivent être écrites au format: `nom (type)`
- Les entités peuvent se répéter entre les faits
- Utiliser des noms au lieu de pronoms
- Pas d'explications, juste la sortie au format markdown :
## [fait]
- nom (type)
- nom (type)
""",

de="""
Aufgabe: Fakten und ihre entsprechenden Entitäten extrahieren.

Anweisungen:
- Verwenden Sie strikt die INPUT-Fakten als Überschriften, ändern Sie sie nicht, fügen Sie keine neuen hinzu
- Extrahieren Sie für jeden Fakt jede Entität (d.h. Subjekte, Objekte, Ereignisse, Konzepte usw.)
- Entitäten müssen im Format geschrieben werden: `Name (Typ)`
- Entitäten können sich über Fakten hinweg wiederholen
- Verwenden Sie Namen anstelle von Pronomen
- Keine Erklärungen, nur die Ausgabe im Markdown-Format:
## [Fakt]
- Name (Typ)
- Name (Typ)
""",

), examples=[

Example(flow="chat", example_input=Translations(
en="""
current timestamp: 2023-02-12 13:30

# Facts
## User had dinner with the family last night.
## The husband of user cooked lasagna.
## Lasagna is the favorite dish of the daughter of user.
## The son of user brought his girlfriend.
## The family of user was meeting the girlfriend of the son of user for the first time.

Optional entities:
- User (current user)
- Husband (spouse of user)
- Bob (neighbor of user)
""",
es="""
tiempo actual: 2023-02-12 13:30

# Hechos
## El usuario/a cenó con la familia anoche.
## El marido del usuario/a cocinó lasaña.
## La lasaña es el plato favorito de la hija del usuario/a.
## El hijo del usuario/a trajo a su novia.
## La familia del usuario/a conoció a la novia del hijo del usuario/a por primera vez.

Entidades opcionales:
- Usuario/a (usuario/a actual)
- Marido (cónyuge del usuario/a)
- Bob (vecino del usuario/a)
""",
fr="""
horodatage actuel : 2023-02-12 13:30

# Faits
## L'utilisateur/trice a dîné avec la famille hier soir.
## Le mari de l'utilisateur/trice a cuisiné des lasagnes.
## Les lasagnes sont le plat préféré de la fille de l'utilisateur/trice.
## Le fils de l'utilisateur/trice a amené sa petite amie.
## La famille de l'utilisateur/trice rencontrait la petite amie du fils de l'utilisateur/trice pour la première fois.

Entités optionnelles :
- Utilisateur/trice (utilisateur/trice actuel/le)
- Mari (conjoint de l'utilisateur/trice)
- Bob (voisin de l'utilisateur/trice)
""",
de="""
aktueller Zeitstempel: 2023-02-12 13:30

# Fakten
## Der Benutzer/in hat gestern Abend mit der Familie zu Abend gegessen.
## Der Ehemann des Benutzers/in hat Lasagne gekocht.
## Lasagne ist das Lieblingsgericht der Tochter des Benutzers.
## Der Sohn des Benutzers/in hat seine Freundin mitgebracht.
## Die Familie des Benutzers/in hat die Freundin des Sohnes des Benutzers/in zum ersten Mal getroffen.

Optionale Entitäten:
- Benutzer/in (aktueller Benutzer/in)
- Ehemann (Ehepartner des Benutzers)
- Bob (Nachbar des Benutzers)
""",
), example_output=Translations(
en="""
## User had dinner with the family last night.
- User (current user)
- Family (relatives of user)
- Dinner (event last night from 2023-02-12 13:30)

## The husband of user cooked lasagna.
- Husband (spouse of user)
- Lasagna (Italian pasta dish)

## Lasagna is the favorite dish of the daughter of user.
- Lasagna (Italian pasta dish)
- Daughter (female child of user)

## The son of user brought his girlfriend.
- Son (male child of user)
- Girlfriend (romantic partner of son of user)

## The family of user was meeting the girlfriend of the son of user for the first time.
- Family (relatives of user)
- Girlfriend (romantic partner of son of user)
""",
es="""
## El usuario/a cenó con la familia anoche.
- Usuario/a (usuario/a actual)
- Familia (parientes del usuario/a)
- Cena (evento de anoche del 12-02-2023 13:30)

## El marido del usuario/a cocinó lasaña.
- Marido (cónyuge del usuario/a)
- Lasaña (plato de pasta italiano)

## La lasaña es el plato favorito de la hija del usuario/a.
- Lasaña (plato de pasta italiano)
- Hija (hija del usuario/a)

## El hijo del usuario/a trajo a su novia.
- Hijo (hijo del usuario/a)
- Novia (pareja sentimental del hijo del usuario/a)

## La familia del usuario/a conoció a la novia del hijo del usuario/a por primera vez.
- Familia (parientes del usuario/a)
- Novia (pareja sentimental del hijo del usuario/a)
""",
fr="""
## L'utilisateur/trice a dîné avec la famille hier soir.
- Utilisateur/trice (utilisateur/trice actuel/le)
- Famille (proches de l'utilisateur/trice)
- Dîner (événement d'hier soir du 12-02-2023 13:30)

## Le mari de l'utilisateur/trice a cuisiné des lasagnes.
- Mari (conjoint de l'utilisateur/trice)
- Lasagnes (plat de pâtes italien)

## Les lasagnes sont le plat préféré de la fille de l'utilisateur/trice.
- Lasagnes (plat de pâtes italien)
- Fille (enfant de sexe féminin de l'utilisateur/trice)

## Le fils de l'utilisateur/trice a amené sa petite amie.
- Fils (enfant de sexe masculin de l'utilisateur/trice)
- Petite amie (partenaire romantique du fils de l'utilisateur/trice)

## La famille de l'utilisateur/trice rencontrait la petite amie du fils de l'utilisateur/trice pour la première fois.
- Famille (proches de l'utilisateur/trice)
- Petite amie (partenaire romantique du fils de l'utilisateur/trice)
""",
de="""
## Der Benutzer/in hat gestern Abend mit der Familie zu Abend gegessen.
- Benutzer/in (aktueller Benutzer/in)
- Familie (Verwandte des/der Nutzers/in)
- Abendessen (Ereignis von gestern Abend vom 12.02.2023 13:30)

## Der Ehemann des Benutzers/in hat Lasagne gekocht.
- Ehemann (Ehepartner des/der Nutzers/in)
- Lasagne (italienisches Nudelgericht)

## Lasagne ist das Lieblingsgericht der Tochter des Benutzers.
- Lasagne (italienisches Nudelgericht)
- Tochter (weibliches Kind des/der Nutzers/in)

## Der Sohn des Benutzers/in hat seine Freundin mitgebracht.
- Sohn (männliches Kind des/der Nutzers/in)
- Freundin (romantische Partnerin des Sohnes des/der Nutzers/in)

## Die Familie des Benutzers/in hat die Freundin des Sohnes des Benutzers/in zum ersten Mal getroffen.
- Familie (Verwandte des/der Nutzers/in)
- Freundin (romantische Partnerin des Sohnes des/der Nutzers/in)
""",
)),

Example(flow="file", example_input=Translations(
en="""
source: "Eukaryotes, Origin of". Encyclopedia of Biodiversity. Vol. 2.

# Facts
## Eukaryotic cells are the building blocks of complex life.
## Eukaryotic cells have internal organization with a plasma membrane and cytoplasm.
## Cytoplasm contains organelles like mitochondria (energy), endoplasmic reticulum (synthesis) and nucleus (genetic information).
## The nucleus is enclosed by a nuclear envelope.

Optional entities:
- Prokariote (cell without membrane-bound nucleus)
- Plasma membrane (outer layer of cell)
- Cytoplasm (internal cell fluid)
- Genetic material (DNA)
""",
es="""
fuente: "Eucariotas, Origen de". Enciclopedia de la Biodiversidad. Vol. 2.

# Hechos
## Las células eucariotas son los componentes básicos de la vida compleja.
## Las células eucariotas tienen organización interna con una membrana plasmática y citoplasma.
## El citoplasma contiene orgánulos como mitocondrias (energía), retículo endoplasmático (síntesis) y núcleo (información genética).
## El núcleo está rodeado por una envoltura nuclear.

Entidades opcionales:
- Procariota (célula sin núcleo delimitado por membrana)
- Membrana plasmática (capa externa de la célula)
- Citoplasma (fluido interno de la célula)
- Material genético (ADN)
""",
fr="""
source : "Eucaryotes, Origine des". Encyclopédie de la Biodiversité. Vol. 2.

# Faits
## Les cellules eucaryotes sont les éléments constitutifs de la vie complexe.
## Les cellules eucaryotes ont une organisation interne avec une membrane plasmique et un cytoplasme.
## Le cytoplasme contient des organites comme les mitochondries (énergie), le réticulum endoplasmique (synthèse) et le noyau (information génétique).
## Le noyau est entouré d'une enveloppe nucléaire.

Entités optionnelles :
- Procaryote (cellule sans noyau délimité par une membrane)
- Membrane plasmique (couche externe de la cellule)
- Cytoplasme (fluide interne de la cellule)
- Matériel génétique (ADN)
""",
de="""
Quelle: "Eukaryoten, Ursprung der". Enzyklopädie der Biodiversität. Bd. 2.

# Fakten
## Eukaryotische Zellen sind die Bausteine komplexen Lebens.
## Eukaryotische Zellen haben eine innere Organisation mit einer Plasmamembran und Zytoplasma.
## Das Zytoplasma enthält Organellen wie Mitochondrien (Energie), endoplasmatisches Retikulum (Synthese) und Zellkern (genetische Information).
## Der Zellkern ist von einer Kernhülle umschlossen.

Optionale Entitäten:
- Prokaryot (Zelle ohne membranumschlossenen Zellkern)
- Plasmamembran (äußere Zellschicht)
- Zytoplasma (innere Zellflüssigkeit)
- Genetisches Material (DNA)
""",
), example_output=Translations(
en="""
## Eukaryotic cells are the building blocks of complex life.
- Eukaryotic cells (cell type)
- complex life (concept)

## Eukaryotic cells have internal organization with a plasma membrane and cytoplasm.
- Eukaryotic cells (cell type)
- internal organization (cellular feature)
- Plasma membrane (outer layer of cell)
- Cytoplasm (internal cell fluid)

## Cytoplasm contains organelles like mitochondria (energy), endoplasmic reticulum (synthesis) and nucleus (genetic information).
- Cytoplasm (internal cell fluid)
- organelles (cellular component)
- Mitochondria (energy-producing organelle)
- Endoplasmic reticulum (synthesis organelle)
- Nucleus (genetic information center)

## The nucleus is enclosed by a nuclear envelope.
- Nucleus (genetic information center)
- nuclear envelope (nucleus enclosure)
""",
es="""
## Las células eucariotas son los componentes básicos de la vida compleja.
- Células eucariotas (tipo de célula)
- vida compleja (concepto)

## Las células eucariotas tienen organización interna con una membrana plasmática y citoplasma.
- Células eucariotas (tipo de célula)
- organización interna (característica celular)
- Membrana plasmática (capa externa de la célula)
- Citoplasma (fluido celular interno)

## El citoplasma contiene orgánulos como mitocondrias (energía), retículo endoplasmático (síntesis) y núcleo (información genética).
- Citoplasma (fluido celular interno)
- orgánulos (componente celular)
- Mitocondrias (orgánulo productor de energía)
- Retículo endoplasmático (orgánulo de síntesis)
- Núcleo (centro de información genética)

## El núcleo está rodeado por una envoltura nuclear.
- Núcleo (centro de información genética)
- envoltura nuclear (recinto del núcleo)
""",
fr="""
## Les cellules eucaryotes sont les éléments constitutifs de la vie complexe.
- Cellules eucaryotes (type de cellule)
- vie complexe (concept)

## Les cellules eucaryotes ont une organisation interne avec une membrane plasmique et un cytoplasme.
- Cellules eucaryotes (type de cellule)
- organisation interne (caractéristique cellulaire)
- Membrane plasmique (couche externe de la cellule)
- Cytoplasme (fluide cellulaire interne)

## Le cytoplasme contient des organites comme les mitochondries (énergie), le réticulum endoplasmique (synthèse) et le noyau (information génétique).
- Cytoplasme (fluide cellulaire interne)
- organites (composant cellulaire)
- Mitochondries (organite producteur d'énergie)
- Réticulum endoplasmique (organite de synthèse)
- Noyau (centre d'information génétique)

## Le noyau est entouré d'une enveloppe nucléaire.
- Noyau (centre d'information génétique)
- enveloppe nucléaire (enceinte du noyau)
""",
de="""
## Eukaryotische Zellen sind die Bausteine komplexen Lebens.
- Eukaryotische Zellen (Zelltyp)
- komplexes Leben (Konzept)

## Eukaryotische Zellen haben eine innere Organisation mit einer Plasmamembran und Zytoplasma.
- Eukaryotische Zellen (Zelltyp)
- innere Organisation (zelluläres Merkmal)
- Plasmamembran (äußere Zellschicht)
- Zytoplasma (innere Zellflüssigkeit)

## Das Zytoplasma enthält Organellen wie Mitochondrien (Energie), endoplasmatisches Retikulum (Synthese) und Zellkern (genetische Information).
- Zytoplasma (innere Zellflüssigkeit)
- Organellen (zellulärer Bestandteil)
- Mitochondrien (energieproduzierende Organelle)
- Endoplasmatisches Retikulum (Synthese-Organelle)
- Zellkern (Zentrum genetischer Information)

## Der Zellkern ist von einer Kernhülle umschlossen.
- Zellkern (Zentrum genetischer Information)
- Kernhülle (Umschließung des Zellkerns)
""",
)),
])

ENTITY_DEFINITIONS = Prompt(prompt_type="system", prompt=Translations(

en="""
Task: Specify what the indefinite headings refer to.

Instructions:
- Select from the allowed headings only the ones that are indefinite (i.e. unclear, general, ambiguous)
- Select means select, do not modify the selected headings, do not add new ones
- For each selected heading, list one by one every entity the heading refers to
- Entities must be written with format: `name (type)`
- Entity format is one entity with a single set of parentheses
- Entities may repeat across headings
- If not applicable, list 'None'
- No explanations, just output in markdown format:
## [heading]
- name (type)
""",

es="""
Tarea: Especificar a qué se refieren los encabezados indefinidos.

Instrucciones:
- Seleccionar de los encabezados permitidos solo aquellos que sean indefinidos (es decir, poco claros, generales, ambiguos)
- Seleccionar significa seleccionar, no modificar los encabezados seleccionados, no añadir nuevos
- Para cada encabezado seleccionado, listar una por una cada entidad a la que se refiere el encabezado
- Las entidades deben escribirse con el formato: `nombre (tipo)`
- El formato para la entidad es una entidad y un solo par de paréntesis
- Las entidades pueden repetirse entre encabezados
- Si no aplica, listar 'Ninguno'
- Nada de explicaciones, solo escribe en formato markdown:
## [encabezado]
- nombre (tipo)
""",

fr="""
Tâche : Spécifier à quoi se réfèrent les titres indéfinis.

Instructions:
- Sélectionner parmi les titres autorisés uniquement ceux qui sont indéfinis (c'est-à-dire peu clairs, généraux, ambigus)
- Sélectionner signifie sélectionner, ne pas modifier les titres sélectionnés, ne pas en ajouter de nouveaux
- Pour chaque titre sélectionné, lister un par un chaque entité à laquelle le titre fait référence
- Les entités doivent être écrites au format : `nom (type)`
- Le format d'entité est une entité avec une seule paire de parenthèses
- Les entités peuvent se répéter entre les titres
- Si non applicable, lister 'Aucun'
- Pas d'explications, juste la sortie au format markdown :
## [titre]
- nom (type)
""",

de="""
Aufgabe: Geben Sie an, worauf sich die unbestimmten Überschriften beziehen.

Anweisungen:
- Wählen Sie aus den erlaubten Überschriften nur diejenigen aus, die unbestimmt sind (d. h. unklar, allgemein, mehrdeutig)
- Auswählen bedeutet auswählen, die ausgewählten Überschriften nicht ändern, keine neuen hinzufügen
- Listen Sie für jede ausgewählte Überschrift einzeln jede Entität auf, auf die sich die Überschrift bezieht
- Entitäten müssen im Format geschrieben werden: `Name (Typ)`
- Das Entitätsformat ist eine Entität mit einem einzigen Satz Klammern
- Entitäten können sich über Überschriften hinweg wiederholen
- Falls nicht zutreffend, listen Sie 'Keine' auf
- Keine Erklärungen, nur die Ausgabe im Markdown-Format:
## [Überschrift]
- Name (Typ)
""",
), examples=[

Example(flow="chat", example_input=Translations(
en="""
# Headings
## User (current user)
## Husband (spouse of user)
## Everyone (people at the dinner)

# The headings refer to entities in the following text
I had dinner with my family last night. My husband cooked lasagna, which is my daughter's favorite dish. Our son brought his girlfriend, who we were meeting for the first time. She brought a lovely bottle of wine that everyone liked.
""",
es="""
# Encabezados
## Usuario/a (usuario/a actual)
## Marido (cónyuge del usuario/a)
## Todos (personas en la cena)

# Los encabezados se refieren a entidades en el siguiente texto
Anoche cené con mi familia. Mi marido cocinó lasaña, que es el plato favorito de mi hija. Nuestro hijo trajo a su novia, a quien conocíamos por primera vez. Ella trajo una botella de vino encantadora que a todos les gustó.
""",
fr="""
# Titres
## Utilisateur/trice (utilisateur/trice actuel/le)
## Mari (conjoint de l'utilisateur/trice)
## Tout le monde (personnes présentes au dîner)

# Les titres font référence aux entités dans le texte suivant
J'ai dîné avec ma famille hier soir. Mon mari a cuisiné des lasagnes, qui est le plat préféré de ma fille. Notre fils a amené sa petite amie, que nous rencontrions pour la première fois. Elle a apporté une jolie bouteille de vin que tout le monde a aimée.
""",
de="""
# Überschriften
## Benutzer/in (aktueller Benutzer/in)
## Ehemann (Ehepartner des Benutzers/in)
## Alle (Personen beim Abendessen)

# Die Überschriften beziehen sich auf Entitäten im folgenden Text
Ich habe gestern Abend mit meiner Familie zu Abend gegessen. Mein Mann hat Lasagne gekocht, das ist das Lieblingsgericht meiner Tochter. Unser Sohn hat seine Freundin mitgebracht, die wir zum ersten Mal trafen. Sie hat eine schöne Flasche Wein mitgebracht, die allen gefiel.
""",
), example_output=Translations(
en="""
## Everyone (people at the dinner)
- User (current user)
- Husband (spouse of user)
- Daughter (child of user)
- Son (child of user)
- Girlfriend (girlfriend of user's son)
""",
es="""
## Todos (personas en la cena)
- Usuario/a (usuario/a actual)
- Esposo (cónyuge del usuario/a)
- Hija (hija del usuario/a)
- Hijo (hijo del usuario/a)
- Novia (novia del hijo del usuario/a)
""",
fr="""
## Tout le monde (personnes au dîner)
- Utilisateur/trice (utilisateur/trice actuel/le)
- Mari (conjoint/e de l'utilisateur/trice)
- Fille (enfant de l'utilisateur/trice)
- Fils (enfant de l'utilisateur/trice)
- Petite amie (petite amie du fils de l'utilisateur/trice)
""",
de="""
## Alle (Personen beim Abendessen)
- Benutzer/in (aktueller Benutzer/in)
- Ehemann (Ehepartner/in des Benutzers/in)
- Tochter (Kind des Benutzers/in)
- Sohn (Kind des Benutzers/in)
- Freundin (Freundin des Sohnes des Benutzers/in)
""",
)),

Example(flow="file", example_input=Translations(
en="""
# Headings
## Cytoplasm (internal cell fluid)
## All of them (organelles)
## Mitochondria (energy-producing organelle)

# The headings refer to entities in the following text
Eukaryotic cells have organelles like mitochondria (energy), endoplasmic reticulum (synthesis), and a nucleus (genetic information) enclosed by a nuclear envelope, all of which are contained in the cytoplasm.
""",
es="""
# Encabezados
## Citoplasma (fluido celular interno)
## Todos ellos (orgánulos)
## Mitocondrias (orgánulo productor de energía)

# Los encabezados se refieren a entidades en el siguiente texto
Las células eucariotas tienen orgánulos como las mitocondrias (energía), el retículo endoplasmático (síntesis) y un núcleo (información genética) encerrado por una envoltura nuclear, todos los cuales están contenidos en el citoplasma.
""",
fr="""
# Titres
## Cytoplasme (fluide cellulaire interne)
## Tous (organites)
## Mitochondries (organite producteur d'énergie)

# Les titres font référence à des entités dans le texte suivant
Les cellules eucaryotes possèdent des organites comme les mitochondries (énergie), le réticulum endoplasmique (synthèse) et un noyau (information génétique) entouré d'une enveloppe nucléaire, tous contenus dans le cytoplasme.
""",
de="""
# Überschriften
## Zytoplasma (innere Zellflüssigkeit)
## Alle (Organellen)
## Mitochondrien (energieproduzierendes Organell)

# Die Überschriften beziehen sich auf Entitäten im folgenden Text
Eukaryotische Zellen besitzen Organellen wie Mitochondrien (Energie), endoplasmatisches Retikulum (Synthese) und einen Zellkern (genetische Information), der von einer Kernhülle umschlossen ist, die alle im Zytoplasma enthalten sind.
""",
), example_output=Translations(
en="""
## All of them (organelles)
- mitochondria (organelle for energy)
- endoplasmic reticulum (organelle for synthesis)
- nucleus (organelle for genetic information)
""",
es="""
## Todos ellos (orgánulos)
- mitocondria (orgánulo para la energía)
- retículo endoplasmático (orgánulo para la síntesis)
- núcleo (orgánulo para la información genética)
""",
fr="""
## Tous (organites)
- mitochondrie (organite pour l'énergie)
- réticulum endoplasmique (organite pour la synthèse)
- noyau (organite pour l'information génétique)
""",
de="""
## Alle (Organellen)
- Mitochondrium (Organell für Energie)
- Endoplasmatisches Retikulum (Organell für Synthese)
- Zellkern (Organell für genetische Information)
""",

)),
])

QUERY_NODES = Prompt(prompt_type="system", prompt=Translations(

en="""
Task: Create Topics, Facts and Entities

Instructions:
- Derive topics from the INPUT and list them under '# Topics'
- Extract concise facts, if the INPUT is a question create concise potential answers, use format `## [fact or potential answer]`
- For each `## [fact or potential answer]`, list each entity (i.e. subjects, objects, events, concepts, etc.) with format `name (type)`
- Use 'None' if there are no items to list
- Use names instead of pronouns
- No explanations, just output in markdown format:
# Topics
- [topic]
- [topic]

## [fact or potential answer]
- name (type)
- name (type)
""",

es="""
Tarea: Crear Temas, Hechos y Entidades

Instrucciones:
- Derivar temas del INPUT y listarlos bajo '# Temas'
- Extraer hechos concisos, si el INPUT es una pregunta crea respuestas potenciales concisas, usar el formato `## [hecho o respuesta potencial]`
- Para cada `## [hecho o respuesta potencial]`, listar cada entidad (es decir, sujetos, objetos, eventos, conceptos, etc.) con el formato `nombre (tipo)`
- Usar 'None' si no hay elementos para listar
- Usar nombres en lugar de pronombres
- Nada de explicaciones, solo escribe en formato markdown:
# Temas
- [tema]
- [tema]

## [hecho o respuesta potencial]
- nombre (tipo)
- nombre (tipo)
""",

fr="""
Tâche: Créer des Sujets, des Faits et des Entités

Instructions:
- Dériver les sujets de l'INPUT et les lister sous '# Sujets'
- Extraire des faits concis, si l'INPUT est une question créer des réponses potentielles concises, utiliser le format `## [fait ou réponse potentielle]`
- Pour chaque `## [fait ou réponse potentielle]`, lister chaque entité (c'est-à-dire sujets, objets, événements, concepts, etc.) avec le format `nom (type)`
- Utiliser 'Aucun' s'il n'y a pas d'éléments à lister
- Utiliser des noms au lieu de pronoms
- Pas d'explications, juste sortir au format markdown:
# Sujets
- [sujet]
- [sujet]

## [fait ou réponse potentielle]
- nom (type)
- nom (type)
""",

de="""
Aufgabe: Themen, Fakten und Entitäten erstellen

Anweisungen:
- Themen aus dem INPUT ableiten und sie unter '# Themen' auflisten
- Prägnante Fakten extrahieren, wenn der INPUT eine Frage ist, prägnante potenzielle Antworten erstellen, Format `## [Fakt oder potenzielle Antwort]` verwenden
- Für jede(n) `## [Fakt oder potenzielle Antwort]`, jede Entität (d.h. Subjekte, Objekte, Ereignisse, Konzepte, etc.) im Format `Name (Typ)` auflisten
- 'Keine' verwenden, wenn keine Elemente zum Auflisten vorhanden sind
- Namen anstelle von Pronomen verwenden
- Keine Erklärungen, nur im Markdown-Format ausgeben:
# Themen
- [Thema]
- [Thema]

## [Fakt oder potenzielle Antwort]
- Name (Typ)
- Name (Typ)
""",

), examples=[

Example(flow="chat", example_input=Translations(
en="""
I had dinner with my family last night, we met our son's girlfriend for the first time.
""",
es="""
Cené con mi familia anoche, conocimos a la novia de nuestro hijo por primera vez.
""",
fr="""
J'ai dîné avec ma famille hier soir, nous avons rencontré la petite amie de notre fils pour la première fois.
""",
de="""
Ich habe gestern Abend mit meiner Familie zu Abend gegessen, wir haben die Freundin unseres Sohnes zum ersten Mal getroffen.
""",
), example_output=Translations(
en="""
# Topics
- Family dinner
- Family relationships

## The user had dinner with the user's family
- User (person)
- Dinner (event last night)
- Family (user's relatives)

## The user met the user's son's girlfriend for the first time.
- User (person)
- son (user's son)
- girlfriend (son's girlfriend)
""",
es="""
# Temas
- Cena familiar
- Relaciones familiares

## El usuario/a cenó con la familia del usuario/a
- Usuario/a (persona)
- Cena (evento de anoche)
- Familia (parientes del usuario/a)

## El usuario/a conoció a la novia del hijo del usuario/a por primera vez.
- Usuario/a (persona)
- hijo (hijo del usuario/a)
- novia (novia del hijo)
""",
fr="""
# Sujets
- Dîner de famille
- Relations familiales

## L'utilisateur/trice a dîné avec sa famille
- Utilisateur/trice (personne)
- Dîner (événement d'hier soir)
- Famille (proches de l'utilisateur/trice)

## L'utilisateur/trice a rencontré la petite amie de son fils pour la première fois.
- Utilisateur/trice (personne)
- fils (fils de l'utilisateur/trice)
- petite amie (petite amie du fils)
""",
de="""
# Themen
- Familienessen
- Familienbeziehungen

## Der Benutzer/in hat mit seiner Familie zu Abend gegessen
- Benutzer/in (Person)
- Abendessen (Ereignis von gestern Abend)
- Familie (Verwandte des Benutzers/in)

## Der Benutzer/in hat die Freundin seines Sohnes zum ersten Mal getroffen.
- Benutzer/in (Person)
- Sohn (Sohn des Benutzers/in)
- Freundin (Freundin des Sohnes)
""",
)),

Example(flow="file", example_input=Translations(
en="""
What is the time complexity of a breadth-first search (BFS) algorithm on a graph with V vertices and E edges, and why?
""",
es="""
¿Cuál es la complejidad temporal de un algoritmo de búsqueda en anchura (BFS) en un grafo con V vértices y E aristas, y por qué?
""",
fr="""
Quelle est la complexité temporelle d'un algorithme de parcours en largeur (BFS) sur un graphe avec V sommets et E arêtes, et pourquoi ?
""",
de="""
Wie hoch ist die Zeitkomplexität eines Breitensuche-Algorithmus (BFS) auf einem Graphen mit V Knoten und E Kanten, und warum?
""",
), example_output=Translations(
en="""
# Topics
- Graph search algorithm
- Time complexity formula

## Time complexity is O(V + E)
- Breadth-first search (algorithm)
- O (time complexity)
- V (vertices)
- E (edges)

## Each vertex is enqueued and dequeued at most once
- vertex (node)
- queue (data structure)
""",
es="""
# Temas
- Algoritmo de búsqueda en grafos
- Fórmula de complejidad temporal

## La complejidad temporal es O(V + E)
- Búsqueda en anchura (algoritmo)
- O (complejidad temporal)
- V (vértices)
- E (aristas)

## Cada vértice se encola y desencola como máximo una vez
- vértice (nodo)
- cola (estructura de datos)
""",
fr="""
# Sujets
- Algorithme de recherche de graphe
- Formule de complexité temporelle

## La complexité temporelle est O(V + E)
- Recherche en largeur (algorithme)
- O (complexité temporelle)
- V (sommets)
- E (arêtes)

## Chaque sommet est enfilé et défilé au plus une fois
- sommet (nœud)
- file (structure de données)
""",
de="""
# Themen
- Graphsuchalgorithmus
- Zeitkomplexitätsformel

## Die Zeitkomplexität ist O(V + E)
- Breitensuche (Algorithmus)
- O (Zeitkomplexität)
- V (Knoten)
- E (Kanten)

## Jeder Scheitelpunkt wird höchstens einmal in die Warteschlange gestellt und daraus entfernt
- Scheitelpunkt (Knoten)
- Warteschlange (Datenstruktur)
""",
)),
])

RETRIEVAL_CHAT = Prompt(prompt_type="system", prompt=Translations(

en="""
You are a helpful assistant. Memories are your own recollections. Use only relevant memories to inform your responses.
""",

es="""
Eres un asistente útil. Los recuerdos son tus propias rememoraciones. Utiliza solo recuerdos relevantes para informar tus respuestas.
""",

fr="""
Vous êtes un assistant utile. Les souvenirs sont vos propres souvenirs. Utilisez uniquement les souvenirs pertinents pour éclairer vos réponses.
""",

de="""
Sie sind ein hilfreicher Assistent. Erinnerungen sind Ihre eigenen Erinnerungen. Verwenden Sie nur relevante Erinnerungen, um Ihre Antworten zu informieren.
""",

), examples=[])


RETRIEVAL_RAG = Prompt(prompt_type="user", prompt=Translations(

en="""
Task: Respond to the user query using the provided sources.

Instructions:
- Use only relevant sources to inform your responses
- Incorporate inline citations in brackets: [id]
- Citation ids must correspond to the ids in the source tags `<source id=*>`
- If uncertain, concisely ask the user to rephrase the question to see if you can get better sources
""",

es="""
Tarea: Responder a la consulta del usuario utilizando las fuentes proporcionadas.

Instrucciones:
- Utiliza solo fuentes relevantes para informar tus respuestas
- Incorpora citas en línea entre corchetes: [id]
- Los ids de las citas deben corresponder a los ids en las etiquetas de fuente `<source id=*>`
- Si no estás seguro, pide concisamente al usuario que reformule la pregunta para ver si puedes obtener mejores fuentes
""",

fr="""
Tâche : Répondre à la requête de l'utilisateur en utilisant les sources fournies.

Instructions :
- Utilisez uniquement les sources pertinentes pour éclairer vos réponses
- Intégrez des citations en ligne entre crochets : [id]
- Les identifiants de citation doivent correspondre aux identifiants dans les balises source `<source id=*>`
- En cas d'incertitude, demandez de manière concise à l'utilisateur de reformuler la question pour voir si vous pouvez obtenir de meilleures sources
""",

de="""
Aufgabe: Beantworten Sie die Benutzeranfrage anhand der bereitgestellten Quellen.

Anweisungen:
- Verwenden Sie nur relevante Quellen, um Ihre Antworten zu gestalten
- Fügen Sie Inline-Zitate in Klammern ein: [id]
- Die Zitat-IDs müssen mit den IDs in den Quell-Tags `<source id=*>` übereinstimmen
- Wenn Sie unsicher sind, bitten Sie den Benutzer prägnant, die Frage neu zu formulieren, um zu sehen, ob Sie bessere Quellen erhalten können
""",

), examples=[

Example(flow="file", example_input=Translations(
en="""
<query>
What were the findings of the study on kv cache?
</query>

<source id="1">
Instead of predicting one token at a time, DeepSeek employs MTP, allowing the model to predict multiple future tokens in a single step.
6</source>
<source id="2">
Red Hat's blog post on integrating DeepSeek models with vLLM 0.7.1 highlights that MLA offers up to 9.6x more memory capacity for key-value (KV) caches.
11</source>
""",
es="""
<query>
¿Cuáles fueron los hallazgos del estudio sobre la caché KV?
</query>

<source id="1">
En lugar de predecir un token a la vez, DeepSeek emplea MTP, lo que permite al modelo predecir múltiples tokens futuros en un solo paso.
6</source>
<source id="2">
La publicación del blog de Red Hat sobre la integración de los modelos DeepSeek con vLLM 0.7.1 destaca que MLA ofrece hasta 9,6 veces más capacidad de memoria para las cachés de clave-valor (KV).
11</source>
""",
fr="""
<query>
Quelles ont été les conclusions de l'étude sur le cache KV ?
</query>

<source id="1">
Au lieu de prédire un token à la fois, DeepSeek utilise MTP, permettant au modèle de prédire plusieurs tokens futurs en une seule étape.
6</source>
<source id="2">
L'article de blog de Red Hat sur l'intégration des modèles DeepSeek avec vLLM 0.7.1 souligne que MLA offre jusqu'à 9,6 fois plus de capacité mémoire pour les caches clé-valeur (KV).
11</source>
""",
de="""
<query>
Was waren die Ergebnisse der Studie zum KV-Cache?
</query>

<source id="1">
Anstatt ein Token nach dem anderen vorherzusagen, verwendet DeepSeek MTP, wodurch das Modell mehrere zukünftige Tokens in einem einzigen Schritt vorhersagen kann.
6</source>
<source id="2">
Der Blogbeitrag von Red Hat zur Integration von DeepSeek-Modellen mit vLLM 0.7.1 hebt hervor, dass MLA bis zu 9,6x mehr Speicherkapazität für Key-Value (KV)-Caches bietet.
11</source>
""",
), example_output=Translations(
en="""
According to Red Hat's blog post on integrating DeepSeek models, MLA offers up to 9.6x more memory capacity for key-value caches [2].
""",
es="""
Según la publicación del blog de Red Hat sobre la integración de modelos DeepSeek, MLA ofrece hasta 9,6 veces más capacidad de memoria para cachés de clave-valor [2].
""",
fr="""
Selon l'article de blog de Red Hat sur l'intégration des modèles DeepSeek, MLA offre jusqu'à 9,6 fois plus de capacité mémoire pour les caches clé-valeur [2].
""",
de="""
Laut dem Blogbeitrag von Red Hat zur Integration von DeepSeek-Modellen bietet MLA bis zu 9,6-mal mehr Speicherkapazität für Schlüssel-Wert-Caches [2].
""",
)),
])


### FORMAT ###

FORMAT = Prompt(prompt_type="system", prompt=Translations(

en="""
""",

es="""
""",

fr="""
""",

de="""
""",

), examples=[

Example(flow="chat", example_input=Translations(
en="""
""",
es="""
""",
fr="""
""",
de="""
""",
), example_output=Translations(
en="""
""",
es="""
""",
fr="""
""",
de="""
""",
)),

Example(flow="file", example_input=Translations(
en="""
""",
es="""
""",
fr="""
""",
de="""
""",
), example_output=Translations(
en="""
""",
es="""
""",
fr="""
""",
de="""
""",
)),
])

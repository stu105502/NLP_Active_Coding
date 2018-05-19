<h2> Einführung</h2>
Dieses kurze Projekt hat die Aufgabe, dass Job-Inserate von <a href="https://www.jopago.com/">Jopago</a> 1) angefragt werden 2) gescrapt werden und 3) mithilfe ihrer Anzahl von Verben und nach Hilfsverben durchsucht werden.

Diese Projekt wurde auf Basis von Python 2.7.12 geschrieben und verwendet die Bibilotheken, welche in requirements.txt aufgelistet sind. Alternativ können diese Packages auch mit `pip install -r requirements.txt` installiert werden.

Wir haben zwei verschiedene Python Klassen definiert:
<ol>
	<li>
		eine Entry-Klasse, die ein Jobinserat repräsentiert. Diese Klassen abstrahieren die Schritte, welche wir benötigen, um von URL-Adressen zu aktuellen Auswertungen zu gelangen.
	</li>
	<li>
		eine Listen-Klasse, welche die Aufgaben an ihre Entries deligiert. Diese Klasse kann somit bequem aus unseren Enties eine csv-Datei generieren oder eignet sich auch die URL-Adressen abzufragen (siehe Das Anfragen der HTML-Daten) und für diese Adressen Entries zu generieren. 
		</li>
</ol>
Kurz gesagt kann man andeuten, dass in unseren Entries alle Informationen zur HTML-Verareitung stecken und unsere Liste nur einen bequemen Wrapper darstellt.
<br/>

<h2>1) Das Anfragen der HTML-Daten:</h2>
Für das Anfagen der HTML-Seiten verwenden wir die Bibilothek <a href="http://docs.python-requests.org/en/master/"> Requests</a> und das Python Modul <a href="https://docs.python.org/3/library/re.html">re</a>. Requests ermöglicht es uns HTML-Code auf der Basis von URL-Adressen zu erhalten, während re uns das Nutzen regulärer Ausdrücke ermöglicht. Um die URL-Adressen von möglichst vielen Inseraten zu erhalten, fragen wir die Seiten nach dem Muster von <a href="https://www.jopago.com/jobs/search?page=1&pg=1">https://www.jopago.com/jobs/search?page=1&pg=1</a> an. Falls wir auf dieser Seite keine weiteren Inserate finden, ändern wir den page parameter in der URL zu page=2 usw. 

Um aus dem erhaltenen HTML-Code die URL für Jobinserate zu erhalten nutzen wir reguläre Ausdrücke. Uns interessieren URL, die
<ol>
	<li>die das href-Attribute eines Tags repräsentieren</li>
	<li>die mit <i>/jobs/</i> beginnen, aber nicht mit <i>/jobs/search</i>. So sind wir in der Lage zu differenzieren, welche Links und zu aktuellen Inseraten führen und welche dazu dienen weitere Jobangebote zu erhalten</li>
</ol>
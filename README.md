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

<h2>2) Das Scrappen der HTML-Daten</h2>
Nachdem wir unsere URL-Adressen gefunden und angefragt haben, möchten wir nun aus dem HTML-Code, den für uns interessante Code heraus extrahieren. 
Für diesen Prozess nutzen wir das Python-Modul 
<a href="http://lxml.de/">lxml</a>. Ein Modul, welches es bequem erleichtert XML- oder HTML-Daten zu verarbeiten.

 ```
 from lxml import html
 tree = html.fromstring(html)
 text = tree.xpath('//div[@class="job-body"]//text()')
 ```

 Der Oben gezeigte Text würde grundsätzlich ausreichen, um den gesamten, reinen Text, der in dem div-Tag mit der Klasse <i>joby-body</i> und seinen Child-Nodes enthalten ist, zu extrahieren. Dieser Prozess hat allerdings den Nachteil, dass wir Informationen über die Struktur des Inhalts komplett verlieren. Wir können uns auch nicht simpel auf die Punktsetzung verlassen, um Sätze zu differenzieren. Eine Liste ist zum Beispiel von der Form:

 ```
<p><strong>Was wir Ihnen bieten:</strong></p>
<ul>
	<li>Warenein- und Ausgangsbuchungen</li>
	<li>Be- und Entladen mittels Gabelstapler</li>
	<li>Pflege des Warenwirtschaftsystems</li>
	<li>Lager- und Logistiktätigkeiten</li>
</ul>
 ```

 Würden wir uns an den Punkten orientieren, wäre dies alles insgesamt ein einziger Satz. Solche Listen sind ein sehr beliebtes Mittel für Inserate und können nicht einfach vernachlässigt werden, da solche Listen teilweise 50% eines Inserates ausmachen und wir daran interessiert sind, die Aktivität eines Inserates an dem Verhältnis zwischen Verben und Worten jedes Satzes auszumachen. Wir haben uns entschieden hinter jeden Satz, der in einem li-Element aufgelistet ist, künstlich einen Punkt hinzuzufügen. Um solche Spezialfälle fachgerecht zu behandeln, haben wir uns beschlossen rekursiv durch den HTML-Baum zu gehen.

 Abschließend noch ein paar Punkte, welche uns das <i>Text-Scrapping</i> erschwert haben:
 <ul>
 	<li>Die Erfahrung der Nutzer in HTML war ein Problem. Manche Nutzer haben keine li-Element verwendet, um Listen zu kreieren, sonder haben einzelne Punkte simpel durh <i>-</i> angedeutet.</li>
 	<li>Generell die freie Schreibweise in solchen Inseraten war ein Problem. Als Beispiel haben Teilsätze wie <i>Ihr Kontakt: Frau Schubert</i></li> eine wichtige semantische Bedeutung, aber sind können grundsätzlich nicht als ein Satz eingeordnet werden.
 </ul>
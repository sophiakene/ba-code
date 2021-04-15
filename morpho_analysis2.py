import spacy
from spacy import displacy

with open("final_transcription.jsonl") as jsonl:
	sent = ""
	for obj in jsonl:
		obj = obj.strip()
		obj = obj.strip('{"text":")')
		obj = obj.strip('"}')
		sent += obj




nlp = spacy.load("de_core_news_sm")
doc = nlp(sent)


morpho = []
for t in doc:
	morpho.append(t.morph)
#print(morpho)

#html = displacy.render(doc)

html = '<div style="overflow:auto; height:500px"><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="de" id="06a216d0b81d4402987fb9fc3681fe58-0" class="displacy" width="3200" height="837.0" direction="ltr" style="overflow: visible; max-width: none; height: 837.0px; color: #000000; background: #ffffff; font-family: Arial; direction: ltr"><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="50">Chemie</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="50">NOUN</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="225">Michael</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="225">PROPN</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="400">Chodokowski</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="400">PROPN</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="575">war</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="575">AUX</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="750">Anfang</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="750">NOUN</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="925">der</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="925">DET</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1100">zwei</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1100">NUM</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1275">Tausend</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1275">NOUN</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1450">er</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1450">PRON</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1625">das</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1625">PRON</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1800">was</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1800">PRON</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1975">Alexander</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1975">PROPN</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2150">Walli</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2150">PROPN</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2325">heute</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2325">ADV</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2500">ist</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2500">AUX</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2675">Putins</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2675">PROPN</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2850">größter</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2850">ADJ</tspan></text><text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="3025">Gegner</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="3025">NOUN</tspan></text><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-0" stroke-width="2px" d="M70,702.0 C70,439.5 550.0,439.5 550.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-0" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">sb</textPath>    </text>    <path class="displacy-arrowhead" d="M70,704.0 L62,692.0 78,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-1" stroke-width="2px" d="M245,702.0 C245,614.5 365.0,614.5 365.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible;font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-1" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pnc</textPath>    </text>    <path class="displacy-arrowhead" d="M245,704.0 L237,692.0 253,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-2" stroke-width="2px" d="M70,702.0 C70,527.0 370.0,527.0 370.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible;font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-2" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M370.0,704.0 L378.0,692.0 362.0,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-3" stroke-width="2px" d="M595,702.0 C595,614.5 715.0,614.5 715.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-3" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">mo</textPath>    </text>    <path class="displacy-arrowhead" d="M715.0,704.0 L723.0,692.0 707.0,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-4" stroke-width="2px" d="M945,702.0 C945,527.0 1245.0,527.0 1245.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-4" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M945,704.0 L937,692.0 953,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-5" stroke-width="2px" d="M1120,702.0 C1120,614.5 1240.0,614.5 1240.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-5" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M1120,704.0 L1112,692.0 1128,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-6" stroke-width="2px" d="M770,702.0 C770,439.5 1250.0,439.5 1250.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-6" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">ag</textPath>    </text>    <path class="displacy-arrowhead" d="M1250.0,704.0 L1258.0,692.0 1242.0,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-7" stroke-width="2px" d="M595,702.0 C595,352.0 1430.0,352.0 1430.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-7" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">sb</textPath>    </text>    <path class="displacy-arrowhead" d="M1430.0,704.0 L1438.0,692.0 1422.0,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-8" stroke-width="2px" d="M595,702.0 C595,264.5 1610.0,264.5 1610.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-8" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pd</textPath>    </text>    <path class="displacy-arrowhead" d="M1610.0,704.0 L1618.0,692.0 1602.0,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-9" stroke-width="2px" d="M595,702.0 C595,177.0 1790.0,177.0 1790.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-9" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pd</textPath>    </text>    <path class="displacy-arrowhead" d="M1790.0,704.0 L1798.0,692.0 1782.0,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-10" stroke-width="2px" d="M1995,702.0 C1995,614.5 2115.0,614.5 2115.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-10" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pnc</textPath>    </text>    <path class="displacy-arrowhead" d="M1995,704.0 L1987,692.0 2003,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-11" stroke-width="2px" d="M1820,702.0 C1820,527.0 2120.0,527.0 2120.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-11" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M2120.0,704.0 L2128.0,692.0 2112.0,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-12" stroke-width="2px" d="M595,702.0 C595,89.5 2320.0,89.5 2320.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-12" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">mo</textPath>    </text>    <path class="displacy-arrowhead" d="M2320.0,704.0 L2328.0,692.0 2312.0,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-13" stroke-width="2px" d="M595,702.0 C595,2.0 2500.0,2.0 2500.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-13" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">cj</textPath>    </text>    <path class="displacy-arrowhead" d="M2500.0,704.0 L2508.0,692.0 2492.0,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-14" stroke-width="2px" d="M2695,702.0 C2695,527.0 2995.0,527.0 2995.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-14" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">ag</textPath>    </text>    <path class="displacy-arrowhead" d="M2695,704.0 L2687,692.0 2703,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-15" stroke-width="2px" d="M2870,702.0 C2870,614.5 2990.0,614.5 2990.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-15" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M2870,704.0 L2862,692.0 2878,692.0" fill="currentColor"/></g><g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-16" stroke-width="2px" d="M2520,702.0 C2520,439.5 3000.0,439.5 3000.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-16" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pd</textPath>    </text>    <path class="displacy-arrowhead" d="M3000.0,704.0 L3008.0,692.0 2992.0,692.0" fill="currentColor"/></g></svg></div>'


from lxml import etree as ET


root = ET.fromstring(html)

i=0
for elem in root.findall(".//"):
	if elem.get('class'):
		if elem.attrib['class'] == "displacy-word":
		#if elem.attrib['class'] == "displacy-token"
			word = elem.text
			parent = elem.getparent()
			new = ET.SubElement(parent, 'tspan')
			#new = elem.append('tspan')
			new.text = str(morpho[i])
			i += 1

#ET.dump(root)

with open("doc.xml","wb") as doc:
    doc.write(ET.tostring(root, pretty_print=True))


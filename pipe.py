"""prerequisites:
- Google Chrome
- python packages selenium and webdriver
- IMS-Speech login: https://75474978-c3fa-43a5-aa6c-ee36f2515064.ma.bw-cloud-instance.org/ims-speech/u/register
- Popen
""" 

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import re
import requests
import getpass

import prodigy
from prodigy import set_hashes
from prodigy.components.db import connect
from prodigy.components.preprocess import add_tokens
from prodigy.components.loaders import Audio, JSONL

import subprocess

import spacy
from spacy import displacy

from collections import Counter
import math


#-----------------------------------------------------------------------------------------------------------------------------
# LANGUAGE SELECTION
"""
language = input("Enter 'de' for standard German or 'ch for Swiss German")

-> use respective pipeline
"""


#------------------------------------------------------------------------------------------------------------------------------
#ASR transcription

# go to IMS login page
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://75474978-c3fa-43a5-aa6c-ee36f2513064.ma.bw-cloud-instance.org/ims-speech/")

# login
mail = driver.find_element_by_id("email")
password = driver.find_element_by_id("password")

# enter mail and password
user_mail = input("Enter e-Mail address for IMS speech login: ")
user_pw = getpass.getpass(prompt="Enter password: ")

mail.send_keys(user_mail)
password.send_keys(user_pw, Keys.RETURN)

# go to upload page
driver.find_element_by_link_text("Upload recording").click()

time.sleep(3)
user_file = input("Enter absolute path to file to transcribe: ")
filename = user_file.split("/")[-1]
print("uploading",filename+".....")


# go to upload page
driver.find_element_by_link_text("Upload recording").click()
# upload audio file specified by user
driver.find_element_by_id("content").send_keys(user_file)

driver.find_element_by_xpath('//button[text()="Upload"]').click()

# go to Home site
driver.find_element_by_class_name("navbar-brand").click()
print("transcribing.....")
# check once a minute if transcriptionion is ready

# choose right transcriptionion
a_elements = driver.find_elements_by_tag_name("a")
for a in reversed(a_elements):
    if a.text.startswith(user_file.split('/')[-1]):
    #if a.text.startswith("n.mp3"): 
        a.click()
        break

"""#falls man auf der "successful upload" Seite landet - wann ist das??
a = driver.find_elements_by_tag_name("a")
for an in a:
    print(an.text)
driver.find_elements_by_tag_name("a")[1].click() #TODO TRY!!! statt a_elements bis break
"""

#check once a minute if transcriptionion is ready
while True:
    if driver.find_elements_by_tag_name("span")[1].get_attribute("class") == "badge badge-success": #transcriptionion is ready for download if the badge next to it has class success
        break
    time.sleep(60)
    driver.refresh()


# download transcription
print("downloading transcription.....")

#download .str
#(other formats possible (.ttml, .vtt, .otr))
download_url = re.sub("view", "export/srt", driver.current_url)
#login_page = "https://75474978-c3fa-43a5-aa6c-ee36f2513064.ma.bw-cloud-instance.org/ims-speech/"
login_page = "https://75474978-c3fa-43a5-aa6c-ee36f2513064.ma.bw-cloud-instance.org/ims-speech/u/login"

# create new file to write downloaded transcription into
download = 'downloaded_transcription.txt'

s = requests.Session()
# login to IMS again
s.post(login_page, data={"email": user_mail, "password": user_pw})

# download and save to downloaded_transcription.txt
response = s.get(download_url)

with open(download, 'wb') as transcription:
    transcription.write(response.content)

driver.quit()


#----------------------------------------------------------------------------------------------------------------
# MANUAL ADJUSTMENTS OF transcription IN PRODIGY

dataset = input("Enter new prodigy dataset name: ")

# write output from asr to jsonl
with open("downloaded_transcription.txt", encoding="utf-8") as asr_read:#, open("transcription.jsonl", "w+") as transcription_write: 
    text = ""
    for line in asr_read.readlines():
        if line[0].isalpha():
            text += line.strip()+"\n" 

    #print("here: ",text)
    #examples in JSONL format (read from transcription)
    jsonl = {'audio': filename, 'text': '', 'meta': {'file': filename}, 'path': filename, '_input_hash': -758377432, '_task_hash': -1593748291, '_session_id': None, '_view_id': 'blocks', 'audio_spans': [],"transcript": text, "answer": "accept"}
    #{'audio': 'n.mp3', 'text': 'nawalny', 'meta': {'file': 'n.mp3'}, 'path': 'n.mp3', '_input_hash': -758377432, '_task_hash': -1593748291, '_session_id': None, '_view_id': 'blocks', 'audio_spans': [],"transcription": "text", "answer": "accept"}


# save asr transcription to prodigy database
db = connect()
# hash the examples to make sure they all have a unique task hash and input hash – this is used by Prodigy to distinguish between annotations on the same input data
jsonl_annotations = [set_hashes(jsonl)] # jsonl_annotations = [set_hashes(ann) for ann in jsonl_annotations] #bei mehreren audios (?)

# create new dataset
db.add_dataset(dataset)
# add examples to the (existing!) dataset
db.add_examples(jsonl_annotations, datasets=[dataset]) 


reviewed_dataset = input("Enter NEW dataset name for reviewed transcription: ")
while reviewed_dataset in db:
    reviewed_dataset = input("Database name already taken. Enter NEW dataset name for reviewed transcription: ")
    if not reviewed_dataset in db:
        break



print("\nPress ctrl+c when done transcribing\n")
#open prodigy to transcribe manually/review automatic transcriptionion (--fetch-media loads in audio as well)
prodigy.serve("audio.transcribe {} dataset:{} --fetch-media".format(reviewed_dataset, dataset)) 

#input("Type 'ok' when having saved the corrected transcription: ")

reviewed_transcription = db.get_dataset(reviewed_dataset)

#print(reviewed_transcription) #

for dic in reviewed_transcription:
    final_transcription = dic["transcript"] #müsste egtl immer nur 1 sein in dem kontext
    #TypeError: list indices must be integers or slices, not str!!!! kein dictionary in der liste??? types printen....



#prepare for annotation: 1 sentence at a time
"""labels = []
while input() != "ok":
    labels.append(input("Enter label names separated by ENTER. Write 'ok' when done."))"""

"""with open("transcription_for_annotation.jsonl", "w+") as w:
    for sentence in manually_transcribed.readlines():
        w.write("{text: "+sentence+",label: , answer: accept") #???
prodigy.serve()
"""


nlp = spacy.load("de_core_news_sm")
final_transcription = re.sub("\n"," ",final_transcription)
doc = nlp(final_transcription)

with open("final_transcription.jsonl", "w") as f:
    for sent in doc.sents:
        f.write('{"text":"'+ str(sent)+'"}\n')

        




#----------------------------------------------------------------------------------------------------------------

#PARSING etc. WITH SPACY 

l = []

for sent in doc.sents:
    pos_tag = displacy.render(sent)
    pos_tag = re.sub('style="','style="overflow:visible; ', pos_tag)
    pos_tag = '<div style="overflow:auto; height:500px">' + pos_tag + '</div>'

    #hier morpho einfügen - vorerst auf server
    pos_tag = '<div style="overflow:auto; height:500px">\n  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="de" id="06a216d0b81d4402987fb9fc3681fe58-0" class="displacy" width="3200" height="837.0" direction="ltr" style="overflow: visible; max-width: none; height: 837.0px; color: #000000; background: #ffffff; font-family: Arial; direction: ltr">\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="50">Chemie</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="50">NOUN</tspan><tspan>Case=Nom|Gender=Fem|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="225">Michael</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="225">PROPN</tspan><tspan>Case=Nom|Gender=Masc|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="400">Chodokowski</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="400">PROPN</tspan><tspan>Case=Nom|Gender=Masc|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="575">war</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="575">AUX</tspan><tspan>Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="750">Anfang</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="750">NOUN</tspan><tspan>Gender=Masc|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="925">der</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="925">DET</tspan><tspan>Case=Gen|Definite=Def|Gender=Neut|Number=Plur|PronType=Art</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1100">zwei</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1100">NUM</tspan><tspan></tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1275">Tausend</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1275">NOUN</tspan><tspan>Case=Gen|Gender=Masc|Number=Plur</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1450">er</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1450">PRON</tspan><tspan>Case=Nom|Gender=Masc|Number=Sing|Person=3|PronType=Prs</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1625">das</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1625">PRON</tspan><tspan>Case=Acc|Gender=Neut|Number=Sing|PronType=Dem</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1800">was</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1800">PRON</tspan><tspan>Case=Acc|Gender=Neut|Number=Sing|PronType=Int</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1975">Alexander</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1975">PROPN</tspan><tspan>Case=Nom|Gender=Masc|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2150">Walli</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2150">PROPN</tspan><tspan>Case=Nom|Gender=Masc|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2325">heute</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2325">ADV</tspan><tspan></tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2500">ist</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2500">AUX</tspan><tspan>Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2675">Putins</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2675">PROPN</tspan><tspan>Case=Nom|Definite=Ind|Gender=Fem|Number=Sing|PronType=Art</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2850">gr&#246;&#223;ter</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2850">ADJ</tspan><tspan>Case=Dat|Degree=Pos|Gender=Fem|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="3025">Gegner</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="3025">NOUN</tspan><tspan>Case=Nom|Number=Sing</tspan></text>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-0" stroke-width="2px" d="M70,702.0 C70,439.5 550.0,439.5 550.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-0" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">sb</textPath>    </text>    <path class="displacy-arrowhead" d="M70,704.0 L62,692.0 78,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-1" stroke-width="2px" d="M245,702.0 C245,614.5 365.0,614.5 365.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible;font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-1" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pnc</textPath>    </text>    <path class="displacy-arrowhead" d="M245,704.0 L237,692.0 253,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-2" stroke-width="2px" d="M70,702.0 C70,527.0 370.0,527.0 370.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible;font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-2" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M370.0,704.0 L378.0,692.0 362.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-3" stroke-width="2px" d="M595,702.0 C595,614.5 715.0,614.5 715.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-3" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">mo</textPath>    </text>    <path class="displacy-arrowhead" d="M715.0,704.0 L723.0,692.0 707.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-4" stroke-width="2px" d="M945,702.0 C945,527.0 1245.0,527.0 1245.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-4" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M945,704.0 L937,692.0 953,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-5" stroke-width="2px" d="M1120,702.0 C1120,614.5 1240.0,614.5 1240.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-5" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M1120,704.0 L1112,692.0 1128,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-6" stroke-width="2px" d="M770,702.0 C770,439.5 1250.0,439.5 1250.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-6" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">ag</textPath>    </text>    <path class="displacy-arrowhead" d="M1250.0,704.0 L1258.0,692.0 1242.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-7" stroke-width="2px" d="M595,702.0 C595,352.0 1430.0,352.0 1430.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-7" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">sb</textPath>    </text>    <path class="displacy-arrowhead" d="M1430.0,704.0 L1438.0,692.0 1422.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-8" stroke-width="2px" d="M595,702.0 C595,264.5 1610.0,264.5 1610.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-8" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pd</textPath>    </text>    <path class="displacy-arrowhead" d="M1610.0,704.0 L1618.0,692.0 1602.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-9" stroke-width="2px" d="M595,702.0 C595,177.0 1790.0,177.0 1790.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-9" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pd</textPath>    </text>    <path class="displacy-arrowhead" d="M1790.0,704.0 L1798.0,692.0 1782.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-10" stroke-width="2px" d="M1995,702.0 C1995,614.5 2115.0,614.5 2115.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-10" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pnc</textPath>    </text>    <path class="displacy-arrowhead" d="M1995,704.0 L1987,692.0 2003,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-11" stroke-width="2px" d="M1820,702.0 C1820,527.0 2120.0,527.0 2120.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-11" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M2120.0,704.0 L2128.0,692.0 2112.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-12" stroke-width="2px" d="M595,702.0 C595,89.5 2320.0,89.5 2320.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-12" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">mo</textPath>    </text>    <path class="displacy-arrowhead" d="M2320.0,704.0 L2328.0,692.0 2312.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-13" stroke-width="2px" d="M595,702.0 C595,2.0 2500.0,2.0 2500.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-13" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">cj</textPath>    </text>    <path class="displacy-arrowhead" d="M2500.0,704.0 L2508.0,692.0 2492.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-14" stroke-width="2px" d="M2695,702.0 C2695,527.0 2995.0,527.0 2995.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-14" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">ag</textPath>    </text>    <path class="displacy-arrowhead" d="M2695,704.0 L2687,692.0 2703,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-15" stroke-width="2px" d="M2870,702.0 C2870,614.5 2990.0,614.5 2990.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-15" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M2870,704.0 L2862,692.0 2878,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-16" stroke-width="2px" d="M2520,702.0 C2520,439.5 3000.0,439.5 3000.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-16" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pd</textPath>    </text>    <path class="displacy-arrowhead" d="M3000.0,704.0 L3008.0,692.0 2992.0,692.0" fill="currentColor"/></g>\n  </svg>\n</div>\n'
    pos_tag = re.sub('\|', '\n', pos_tag)
    l.append(pos_tag)

"""
output von morpho_analysis:
<div style="overflow:auto; height:500px">\n  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="de" id="06a216d0b81d4402987fb9fc3681fe58-0" class="displacy" width="3200" height="837.0" direction="ltr" style="overflow: visible; max-width: none; height: 837.0px; color: #000000; background: #ffffff; font-family: Arial; direction: ltr">\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="50">Chemie</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="50">NOUN</tspan><tspan>Case=Nom|Gender=Fem|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="225">Michael</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="225">PROPN</tspan><tspan>Case=Nom|Gender=Masc|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="400">Chodokowski</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="400">PROPN</tspan><tspan>Case=Nom|Gender=Masc|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="575">war</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="575">AUX</tspan><tspan>Mood=Ind|Number=Sing|Person=3|Tense=Past|VerbForm=Fin</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="750">Anfang</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="750">NOUN</tspan><tspan>Gender=Masc|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="925">der</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="925">DET</tspan><tspan>Case=Gen|Definite=Def|Gender=Neut|Number=Plur|PronType=Art</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1100">zwei</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1100">NUM</tspan><tspan></tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1275">Tausend</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1275">NOUN</tspan><tspan>Case=Gen|Gender=Masc|Number=Plur</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1450">er</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1450">PRON</tspan><tspan>Case=Nom|Gender=Masc|Number=Sing|Person=3|PronType=Prs</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1625">das</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1625">PRON</tspan><tspan>Case=Acc|Gender=Neut|Number=Sing|PronType=Dem</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1800">was</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1800">PRON</tspan><tspan>Case=Acc|Gender=Neut|Number=Sing|PronType=Int</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="1975">Alexander</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="1975">PROPN</tspan><tspan>Case=Nom|Gender=Masc|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2150">Walli</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2150">PROPN</tspan><tspan>Case=Nom|Gender=Masc|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2325">heute</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2325">ADV</tspan><tspan></tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2500">ist</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2500">AUX</tspan><tspan>Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2675">Putins</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2675">PROPN</tspan><tspan>Case=Nom|Definite=Ind|Gender=Fem|Number=Sing|PronType=Art</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="2850">gr&#246;&#223;ter</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="2850">ADJ</tspan><tspan>Case=Dat|Degree=Pos|Gender=Fem|Number=Sing</tspan></text>\n    <text class="displacy-token" fill="currentColor" text-anchor="middle" y="747.0">    <tspan class="displacy-word" fill="currentColor" x="3025">Gegner</tspan>    <tspan class="displacy-tag" dy="2em" fill="currentColor" x="3025">NOUN</tspan><tspan>Case=Nom|Number=Sing</tspan></text>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-0" stroke-width="2px" d="M70,702.0 C70,439.5 550.0,439.5 550.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-0" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">sb</textPath>    </text>    <path class="displacy-arrowhead" d="M70,704.0 L62,692.0 78,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-1" stroke-width="2px" d="M245,702.0 C245,614.5 365.0,614.5 365.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible;font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-1" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pnc</textPath>    </text>    <path class="displacy-arrowhead" d="M245,704.0 L237,692.0 253,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-2" stroke-width="2px" d="M70,702.0 C70,527.0 370.0,527.0 370.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible;font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-2" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M370.0,704.0 L378.0,692.0 362.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-3" stroke-width="2px" d="M595,702.0 C595,614.5 715.0,614.5 715.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-3" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">mo</textPath>    </text>    <path class="displacy-arrowhead" d="M715.0,704.0 L723.0,692.0 707.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-4" stroke-width="2px" d="M945,702.0 C945,527.0 1245.0,527.0 1245.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-4" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M945,704.0 L937,692.0 953,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-5" stroke-width="2px" d="M1120,702.0 C1120,614.5 1240.0,614.5 1240.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-5" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M1120,704.0 L1112,692.0 1128,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-6" stroke-width="2px" d="M770,702.0 C770,439.5 1250.0,439.5 1250.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-6" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">ag</textPath>    </text>    <path class="displacy-arrowhead" d="M1250.0,704.0 L1258.0,692.0 1242.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-7" stroke-width="2px" d="M595,702.0 C595,352.0 1430.0,352.0 1430.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-7" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">sb</textPath>    </text>    <path class="displacy-arrowhead" d="M1430.0,704.0 L1438.0,692.0 1422.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-8" stroke-width="2px" d="M595,702.0 C595,264.5 1610.0,264.5 1610.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-8" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pd</textPath>    </text>    <path class="displacy-arrowhead" d="M1610.0,704.0 L1618.0,692.0 1602.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-9" stroke-width="2px" d="M595,702.0 C595,177.0 1790.0,177.0 1790.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-9" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pd</textPath>    </text>    <path class="displacy-arrowhead" d="M1790.0,704.0 L1798.0,692.0 1782.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-10" stroke-width="2px" d="M1995,702.0 C1995,614.5 2115.0,614.5 2115.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-10" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pnc</textPath>    </text>    <path class="displacy-arrowhead" d="M1995,704.0 L1987,692.0 2003,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-11" stroke-width="2px" d="M1820,702.0 C1820,527.0 2120.0,527.0 2120.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-11" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M2120.0,704.0 L2128.0,692.0 2112.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-12" stroke-width="2px" d="M595,702.0 C595,89.5 2320.0,89.5 2320.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-12" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">mo</textPath>    </text>    <path class="displacy-arrowhead" d="M2320.0,704.0 L2328.0,692.0 2312.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-13" stroke-width="2px" d="M595,702.0 C595,2.0 2500.0,2.0 2500.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-13" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">cj</textPath>    </text>    <path class="displacy-arrowhead" d="M2500.0,704.0 L2508.0,692.0 2492.0,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-14" stroke-width="2px" d="M2695,702.0 C2695,527.0 2995.0,527.0 2995.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-14" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">ag</textPath>    </text>    <path class="displacy-arrowhead" d="M2695,704.0 L2687,692.0 2703,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-15" stroke-width="2px" d="M2870,702.0 C2870,614.5 2990.0,614.5 2990.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-15" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">nk</textPath>    </text>    <path class="displacy-arrowhead" d="M2870,704.0 L2862,692.0 2878,692.0" fill="currentColor"/></g>\n    <g class="displacy-arrow">    <path class="displacy-arc" id="arrow-06a216d0b81d4402987fb9fc3681fe58-0-16" stroke-width="2px" d="M2520,702.0 C2520,439.5 3000.0,439.5 3000.0,702.0" fill="none" stroke="currentColor"/>    <text dy="1.25em" style="overflow:visible; font-size: 0.8em; letter-spacing: 1px">        <textPath xlink:href="#arrow-06a216d0b81d4402987fb9fc3681fe58-0-16" class="displacy-label" startOffset="50%" side="left" fill="currentColor" text-anchor="middle">pd</textPath>    </text>    <path class="displacy-arrowhead" d="M3000.0,704.0 L3008.0,692.0 2992.0,692.0" fill="currentColor"/></g>\n  </svg>\n</div>\n'
"""



#---------------------------------------------------------------------------------------------------------------------

#PRODIGY RECIPE

def get_stream(file):
    i = 0
    for eg in file:
        eg["html"] = l[i]
        yield eg
        i += 1


@prodigy.recipe("custom_recipe")
def custom_recipe(dataset, jsonl_file):

    stream = JSONL(jsonl_file)
    stream = get_stream(stream)
    stream = add_tokens(nlp, stream)
    blocks = [
    {"view_id": "html"},
    {"view_id": "ner_manual"}  
    ]
    return{
    "dataset": dataset,
    "stream": stream,
    "view_id": "blocks",
    "config": {
    "labels": ["LABEL1", "LABEL2", "LABEL3"],
    "blocks":blocks
    }}


#-----------------------------------------------------------------------------------------------------------------------------


#PRODIGY ANNOTATIONS

prodigy.serve("custom_recipe some_data final_transcription.jsonl")



#------------------------------------------------------------------------------------------------------------------#

#AUTOMATIC ANALYSIS

print(50*"-")

print("Lexical diversity")
#type token ratio
tokens = [t.text for t in doc if not t.is_punct] #and not t.is_stop
num_tokens = len(tokens)
word_freq = Counter(tokens)
num_types = len(word_freq)
ttr = num_types / num_tokens *100
print("Type-token ratio: ",ttr)

#MATTR
mattr = []
window_width = 10
last_index = num_tokens - window_width
for start in range(last_index):
    window = tokens[start:start+window_width]
    word_count = Counter(window)
    types = list(word_count.keys())
    local_ttr = (len(types))/(len(window)) 
    mattr.append(local_ttr)
mattr_score = sum(mattr)/len(mattr)*100
print("Moving-average type-token ratio: ", mattr_score)


#Brunet's Index
bi = num_tokens**num_types**(-0.165)
print("Brunet's Index: ", bi)

#Honoré's statistic
#v1 = number of unique words
v1 = 0
for w in word_freq:
    if word_freq[w] == 1:
        v1 += 1

hs = 100*math.log(num_tokens)/((1-v1)/num_types)
print("Honoré's statistic: ", hs)



print(50*"-")

print("Lexical density")
# cd = number of verbs + nouns + adjectives + adverbs / number of tokens
pos = Counter([t.pos_ for t in doc if not t.is_punct])
cd = pos["VERB"]+pos["NOUN"]+pos["PROPN"]+pos["ADJ"]+pos["ADV"] / sum(pos.values())
print(cd) 

print(50*"-")


#average sentence length

number_of_words = 0
number_of_sentences = 0

for s in doc.sents:
    number_of_sentences += 1
    for t in s:
        if not t.is_punct:
            number_of_words += 1

asl = number_of_words / number_of_sentences

print("Average sentence lentgh:", asl)

#counter for pos tags
pos = [t.pos_ for t in doc]
num_pos = Counter(pos)
#print(num_pos)

print(50*"-")

#write numbers to file
results_file = input("Enter new file name where to write results: ")


with open(results_file, "w") as f:
    f.write("Lexical diversity\nType-token ratio: "+str(ttr)+"\nMoving-average type-token ratio: "+str(mattr_score)+"\nBrunet's Index: "+str(bi)+"\nHonoré's statistic: "+str(hs))
    f.write("\n\nLexical density\nCD: "+str(cd))
    f.write("\n\nAverage sentence length: "+str(asl))

print("Wrote results to ", results_file)

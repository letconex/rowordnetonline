# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, jsonify
import rowordnet
from rowordnet import *
wn = rowordnet.RoWordNet()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_AS_ASCII'] = False  # to print jsonify to utf-8 directly / or use json library instead
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

def filterpos(word, posro): # NOUN, VERB, ADVERB, ADJECTIVE
    if posro == 'NOUN':
        synset_idx = wn.synsets(literal=word, pos=Synset.Pos.NOUN)
        print("Filter by '{}'".format(posro))
    elif posro == 'VERB':
        synset_idx = wn.synsets(literal=word, pos=Synset.Pos.VERB)
        print("Filter by '{}'".format(posro))
    elif posro == 'ADVERB':
        synset_idx = wn.synsets(literal=word, pos=Synset.Pos.ADVERB)
        print("Filter by '{}'".format(posro))
    elif posro == 'ADJECTIVE':
        synset_idx = wn.synsets(literal=word, pos=Synset.Pos.ADJECTIVE)
        print("Filter by '{}'".format(posro))
    else:
        synset_idx = wn.synsets(literal=word)
        # print(synset_idx)
    if synset_idx == []:
        notfoundmessage = f'{word} not found!'
        # print(notfoundmessage)
        return [notfoundmessage]
    else:
        wordlist = []
        deflist = []
        for synset_ID in synset_idx:
            synset_object = wn(synset_ID)
            # print("{0}, {1}, {2}, {3}, {4}".format(synset_object.literals, synset_object.pos, synset_object.definition, synset_object.domain, synset_object.sumo))
            # print(type(synset_object.literals)) # 
            # print("{0}, {1}, {2}".format([str(x) for x in synset_object.literals], synset_object.pos, synset_object.definition))
            # print("<b>{0}</b> = {1}<br>".format(str(synset_object.literals)[2:-2].replace("_", " ").replace("'", ""), synset_object.definition))
            words = str(synset_object.literals)[2:-2].replace("_", " ").replace("'", "")
            defs = str(synset_object.definition)
            # print(words)
            # print(defs)
            wordlist.append(words)
            deflist.append(defs)
    # return words, defs
    return wordlist, deflist

@app.route('/about')
def about():
    flash('Search Romanian Wordnet: POS can be NOUN, VERB, ADVERB, ADJECTIVE!')
    return render_template("base.html")

@app.route('/', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        searchterm = request.form.get('searchformterm')
        POS = 'ALL'
        wordnetresult = filterpos(searchterm, POS)
        print(f'Query term: {searchterm}')
        return render_template("result.html", searchterm=searchterm, wordnetresult=wordnetresult, POS=POS)
    if request.method == 'GET':
        searchterm = ['Insert term']
        wordnetresult = 'Insert term'
        POS = 'ALL'
        return render_template("search.html", searchterm=searchterm, wordnetresult=wordnetresult, POS=POS)
    
    

if __name__ == '__main__':
   app.config['SECRET_KEY'] = 'TiberiuCristianLeon'
   app.secret_key = 'TiberiuCristianLeon'
   app.run(debug = True, host='127.0.0.1', port=5000)
   # app.run(debug = False, host = '127.0.0.1', port = 5000)

'''

    
@app.route('/')
def halllo():
    # print ("Hello world")
    intro = r"<br>Example: https://rowordnet.herokuapp.com/search/?word=casa&pos=NOUN"
    return intro
    
@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e):
# defining function
    messagenotfound = 'Search term not entered!'
    return messagenotfound

@app.route("/search/")
def home(word="", pos=""):
    word = request.args.get('word', word)
    # word = "tren"
        # modelname = 'Helsinki-NLP/opus-mt-{0}-{1}'.format(src, trg)
    wn = rowordnet.RoWordNet()
    #As words are polysemous, searching for a word will likely yield more than one synset. A word is known as a literal in RoWordNet, and every synset has one or more literals that are synonyms.
    try: # if not entered, response type defaults to html
        posro = request.args.get('pos', posro) # NOUN, VERB, ADVERB, ADJECTIVE
        # posro = "NOUN"
    except:
        print('No POS!')
        # return('No POS!')
        posro = ''
    try:
        resultlist = filterpos(word, posro)
        wordlist, deflist = filterpos(word, posro)
        # print ("Found")
    # return word
        # return tuple(resultlist)
        zipx = zip(wordlist, deflist)
        return render_template("list.html", wordlist = wordlist, deflist = deflist, zipx = zipx, word=word, posro=posro)
        # for res in tuple(resultlist):
            # return res
    except Exception as error:
        print(word + ' not found! ')
        print(error)
        return('Not found!')
    
# synset_ids = wn.synsets(literal=word)
# print(synset_ids)
# print(wn.synsets(word))
#for synset_id in wn.synsets(word):
    # wn.print_synset(synset_id)
    # synset_object = wn.synset(synset_id)
    # synset_object = wn(synset_id)
    # print(synset_object)
    # pass
    # print("Literals (synonyms): {}".format(synset_object.literals))
    # print("Definition: {}".format(synset_object.definition))
    # print("POS, DOMAIN, SUMO: {0}, {1}, {2}".format(synset_object.pos, synset_object.domain, synset_object.sumo))
    # print("Print its ID: {}".format(synset_object.pos + ' - ' + synset_object.domain + ' - ' + synset_object.sumo))
# synset_ids_all = wn.synsets() # get all synset IDs in RoWordNet
# synset_ids_verbs = wn.synsets(pos=synset.pos.VERB) # get all verb synset IDs
# synset_ids = wn.synsets(literal="cal", pos=Synset.Pos.NOUN) # get all synset IDs that contain word "cal" and are nouns
# print(synset_ids)
# synset_id = wn.synsets(word)[2] # select the third synset from all synsets containing word "tren"
# print("\nPrint all outbound relations of {}".format(wn.synset(synset_id)))
# outbound_relations = wn.outbound_relations(synset_id)
# for outbound_relation in outbound_relations:
    # target_synset_id = outbound_relation[0]        
    # relation = outbound_relation[1]
    # print("\tOutboud relation [{}] to synset {}".format(relation,wn.synset(target_synset_id)))
    
# synset_id = wn.synsets(word)[2] # select the third synset from all synsets containing word "tren"
# print("\nPrint all inbound relations of {}".format(wn.synset(synset_id)))
# inbound_relations = wn.inbound_relations(synset_id)
# for inbound_relation in inbound_relations:
    # target_synset_id = inbound_relation[0]        
    # relation = inbound_relation[1]
    # print("\t Inbound relation [{}] to synset {}".format(relation,wn.synset(target_synset_id)))

if __name__ == '__main__':
   # app.run(threaded=True, port=5000, debug = True)
   app.run(port=5000, debug = True)
   '''

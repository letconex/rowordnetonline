import requests
from flask import Flask, render_template, request, jsonify
import scripts.staticparams
import scripts.gtranslate, scripts.deeplfreeapi, scripts.mttranslateedge, scripts.hallodotro
app = Flask(__name__, template_folder='templates', static_folder='static')

alldiclist = scripts.staticparams.alldiclist
allmtlist = scripts.staticparams.allmtlist
alllangshort = scripts.staticparams.alllangshort
pages = scripts.staticparams.dictpages
selectedradiooptions = scripts.staticparams.selectedradiooptions
dictselectedcheckstates = scripts.staticparams.dictselectedcheckstates
mtselectedcheckstates = scripts.staticparams.mtselectedcheckstates
SLselectedcheckstates = scripts.staticparams.SLselectedcheckstates
TLselectedcheckstates = scripts.staticparams.TLselectedcheckstates
print(TLselectedcheckstates)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template("home.html", pages=pages)
    if request.method == 'POST':
        selecteddiclist = request.form.getlist('dictionaries')
        argsdiclist = request.args.get('dictionaries')
        sourcelang = request.form.get('sourcelanguagenames')
        targetlang = request.form.get('targetlanguagenames')
        return render_template("resultdic.html", SLselectedcheckstates=SLselectedcheckstates, TLselectedcheckstates=TLselectedcheckstates, selecteddiclist=selecteddiclist, sourcelang=sourcelang, targetlang=targetlang, dictselectedcheckstates=dictselectedcheckstates, mtselectedcheckstates=mtselectedcheckstates)

@app.route('/resultdic.html', methods=['POST', 'GET'])
def resultdic():
    if request.method == 'GET':
        return render_template("searchdic.html")
    if request.method == 'POST':
        postedoptions = request.form
        # parsepostedresponse(postedoptions)
        print(postedoptions)
        for postedselection in postedoptions:
            # print(postedselection)
            pass
        # for key, value in postedoptions.items():
            # print(key + '---' + value)
        # hello = get_template_attribute('searchdic.html', 'dictionaries')
        # selecteddiclist = request.form.getlist('dictionaries')
        selecteddiclist = postedoptions.getlist('dictionaries')
        # print(selecteddiclist)
        # sourcelang = request.form.get('sourcelanguagenames')
        sourcelang = postedoptions['sourcelanguagenames']
        # print(sourcelang)
        targetlang = postedoptions['targetlanguagenames']
        # print(targetlang)
        searchformterm = postedoptions['searchformterm']
        # print(searchformterm)
        # searchformoptions = request.form.get('bimono')
        searchformoptions = postedoptions['bimono']
        print(searchformoptions)
        for selecteddict in alldiclist:
            if selecteddict in selecteddiclist:
                dictselectedcheckstates[selecteddict] = 'checked'
            else:
                dictselectedcheckstates[selecteddict] = 'unchecked'
        # print(dictselectedcheckstates)
        for selectedsourcelang in SLselectedcheckstates:
            if selectedsourcelang == sourcelang:
                SLselectedcheckstates[selectedsourcelang] = 'selected'
            else:
                SLselectedcheckstates[selectedsourcelang] = 'unselected'
            # print("selectedsourcelang = " + str(SLselectedcheckstates))
        for selectedtargetlang in TLselectedcheckstates:
            if selectedtargetlang == targetlang:
                TLselectedcheckstates[selectedtargetlang] = 'selected'
            else:
                TLselectedcheckstates[selectedtargetlang] = 'unselected'
        resultdict = {}
        rows = []
        if 'Hallo.ro' in selecteddiclist:
            halloresult = scripts.hallodotro.halloro(sourcelang, targetlang, searchformterm, limit=30).getpages()
            halloresult.insert(0, ('<b>Dictionary</b>', '<b>Hallo.ro</b>'))
            rows.append(halloresult)
            # print(rows)
        # deeplapiresult = "result from api"
        # rows.append(searchformterm)
        # rows.append(deeplapiresult)
        # resultdict["Deepl"] = rows
        # print(TLselectedcheckstates)

        return render_template("resultdic.html", SLselectedcheckstates=SLselectedcheckstates, TLselectedcheckstates=TLselectedcheckstates, selecteddiclist=selecteddiclist, sourcelang=sourcelang, targetlang=targetlang, searchformterm=searchformterm, rows=rows, alldiclist=alldiclist, alllangshort=alllangshort, searchformoptions=searchformoptions, pages=pages, dictselectedcheckstates=dictselectedcheckstates, mtselectedcheckstates=mtselectedcheckstates, radiooptions=selectedradiooptions)

@app.route('/resultmt.html', methods=['POST', 'GET'])
def resultmt():
    if request.method == 'GET':
        return render_template("searchmt.html")
    if request.method == 'POST':
        selectedmtlist = request.form.getlist('mtengines')
        sourcelang = request.form.get('sourcelanguagenames')
        targetlang = request.form.get('targetlanguagenames')
        searchformterm = request.form.get('searchformterm')
        for selectedmt in allmtlist:
            if selectedmt in selectedmtlist:
                mtselectedcheckstates[selectedmt] = 'checked'
            else:
                mtselectedcheckstates[selectedmt] = 'unchecked'
        for selectedsourcelang in SLselectedcheckstates:
            if selectedsourcelang == sourcelang:
                SLselectedcheckstates[selectedsourcelang] = 'selected'
            else:
                SLselectedcheckstates[selectedsourcelang] = 'unselected'
        for selectedtargetlang in TLselectedcheckstates:
            if selectedtargetlang == targetlang:
                TLselectedcheckstates[selectedtargetlang] = 'selected'
            else:
                TLselectedcheckstates[selectedtargetlang] = 'unselected'
        rows = []
        # print(selectedmtlist)
        if 'Google' in selectedmtlist:
            googleresult = scripts.gtranslate.gtrans(sourcelang, targetlang, searchformterm).gtranslate()
            rows.append('Google')
            rows.append(googleresult)
        if 'Microsoft' in selectedmtlist:
            microsoftresult = scripts.mttranslateedge.mtrans(sourcelang, targetlang, searchformterm).mtranslate()
            rows.append('Microsoft')
            rows.append(microsoftresult)
        if 'Deepl' in selectedmtlist:
            deeplresult = scripts.deeplfreeapi.deeplfreeapi(sourcelang, targetlang, searchformterm)
            rows.append('Deepl')
            rows.append(deeplresult)
        print(mtselectedcheckstates)
        return render_template("resultmt.html", SLselectedcheckstates=SLselectedcheckstates, TLselectedcheckstates=TLselectedcheckstates, selectedmtlist=selectedmtlist, sourcelang=sourcelang, targetlang=targetlang, mtselectedcheckstates=mtselectedcheckstates, searchformterm=searchformterm, rows=rows, allmtlist=allmtlist, alllangshort=alllangshort, radiooptions=selectedradiooptions, pages=pages)

@app.route('/home.html')
def home():
    return render_template('home.html', pages=pages)
@app.route('/about.html')
def about():
    return render_template('about.html', alldiclist=alldiclist, alllangshort=alllangshort, allmtlist=allmtlist, pages=pages)
@app.route('/header.html')
def header():
    return render_template('header.html', pages=pages)
@app.route('/footer.html')
def footer():
    return render_template('footer.html', pages=pages)
@app.route('/searchdic.html')
def searchdic():
    return render_template('searchdic.html', SLselectedcheckstates=SLselectedcheckstates, TLselectedcheckstates=TLselectedcheckstates, alldiclist=alldiclist, alllangshort=alllangshort, pages=pages, radiooptions=selectedradiooptions, dictselectedcheckstates=dictselectedcheckstates)
@app.route('/searchmt.html')
def searchmt():
    return render_template('searchmt.html', SLselectedcheckstates=SLselectedcheckstates, TLselectedcheckstates=TLselectedcheckstates, allmtlist=allmtlist, alllangshort=alllangshort, pages=pages, radiooptions=selectedradiooptions, mtselectedcheckstates=mtselectedcheckstates)

if __name__ == '__main__':
   # app.run(debug = True, host='192.168.0.106', port=5000)
   # app.run(debug = True, host='192.168.1.101', port=5000)
   app.run(debug = True, host='127.0.0.1', port=5000)
   # app.run(debug = False, host = '127.0.0.1', port = 5000)
   app.secret_key = '12345'
   app.config['SECRET_KEY'] = '123'
# if __name__ == '__main__':
# app.run(debug = False, host='127.0.0.1', port=5001)
    # app.run()

from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)
resultfile = 'resultfile.txt'
def append2file(file2write2, text2write): # if file exists, if not a+
    file = open(file2write2, mode='a+', encoding='utf-8')
    file.write(str(text2write).encode('utf-8').decode('utf-8'))
    file.close()

@app.route('/')
def home():
    return 'Wordnet home'
@app.route('/x')
def homex():
   with sql.connect("MyDICs.db") as con:
        cur = con.cursor()
        # tablename = 'IATE-DERO'
        searchterm = 'Lagerung'
        sourcelang = 'DE'
        targetlang = 'RO'
        # queryS = 'SELECT * FROM "' + tablename + '" WHERE "' + sourcelang + '" LIKE "%' + str(searchterm) + '%"'
        # SELECT * FROM "IATE-DERO" WHERE "DE" LIKE "%Lagerung%"
        # return str(queryS)
        # cur.execute(queryS)
        # result = cur.fetchall()
        # return(str({{sourcelang}}))
        queryN = 'SELECT name FROM sqlite_master WHERE type = "table"'
        cur.execute(queryN)
        tablenames = cur.fetchall()
        tablenamescut = []
        for tablename in tablenames:
            tablename = str(tablename)[2:-3]
            tablenamescut.append(str(tablename))
        tablenames = tablenamescut
        # queryC = 'SELECT COUNT (*) FROM "' + str(tablenames [0])[2:-3] + '"'
        # return render_template("home.html", sourcelang = sourcelang, targetlang = targetlang, tablenames = tablenames)
        counts = []
        for tablename in tablenames:
            queryC = 'SELECT COUNT (*) FROM "' + str(tablename) + '"'
            cur.execute(queryC)
            count = cur.fetchall()            # count the number of rows in table
            counts.append(str(count)[2:-3])
            # return render_template("home.html", sourcelang = sourcelang, targetlang = targetlang, tablenames = tablenames, tablename = tablename, counts = counts, queryC = queryC)
        # typetablename = str(type(tablename))
        # tablenamelist = list(tablenames)
        zips = zip(tablenames, counts)
        return render_template("home.html", sourcelang = sourcelang, targetlang = targetlang, tablenamess = tablenamescut, countss = counts, zips = zips)
        # return render_template("home.html", sourcelang = sourcelang, targetlang = targetlang, tablenames = tablenamescut, tablename = tablename, counts = counts, queryC = queryC, count = count, zips = zip(tablenames, counts))
        # return render_template("home.html", sourcelang = sourcelang, targetlang = targetlang, tablenames = tablenames, queryC = queryC)

        # queryC = 'SELECT COUNT (*) FROM "' + tablename + '"'
        # count = cur.execute(queryC).fetchone()[0] # count the number of rows in table        # get list of table names# return render_template('home.html')
# return 'home.html'
        # return(str(result[1]))
        # queryA = 'INSERT INTO tablename (name,addr,city,pin) VALUES (("Buddy Rich"),("Candido"),("Charlie Byrd"),("Charlie 1234"))'
        # cur.execute(queryA)
        # con.commit()
        # return("Record successfully added")
        # con.close()

@app.route('/enternew')
def new_student():
   return render_template('addnew.html')

@app.route('/showsearchform')
def showsearchform():
    return render_template("search.html")


# @app.route('/<some_place>')
# def some_place_page(some_place):
@app.route('/searchit', methods = ['POST', 'GET'])
def searchit():
    tablename = 'IATE-DERO'
    # searchterm = 'Lagerung'
    sourcelang = 'DE'
    targetlang = 'RO'
    if request.method == 'POST':
        # try:
        searchterm = request.form['searchformterm']
            # addr = request.form['add']
            # city = request.form['city']
            # pin = request.form['pin']
        # return str(nm)
    # msg = "Record successfully added"
        # return render_template("result.html", msg = nm)
        # return render_template("result.html", msg = msg)
        with sql.connect("MyDICs.db") as con:
            cur = con.cursor()
            queryS = 'SELECT * FROM "' + tablename + '" WHERE "' + sourcelang + '" LIKE "%' + str(searchterm) + '%"'
            cur.execute(queryS)
            rows = cur.fetchall()
            # con.commit()
            for row in rows:
                text2write = str(row[0]) + ' = ' + str(row[1]) + '\r\n'
                append2file(resultfile, text2write)
            # msg = "Record successfully added"
            return render_template("list.html", sourcelang = sourcelang, rows = rows, targetlang = targetlang, searchterm = searchterm)
            con.close()
        # except:
            # con.rollback()
            # msg = "error in insert operation"
        # finally:
            # return render_template("result.html",msg = msg)
            # return render_template("list.html", sourcelang = sourcelang, resultrows = rows, targetlang = targetlang)
            # con.close()

#http://traduceri.eu.pythonanywhere.com/search/?slang=DE&term=Katze
# @app.route('/search', methods = ['POST', 'GET'])
@app.route('/search/slang=<sourcelang>&term=<searchterm>')
def searchitvar(sourcelang, searchterm):
    #con = sql.connect("MyDICs.db")
    #con.row_factory = sql.Row
    #cur = con.cursor()
    tablename = 'IATE-DERO'
    # sourcelang = 'DE'
    sourcelang = request.args.get('slang')
    print(sourcelang)
    targetlang = 'RO'
    searchterm = request.args.get('term')
    print(searchterm)
    if request.method == 'GET':
        # try:
        with sql.connect("MyDICs.db") as con:
            cur = con.cursor()
            queryS = 'SELECT * FROM "' + tablename + '" WHERE "' + sourcelang + '" LIKE "%' + str(searchterm) + '%"'
            cur.execute(queryS)
            rows = cur.fetchall()
            return render_template("list.html", sourcelang = sourcelang, rows = rows, targetlang = targetlang, searchterm = searchterm)

            if rows == '':
                messagenotfound = 'Search term not found!'
                return render_template("notfound.html", msg = messagenotfound)
            con.close()
        # except:
            # con.rollback()
            # msg = "error in insert operation"
        # finally:
            # return render_template("result.html",msg = msg)
            # return render_template("list.html", sourcelang = sourcelang, resultrows = rows, targetlang = targetlang)
            # con.close()

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']

         with sql.connect("MyDICs.db") as con:
            cur = con.cursor()
            tablename = 'DE-RO'
            cur.execute("INSERT INTO tablename (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )

            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"

      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
    con = sql.connect("MyDICs.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    tablename = 'IATE-DERO'
    searchterm = 'Lagerung'
    sourcelang = 'DE'
    targetlang = 'RO'
    queryS = 'SELECT * FROM "' + tablename + '" WHERE "' + sourcelang + '" LIKE "%' + str(searchterm) + '%"'
    # SELECT * FROM "IATE-DERO" WHERE "DE" LIKE "%Lagerung%"
    # return str(queryS)
    cur.execute(queryS)
    # result = cur.fetchall()
    # return(str(result))
   # cur.execute("select * from tablename")
    rows = cur.fetchall()
    return render_template("list.html", sourcelang = sourcelang, resultrows = rows, targetlang = targetlang)
    # return render_template("list.html", resultrows = rows)

# import sqlite3
# conn = sqlite3.connect('MyDICs.db')
# print ("Opened database successfully")
# conn.execute('CREATE TABLE tablename (name TEXT, addr TEXT, city TEXT, pin TEXT)')
# print ("Table created successfully")
# conn.close()

# if __name__ == '__main__':
# app.run(debug = False, host='127.0.0.1', port=5001)
#     app.run()

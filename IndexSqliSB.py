#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify
import sqlite3
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # to print jsonify to utf-8 directly / or use json library instead
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
db = "MyDICs.db" # tablename = 'IATE-DERO'

def gettablenames(db):
   with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        queryCNN = 'SELECT name FROM sqlite_master WHERE type = "table"'
        cursor.execute(queryCNN)
        tablenames = cursor.fetchall() #        print(tablenames)
        tablenamescut = []
        for tablename in tablenames:
            tablename = str(tablename)[2:-3]
            tablenamescut.append(str(tablename))
        tablenames = tablenamescut #         print(tablenames)
        return tablenames
        
def getcolumnnamesintable(db, tablename):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        # queryCNP = 'PRAGMA table_info("' + tablename + '")'
        # cursor.execute(queryCNP)
        # columnnames = cursor.fetchall() #         print(columnnames[0][1])
        # sourcelang = columnnames[0][1]
        # targetlang = columnnames[1][1] #         print(columnnames[1][1])
        # conn.row_factory = sqlite3.Row                 print(conn.row_factory)
        queryCN = 'select * from "' + str(tablename)   + '"'
        cursor = cursor.execute(queryCN)      # columnnames = cursor.description            print(columnnames)
        columnname = [description[0] for description in cursor.description]
        sourcelang = columnname[0]
        targetlang = columnname[1]
        return sourcelang, targetlang
        
def getcolumnnamesalltables(db, tablenames):
    sourcelangs = []
    targetlangs = []
    for tablename in tablenames:
        sourcelang = getcolumnnamesintable(db, tablename)[0]
        targetlang = getcolumnnamesintable(db, tablename)[1]
        sourcelangs.append(str(sourcelang))
        targetlangs.append(str(targetlang))
    return sourcelangs, targetlangs # return column names, source and target languages
        
def getterm(db, tablename, sourcelang, searchterm):
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            queryS = 'SELECT * FROM "' + tablename + '" WHERE "' + sourcelang + '" LIKE "%' + str(searchterm) + '%"'
            cursor.execute(queryS)
            searchresults = cursor.fetchall()
            return searchresults
            conn.close()
            
def getcounttable(db, tablename):
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        queryC = 'SELECT COUNT (*) FROM "' + str(tablename) + '"'
        cursor.execute(queryC)
        count = cursor.fetchall()            # count the number of rows in table
        str(count)[2:-3]
        return count
        
def getcountalltables(db, tablenames):
    counts = []
    for tablename in tablenames:
        rowsintable = getcounttable(db, tablename)
        rowsintable = str(rowsintable)[2:-3]
        counts.append(str(rowsintable))
    return counts
    

@app.route('/')
def home():
   with sqlite3.connect(db) as conn:
        cursor = conn.cursor()
        tablenames = gettablenames(db)
        counts = getcountalltables(db, tablenames)
        sourcelangs = getcolumnnamesalltables(db, tablenames)[0]
        targetlangs = getcolumnnamesalltables(db, tablenames)[1]
        zips = zip(tablenames, sourcelangs, targetlangs, counts)
        return render_template("home.html", tablenames = tablenames, counts = counts, sourcelangs = sourcelangs, targetlangs = targetlangs, zips = zips)
        
        # return render_template("home.html", sourcelang = sourcelang, targetlang = targetlang, tablenames = tablenamescut, tablename = tablename, counts = counts, queryC = queryC, count = count, zips = zip(tablenames, counts))
        # count = cursor.execute(queryC).fetchone()[0] # count the number of rows in table        # get list of table names# return render_template('home.html')
        # return(str(result[1]))
        # queryA = 'INSERT INTO tablename (name,addr,city,pin) VALUES (("Buddy Rich"),("Candido"),("Charlie Byrd"),("Charlie 1234"))'
        # cursor.execute(queryA)
        # conn.commit()
        # return("Record successfully added")
        # conn.close()
   
@app.route('/searchform', methods = ['POST', 'GET'])
def searchform():
    tablenames = gettablenames(db)
    columnnames = getcolumnnamesalltables(db, tablenames)
    zipx = zip(tablenames, columnnames)
    return render_template("search.html", tablenames = tablenames, columnnames = columnnames, zipx = zipx)
    # return render_template("search.html", zipx = zipx)


# @app.route('/<some_place>')
# def some_place_page(some_place):
@app.route('/searchit', methods = ['POST', 'GET'])
def searchit():
    # tablename = 'IATE-DERO'
    tablename = request.form['tables']
    columnnames = getcolumnnamesintable(db, tablename)
    sourcelang = request.form['languagenames']
    searchterm = request.form['searchformterm']
    # searchterm = 'Lagerung'
    # sourcelang = columnnames[0]
    targetlang = columnnames[1]
    rows = getterm(db, tablename, sourcelang, searchterm)
    if request.method == 'POST':
        # try:
        # searchterm = request.form['searchformterm']
        rows = getterm(db, tablename, sourcelang, searchterm)
            # addr = request.form['add']
            # city = request.form['city']
            # pin = request.form['pin']
        # return str(nm)
    # msg = "Record successfully added"
        # return render_template("result.html", msg = nm)
        # return render_template("result.html", msg = msg)
        with sqlite3.connect("MyDICs.db") as conn:
            cursor = conn.cursor()
            # queryS = 'SELECT * FROM "' + tablename + '" WHERE "' + sourcelang + '" LIKE "%' + str(searchterm) + '%"'
            queryS = 'SELECT * FROM "' + tablename + '" WHERE "' + sourcelang + '" LIKE "%' + str(searchterm) + '%"'
            cursor.execute(queryS)
            # rows = cursor.fetchall()
            # conn.commit()
            # msg = "Record successfully added"
            return render_template("list.html", sourcelang = sourcelang, rows = rows, targetlang = targetlang, searchterm = searchterm)
            conn.close()
        # except:
            # conn.rollback()
            # msg = "error in insert operation"
        # finally:
            # return render_template("result.html",msg = msg)
            # return render_template("list.html", sourcelang = sourcelang, resultrows = rows, targetlang = targetlang)
            # conn.close()

# @app.route('/search', methods = ['POST', 'GET'])
@app.route('/apisearch/', methods = ['POST', 'GET'])
# @app.route('/search/<tablename>+<sourcelang>+<targetlang>+<searchterm>', methods = ['POST', 'GET'])
# http://192.168.1.101:5000/apisearch/?tablename=IATE-DERO&sourcelang=DE&targetlang=RO&searchterm=Haus
def searchitvar(tablename="", sourcelang="", targetlang="", searchterm=""):
    # tablename = request.args.get('tablename', tablename)
    tablename = "IATE-DERO"
    sourcelang = request.args.get('sourcelang', sourcelang)
    targetlang = request.args.get('targetlang', targetlang)
    searchterm = request.args.get('searchterm', searchterm)
    if searchterm == '':
        messagenotfound = 'Search term not found!'
        return render_template("notfound.html", messagenotfound = messagenotfound)
    if request.method == 'GET':
        # try:
        with sqlite3.connect("MyDICs.db") as conn:
            cursor = conn.cursor()
            queryS = 'SELECT * FROM "' + tablename + '" WHERE "' + sourcelang + '" LIKE "' + str(searchterm) + '%"'
            # queryS = 'SELECT * FROM "' + tablename + '" WHERE "' + sourcelang + '" LIKE "%' + str(searchterm) + '%"'
            cursor.execute(queryS)
            rows = cursor.fetchall()
            sourcelang = sourcelang.upper()
            targetlang = targetlang.upper()
            return render_template("list.html", sourcelang = sourcelang, rows = rows, targetlang = targetlang, searchterm = searchterm)
            if rows == '':
                messagenotfound = 'Search term not found!'
                return render_template("notfound.html", msg = messagenotfound)
            conn.close()
        # except:
            # conn.rollback()
            # msg = "error in insert operation"
        # finally:
            # return render_template("result.html",msg = msg)
            # return render_template("list.html", sourcelang = sourcelang, resultrows = rows, targetlang = targetlang)
            # conn.close()

# @app.route('/search', methods = ['POST', 'GET'])
@app.route('/apisearchjson/', methods = ['POST', 'GET'])
# @app.route('/search/<tablename>+<sourcelang>+<targetlang>+<searchterm>', methods = ['POST', 'GET'])
# http://192.168.1.101:5000/apisearch/?tablename=IATE-DERO&sourcelang=DE&targetlang=RO&searchterm=Haus
def searchitvarjson(tablename="", sourcelang="", targetlang="", searchterm=""):
    # tablename = request.args.get('tablename', tablename)
    tablename = "IATE-DERO"
    sourcelang = request.args.get('sourcelang', sourcelang)
    targetlang = request.args.get('targetlang', targetlang)
    searchterm = request.args.get('searchterm', searchterm)
    if searchterm == '':
        messagenotfound = 'Search term not found!'
        return render_template("notfound.html", messagenotfound = messagenotfound)
    if request.method == 'GET':
        # try:
        with sqlite3.connect("MyDICs.db") as conn:
            cursor = conn.cursor()
            # queryS = 'SELECT * FROM "' + tablename + '" WHERE "' + sourcelang + '" LIKE "' + str(searchterm) + '%"'
            queryS = 'SELECT * FROM "' + tablename + '" WHERE "' + sourcelang + '" LIKE "%' + str(searchterm) + '%"'
            cursor.execute(queryS)
            rows = cursor.fetchall()
            # print(rows)
            # print(rows[0])
            sourcelang = sourcelang.upper()
            targetlang = targetlang.upper()
            if rows:
                # return ("Found!")
                jsontranss = jsonify({'source': rows[0][0]})
                jsontranst = jsonify({'translation': rows[0][1]})
                # print(jsontranst)
                # jsontrans = jsonify({'translation': rows[0]})
                # jsontrans = jsonify({'translation': rows})
                # jsontrans = jsonify({'translation': rows})
                # jsontrans = jsonify({'result': [{'source': rows[0][0], 'translation': rows[0][1]}]})
                # return jsontrans
                for row in rows:
                    print(row)
                    jsontrans = jsonify({'result': [{'source': row[0], 'translation': row[1]}]})
                print(jsontrans)
                
                render_template("listjson.html", sourcelang = sourcelang, rows = rows, targetlang = targetlang, searchterm = searchterm)
                return jsontrans
                # {todo_id: todos[todo_id]}
                # return str(jsontrans), str(jsontranss), str(jsontranst)
                # return '{} {} {}'.format(jsontrans, jsontranss, jsontranst)
            else:
                return jsonify({"translation": "Not found!"})
                # return "Not found!"
            # return render_template("listjson.html", sourcelang = sourcelang, rows = rows, targetlang = targetlang, searchterm = searchterm)
            if rows == '':
                messagenotfound = 'Search term not found!'
                return render_template("notfound.html", msg = messagenotfound)
            conn.close()
        # except:
            # conn.rollback()
            # msg = "error in insert operation"
        # finally:
            # return render_template("result.html",msg = msg)
            # return render_template("list.html", sourcelang = sourcelang, resultrows = rows, targetlang = targetlang)
            # conn.close()

# app name 
@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e):
# defining function
    messagenotfound = 'Search term not entered!'
    return render_template("notfound.html", msg = messagenotfound) 
  
@app.route('/enternew')
def new_student():
   return render_template('addnew.html')
   
@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sqlite3.connect("MyDICs.db") as conn:
            cursor = conn.cursor()
            tablename = 'DE-RO'
            cursor.execute("INSERT INTO tablename (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            conn.commit()
            msg = "Record successfully added"
      except:
         conn.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         conn.close()

@app.route('/list')
def list():
    con = sqlite3.connect("MyDICs.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    tablename = 'IATE-DERO'
    searchterm = 'Lagerung'
    sourcelang = 'DE'
    targetlang = 'RO'
    queryS = 'SELECT * FROM "' + tablename + '" WHERE "' + sourcelang + '" LIKE "%' + str(searchterm) + '%"'
    # SELECT * FROM "IATE-DERO" WHERE "DE" LIKE "%Lagerung%"
    # return str(queryS)
    cursor.execute(queryS)
    # result = cursor.fetchall()
    # return(str(result))
   # cursor.execute("select * from tablename")
    rows = cursor.fetchall()
    return render_template("list.html", sourcelang = sourcelang, resultrows = rows, targetlang = targetlang)
    # return render_template("list.html", resultrows = rows)

# import sqlite3

# conn = sqlite3.connect('MyDICs.db')
# print ("Opened database successfully")
# conn.execute('CREATE TABLE tablename (name TEXT, addr TEXT, city TEXT, pin TEXT)')
# print ("Table created successfully")
# conn.close()


if __name__ == '__main__':
   # app.run(debug = True, host='127.0.0.1', port=5000)
   # app.run(debug = True, host='192.168.0.106', port=5000)
   # app.run(debug = True, host='192.168.1.101', port=5000)
   app.run(debug = True, host='127.0.0.1', port=5000)
   home(db)

'''
Example usage:

from flask import jsonify

@app.route('/_get_current_user')
def get_current_user():
    return jsonify(username=g.user.username,
                   email=g.user.email,
                   id=g.user.id)

This will send a JSON response like this to the browser:

{
    "username": "admin",
    "email": "admin@localhost",
    "id": 42
}

'''
from types import MethodDescriptorType
from flask import Flask, render_template, request, redirect, url_for, flash, app, jsonify
from flask_mysqldb import MySQL
from flask import make_response  # cookies
from flask import session
from datetime import timedelta
import json  # enviar json

app = Flask(__name__)

# mysql conexion
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1098741116'
app.config['MYSQL_DB'] = 'encuesta4'

mysql = MySQL(app)  # pasarle la configuracion y se realiza conexion

app.secret_key = 'qwerty9230'  # se necesita siempre


@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM preguntas')
    data = cur.fetchall()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM opciones')
    data2 = cur2.fetchall()
    cur3 = mysql.connection.cursor()
    cur3.execute('SELECT * FROM valores_opciones')
    data3 = cur3.fetchall()
    print((data[15]))
    if (len(data) == 0):
        flash('Aun no hay datos guardados')
        return render_template('Inicio.html')
    else:
        return render_template('Inicio.html', preguntas=data, respuestas=data2, valores=data3)


@app.route('/optionForm')
def optionForm():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM preguntas')
    data = cur.fetchall()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM opciones')
    data2 = cur2.fetchall()
    cur3 = mysql.connection.cursor()
    cur3.execute('SELECT * FROM valores_opciones')
    data3 = cur3.fetchall()
    if (len(data) == 0):
        flash('Aun no hay datos guardados')
        return render_template('optionForm.html', preguntas=0, respuestas=0, valores=0)
    else:
        return render_template('optionForm.html', preguntas=data, respuestas=data2, valores=data3)



@app.route('/createQuestion')
def createQuestion():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM preguntas WHERE EstadoPreg = "CREADA"')
    data = cur.fetchall()
    if len(data)==0:
        flash('no hay preguntas registradas')
        return render_template('createQuestion.html', preguntas=0)
    else:
        return render_template('createQuestion.html', preguntas=1)

@app.route('/insertQuestion', methods=['POST'])
def insertQuestion():
    if request.method == 'POST':
        question = request.form['pregunta']
        estado = 'CREADA'
        cur = mysql.connection.cursor()  # obtenemos conexion
        cur.execute('INSERT INTO preguntas(TexPreg, EstadoPreg, FecRegPreg, HoraRegPreg) VALUES (%s,%s,CURDATE(),CURTIME())',
                    (question, estado))  # escrbimos la consulta
        mysql.connection.commit()
        flash('pregunta guardada satisfactoriamente')
        return render_template('createQuestion.html')



@app.route('/createOptions')
def createOptions():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM preguntas WHERE EstadoPreg = "CREADA"')
    data = cur.fetchall()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM opciones')
    data2 = cur2.fetchall()
    if len(data)==0:
        flash('no hay preguntas registradas por favor registra una para registrar las respuestas')
        return render_template('createQuestion.html', preguntas=0)
    if len(data2)==0:
        flash('no hay respuestas registradas por favor registra una')
        return render_template('createOptions.html', preguntas=data, option=0)
    else:
        return render_template('createOptions.html', preguntas=data, option=1)

@app.route('/insertOption', methods=['POST'])
def insertOption():
    if request.method == 'POST':
        idpreg = request.form['idpregunta']
        answer = request.form['respuesta']
        cur = mysql.connection.cursor()  # obtenemos conexion
        cur.execute('INSERT INTO opciones(IdPreguntas, TextOpc, FecRegOpc, HoraRegOpc) VALUES (%s,%s,CURDATE(),CURTIME())',
                    (idpreg, answer))  # escrbimos la consulta
        mysql.connection.commit()
        flash('respuesta guardada satisfactoriamente')
        return redirect(url_for('createOptions'))



@app.route('/createValues')
def createValues():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM preguntas WHERE EstadoPreg = "CREADA"')
    data = cur.fetchall()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM opciones')
    data2 = cur2.fetchall()
    if len(data2)==0:
        flash('no hay respuestas registradas por favor registra una')
        return render_template('createOptions.html', preguntas=data, option=0)
    else:
        return render_template('createValues.html', respuestas=data2)

@app.route('/insertValues', methods=['POST'])
def insertValues():
    if request.method == 'POST':
        idopc = request.form['idoption']
        segment = request.form['segmento']
        value = request.form['valor']
        cur = mysql.connection.cursor()  # obtenemos conexion
        cur.execute('INSERT INTO valores_opciones(IdOpciones,CarValor, Valor, FecRegVal, FecHorVal) VALUES (%s,%s,%s,CURDATE(),CURTIME())',
        (idopc, segment, value))  # escrbimos la consulta
        mysql.connection.commit()
        return redirect(url_for('Index'))  # nombre de la ruta


@app.route('/prueba', methods=['GET','POST'])
def Prueba():
    if request.method == 'GET':
        return render_template('createMultiple.html')
    if request.method == "POST":
        k = json.dumps(request.form)
        x = json.loads(k)
        print(type(x))

        print(x)
        keys=list(x.keys())
        print(keys)
        sql=f"""INSERT INTO preguntas (TexPreg,EstadoPreg,TipResp) VALUES ('{x[keys[0]]}','CREADA','{x[keys[1]]}')"""
        for key in keys[2:]:
            sql=f"""
            INSERT INTO opciones (idPreguntas,TextOpc) VALUES ('{x[key[0]]}','{x[key]}')
            """
        return jsonify(request.form)

"""
@app.route('/Math/port', methods=['POST'])
def Math():
    print(request.form)
    if request.method == 'POST':
        # DATOS BD AND FORM
        RT00 = request.form['RT00']
        RT01 = request.form['RT01']
        RT02 = request.form['RT02']
        #RT03 =request.form['RT03']
        RT04 = request.form['RT04']
        RT05 = request.form['RT05']

@app.route('/Math', methods=['POST'])
def Math():
    print(request.form)
    if request.method == 'POST':
        # DATOS BD AND FORM
        RT00 = request.form['RT00']
        RT01 = request.form['RT01']
        RT02 = request.form['RT02']
        #RT03 =request.form['RT03']
        RT04 = request.form['RT04']
        RT05 = request.form['RT05']
        RT06 = request.form['RT06']
        RT07 = request.form['RT07']
        RT08 = request.form['RT08']
        RT09 = request.form['RT09']
        RT10 = request.form['RT10']
        RT11 = request.form['RT11']
        RT12 = request.form['RT12']
        RT13 = request.form['RT13']
        RT14 = request.form['RT14']
        RT15 = request.form['RT15']
        RT16 = request.form['RT16']
        RT17 = request.form['RT17']
        RT18 = request.form['RT18']
        RT19 = request.form['RT19']
        RT20 = request.form['RT20']
        RT21 = request.form['RT21']
        RT22 = request.form['RT22']
        RT23 = request.form['RT23']
        RT24 = request.form['RT24']
        RT25 = request.form['RT25']
        RT26 = request.form['RT26']
        RT27 = request.form['RT27']
        RT28 = request.form['RT28']
        RT29 = request.form['RT29']
        RT30 = request.form['RT30']
        RT31 = request.form['RT31']
        RT32 = request.form['RT32']
        RT33 = request.form['RT33']
        RT34 = request.form['RT34']
        RT35 = request.form['RT35']
        RT36 = request.form['RT36']
        RT37 = request.form['RT37']
        RT38 = request.form['RT38']
        RT39 = request.form['RT39']
        RT40 = request.form['RT40']
        RT41 = request.form['RT41']
        RT42 = request.form['RT42']

        # DATOS MATEMATICOS
        SCc1 = float(request.form['SCc1'])
        SCc2 = float(request.form['SCc2'])
        SCp1 = float(request.form['SCp1'])
        SCp2 = float(request.form['SCp2'])
        SCc3 = float(request.form['SCc3'])
        SCd = float(request.form['SCd'])
        SCcsum = (SCc1+SCc2+SCc3)
        SCpsum = (SCp1+SCp2)
        SCdsum = SCd
        SumaSCc = 3
        SumaSCp = 2
        SumaSCd = 1

        PVc1 = float(request.form['PVc1'])
        PVc2 = float(request.form['PVc2'])
        PVp1 = float(request.form['PVp1'])
        PVp2 = float(request.form['PVp2'])
        PVc3 = float(request.form['PVc3'])
        PVd = float(request.form['PVd'])
        PVcsum = (PVc1+PVc2+PVc3)
        PVpsum = (PVp1+PVp2)
        PVdsum = PVd
        SumaPVc = 3
        SumaPVp = 2
        SumaPVd = 1

        CCp = float(request.form['CCp'])
        CCc = float(request.form['CCc'])
        CCta = float(request.form['CCta'])
        CCtc = float(request.form['CCtc'])
        CCd = float(request.form['CCd'])
        CCpsum = CCp
        CCcsum = CCc
        CCtasum = CCta
        CCtcsum = CCtc
        CCdsum = CCd
        SumaCCp = 1
        SumaCCc = 1
        SumaCCta = 1
        SumaCCtc = 1
        SumaCCd = 1

        ACCta = float(request.form['ACCta'])
        ACCtc = float(request.form['ACCtc'])
        ACCd = float(request.form['ACCd'])
        ACCtasum = ACCta
        ACCtcsum = ACCtc
        ACCdsum = ACCd
        SumaACCta = 1
        SumaACCtc = 1
        SumaACCd = 1

        Ic = float(request.form['Ic'])
        Ip = float(request.form['Ip'])
        Ita = float(request.form['Ita'])
        Itc = float(request.form['Itc'])
        Id = float(request.form['Id'])
        Icsum = Ic
        Ipsum = Ip
        Itasum = Ita
        Itcsum = Itc
        Idsum = Id
        SumaIc = 1
        SumaIp = 1
        SumaIta = 1
        SumaItc = 1
        SumaId = 1

        RECta = float(request.form['RECta'])
        RECtc = float(request.form['RECtc'])
        RECd = float(request.form['RECd'])
        RECtasum = RECta
        RECtcsum = RECtc
        RECdsum = RECd
        SumaRECta = 1
        SumaRECtc = 1
        SumaRECd = 1

        RCc = float(request.form['RCc'])
        RCta = float(request.form['RCta'])
        RCtc = float(request.form['RCtc'])
        RCd = float(request.form['RCd'])
        RCcsum = RCc
        RCtasum = RCta
        RCtcsum = RCtc
        RCdsum = RCd
        SumaRCc = 1
        SumaRCta = 1
        SumaRCtc = 1
        SumaRCd = 1

        ECta1 = float(request.form['ECta1'])
        ECtc1 = float(request.form['ECtc1'])
        ECd1 = float(request.form['ECd1'])

        ECta2 = float(request.form['ECta2'])
        ECtc2 = float(request.form['ECtc2'])
        ECd2 = float(request.form['ECd2'])
        ECtasum = (ECta1+ECta2)
        ECtcsum = (ECtc1+ECtc2)
        ECdsum = (ECd1+ECd2)
        SumaECta = 2
        SumaECtc = 2
        SumaECd = 2

        ACta = float(request.form['ACta'])
        ACtc = float(request.form['ACtc'])
        ACd = float(request.form['ACd'])
        ACtasum = ACta
        ACtcsum = ACtc
        ACdsum = ACd
        SumaACta = 1
        SumaACtc = 1
        SumaACd = 1

        # Formulacion C,P
        C = (PVcsum+SCcsum+Icsum+RCcsum+CCcsum) / \
            (SumaPVc+SumaSCc+SumaIc+SumaRCc+SumaCCc)
        P = (PVpsum+SCpsum+Ipsum+CCpsum)/(SumaPVp+SumaSCp+SumaIp+SumaCCp)
        # Formulacion TA,TC,D
        TA = (RCtasum+CCtasum+Itasum+ECtasum+RECtasum+ACtasum+ACCtasum) / \
            (SumaRCta+SumaCCta+SumaIta+SumaECta+SumaRECta+SumaACta+SumaACCta)
        TC = (RCtcsum+CCtcsum+Itcsum+ECtcsum+RECtcsum+ACtcsum+ACCtcsum) / \
            (SumaRCtc+SumaCCtc+SumaItc+SumaECtc+SumaRECtc+SumaACtc+SumaACCtc)
        TD = (PVdsum+SCdsum+RCdsum+CCdsum+Idsum+ECdsum+RECdsum+ACdsum+ACCdsum) / \
            (SumaPVd+SumaSCd+SumaRCd+SumaCCd +
             SumaId+SumaECd+SumaRECd+SumaACd+SumaACCd)

        # eje y
        if C > P:
            y = 2.5+((C-P)/2)
            print("eje y = "+str(y))
        if P > C:
            y = (P-C)/2
            print("eje y = "+str(y))
        if C == P:
            y = C
            print("eje y = "+str(y))
        # eje x
        if TC > 2.5:
            x = 2.5+((TC-2.5)/2)+(TD/4)
            print("eje x = "+str(x))
        if TC <= 2.5:
            x = (TA/4)+(TD/4)
            print("eje x = "+str(x))

        return render_template('main.html', ejey=y, ejex=x)
"""

@app.route('/ViewForm')
def ViewForm():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM preguntas')
    data = cur.fetchall()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM opciones')
    data2 = cur2.fetchall()
    cur3 = mysql.connection.cursor()
    cur3.execute('SELECT * FROM valores_opciones')
    data3 = cur3.fetchall()
    if (len(data) == 0):
        flash('Aun no hay datos guardados')
        return render_template('ViewForm.html', preguntas=data, respuestas=data2, valores=data3)
    else:
        return render_template('ViewForm.html', preguntas=data, respuestas=data2, valores=data3)



if __name__ == '__main__':
    app.run(port=3000, debug=True)  # PUERTO Y MODO PRUEBAS

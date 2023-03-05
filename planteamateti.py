#from flask import Flask, render_template, request, redirect, url_for, flash, session
#from flask_mysqldb import MySQL
#from datetime import datetime, date, time

#app = Flask(__name__)

#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '1098741116'
#app.config['MYSQL_DB'] = 'software1'


#ahora vamos a inicializar una sesion es decir datos que guarda nuestro servidor para luego poder reutilizarlos
#en este caso lo vamos a guardar dentro de la memoria de la aplicacion
#con secret_key le decimos como va a ir protegida nuestra sesion
#app.secret_key = 'mysecretkey'

#mysql = MySQL(app)
#cada vez que un usuario entre a nuestra ruta principal vamos a devolverle algo es esta linea:

#respuestas cuestionario
#Frente a la satisfacción de los clientes con la promesa de valor de la empresa, usted
PVc1 = 1.75
PVc2 = 2.25
PVp1 = 1.75
PVp2 = 1.75
PVc3 = 2.25
PVd = 1.75
PVcsum = (PVc1+PVc2+PVc3)
PVpsum = (PVp1+PVp2)
PVdsum = PVd
SumaPVc = 3
SumaPVp = 2
SumaPVd = 1

#Al caracterizar a sus clientes usted utiliza
SCc1 = 1.75
SCc2 = 2.25
SCp1 = 1.75
SCp2 = 1.75
SCc3 = 2.25
SCd = 1.75
SCcsum = (SCc1+SCc2+SCc3)
SCpsum = (SCp1+SCp2)
SCdsum = SCd
SumaSCc = 3
SumaSCp = 2
SumaSCd = 1

#Frente a la satisfacción de los clientes con la promesa de valor de la empresa, usted
RCc = 1.75
RCta = 2.25
RCtc = 1.75
RCd = 1.75
RCcsum = RCc
RCtasum = RCta
RCtcsum = RCtc
RCdsum = RCd
SumaRCc = 1
SumaRCta = 1
SumaRCtc = 1
SumaRCd = 1

#Con respecto a los canales de comunicación con los clientes
CCp = 1.75
CCc = 2.25
CCta = 1.75
CCtc = 1.75
CCd = 1.75
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

#Frente a las alianzas (señalar las que aplique)
ACta = 2.5
ACtc = 2.5
ACd = 2.75
ACtasum = ACta
ACtcsum = ACtc
ACdsum = ACd
SumaACta = 1
SumaACtc = 1
SumaACd = 1

#Frente a la identificación de requerimientos, necesidades o nuevas tendencias de su mercado
ACCta = 3
ACCtc = 3
ACCd = 3
ACCtasum = ACCta
ACCtcsum = ACCtc
ACCdsum = ACCd
SumaACCta = 1
SumaACCtc = 1
SumaACCd = 1

#Frente a la forma de pago para sus clientes (Seleccione las que tiene disponibles)
RECta = 1.75
RECtc = 1.75
RECd = 1.75
RECtasum = RECta
RECtcsum = RECtc
RECdsum = RECd
SumaRECta = 1
SumaRECtc = 1
SumaRECd = 1

#Con respecto a su modelo de ingresos
Ic = 2.5
Ip = 2.5
Ita = 2.5
Itc = 2.5
Id = 2.5
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

#Con respecto a la información financiera
ECta1 = 0.5
ECtc1 = 0.5
ECd1 = 0.5
ECta2 = 1.75
ECtc2 = 1.75
ECd2 = 1.75
ECtasum = (ECta1+ECta2)
ECtcsum = (ECtc1+ECtc2)
ECdsum = (ECd1+ECd2)
SumaECta = 2
SumaECtc = 2
SumaECd = 2

#Formulacion C,P
C = (PVcsum+SCcsum+Icsum+RCcsum+CCcsum)/(SumaPVc+SumaSCc+SumaIc+SumaRCc+SumaCCc)
P = (PVpsum+SCpsum+Ipsum+CCpsum)/(SumaPVp+SumaSCp+SumaIp+SumaCCp)
#Formulacion TA,TC,D
TA = (RCtasum+CCtasum+Itasum+ECtasum+RECtasum+ACtasum+ACCtasum)/(SumaRCta+SumaCCta+SumaIta+SumaECta+SumaRECta+SumaACta+SumaACCta)
TC = (RCtcsum+CCtcsum+Itcsum+ECtcsum+RECtcsum+ACtcsum+ACCtcsum)/(SumaRCtc+SumaCCtc+SumaItc+SumaECtc+SumaRECtc+SumaACtc+SumaACCtc)
TD = (PVdsum+SCdsum+RCdsum+CCdsum+Idsum+ECdsum+RECdsum+ACdsum+ACCdsum)/(SumaPVd+SumaSCd+SumaRCd+SumaCCd+SumaId+SumaECd+SumaRECd+SumaACd+SumaACCd)

#eje y
if C>P:
    k = 2.5+((C-P)/2)
    print("eje y = "+str(k))
if P>C:
    k = (P-C)/2
    print("eje y = "+str(k))
if C==P:
    k = C
    print("eje y = "+str(k))
#eje x
if TC > 2.5:
    t = 2.5+((TC-2.5)/2)+(TD/4)
    print("eje x = "+str(t))
if TC <= 2.5:
    t = (TA/4)+(TD/4)
    print("eje x = "+str(t))
    

#activar el debug del servidor
#if __name__ == '__main__':
    #le damos el puerto y debug
#    app.run(port = 5500, debug = True)
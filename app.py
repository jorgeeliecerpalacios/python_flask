# flash nos sirve para enviar errores 
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)

# configuracion base de datos
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'contactos' 
mysql = MySQL(app)

# settings, inicializamos una session la cual son los datos que guarda nuestra aplicacion que luego podemos utilizarlos ya quelos podemos guardar como cookies, memoria del navegador o en memoria del servidor, aca lo guardaremos en memoria de la aplicacion
# este secret_key es para saber como va a ir protegida nuestra session
app.secret_key = 'mysecretkey'


# rutas
@app.route('/')
def Index():
    # aqui vamos hacer la consulta a la base de datos 
    cur = mysql.connection.cursor()
    # aca hacemos la consulta 
    cur.execute('SELECT * FROM contacts')
    # para obtener todos los datos le ponemos fetchall
    data = cur.fetchall()
    # aca enviamos los datos atravez del contexto
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def Add():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        # esta es la coneccion 
        cur = mysql.connection.cursor()
        # se escribe la consulta de los datos que se van a insertar en la base de datos 
        # despues del INSERT INTO el nombre que se escribe es el nombre de la tabla mas no el de la base de datos 
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
        # aca se ejecuta la consulta
        mysql.connection.commit()
        # aqui insertamos flash para enviar el texto que queremos plasmar 
        flash('Contacto guardado exitosamente')
        #  con el redirect(url_for('')) lo que hacemos es redireccionar hacia la pagina que se encuentra dentro del parametro de url_for
        return redirect(url_for('Index'))

@app.route('/edit')
def Edit():
    return 'hola Edit'

# para que me funcione la ruta del delete debo darle el parametro que esta recibe extra que en este caso es el id  y se lo mandamos con la etiqueta que se encuentra al lado del /
@app.route('/delete/<string:id>')
def Borrar(id):
    # aqui vamos hacer la consulta a la base de datos 
    cur = mysql.connection.cursor()
    # se escribe la consulta de la accion a realizar  
    # con el format le damos formato tipo string para que se ejecute en la ruta dicha operacion
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto eliminado correctamente')
    return redirect(url_for('Index'))

# arranque 
if __name__ == '__main__':
    app.run(port = 8000, debug = True)
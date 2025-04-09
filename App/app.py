import pandas as pd
from flask import Flask, render_template, request, jsonify, redirect , url_for
import joblib
from flask_mysqldb import MySQL

# Cargar el modelo guardado desde el archivo
modelo_guardado = 'modelo.h5'
modelo_cargado = joblib.load(modelo_guardado)

# Crear la aplicación Flask
app = Flask(__name__)


# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'agriculturas'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Inicializar la extensión MySQL
mysql = MySQL(app)

# Variable global para almacenar los datos de usuario
datos_usuario = {}

# Función para convertir los valores de opción múltiple a etiquetas ("Si" o "No")
def convertir_opcion_multiple(valor):
    opciones = {
        '1': 'Si',
        '2': 'No',
        # Agregar aquí las demás opciones
    }
    return opciones[valor]


def convertir_opcion_multiple2(valor):
    opciones = {
        "1": "Sequías",
        "2": "Plagas",
        "3": "Inundación",
        "4": "Semillas",
        "5": "Prácticas inadecuadas",
        "6": "Edad de la Plantación",
        "7": "Otra"
    }
    return opciones[valor]

# Ruta principal que muestra la interfaz gráfica
@app.route('/')
def index():
    return render_template('login.html')

# Ruta para recibir los datos ingresados por el usuario y devolver la predicción en /predict
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        datos = request.form

    global datos_usuario
    # Acceder a los datos almacenados en la variable global
    nombre = datos_usuario.get('nombre', '')
    apellido = datos_usuario.get('apellido', '')
    ciudad = datos_usuario.get('ciudad', '')
    provincia = datos_usuario.get('provincia', '')
    canton = datos_usuario.get('canton', '')
    recinto = datos_usuario.get('recinto', '')
    nombre_finca = datos_usuario.get('nombre_finca', '')
    parroquia = datos_usuario.get('parroquia', '')
    # Agrega aquí los demás campos de usuario que estás recolectando

    # Resto del código para obtener los otros datos del formulario
    ct_prepa_suelo = int(datos['ct_prepa_suelo'])
    ct_k510ha = float(datos['ct_k510ha'])
    ct_k511ha = float(datos['ct_k511ha'])
    ct_afecta_prod = int(datos['ct_afecta_prod'])
    ct_riego = int(datos['ct_riego'])
    su_fertilizada = float(datos['su_fertilizada'])
    ct_fqui = int(datos['ct_fqui'])
    ct_fqui_npk = float(datos['ct_fqui_npk'])
    ct_pqui = int(datos['ct_pqui'])
    su_plaguicidas = float(datos['su_plaguicidas'])
    ventas = float(datos['ventas'])

    # Realizar la predicción con el modelo cargado
    prediccion = modelo_cargado.predict([[ct_prepa_suelo, ct_k510ha, ct_k511ha, ct_afecta_prod, ct_riego,
                                          su_fertilizada, ct_fqui, ct_fqui_npk, ct_pqui, su_plaguicidas, ventas]])
    # Guardar los datos del usuario y el resultado de la predicción en la base de datos
    ct_prepa_suelo = convertir_opcion_multiple(datos['ct_prepa_suelo'])
    ct_afecta_prod = convertir_opcion_multiple2(datos['ct_afecta_prod'])
    ct_riego = convertir_opcion_multiple(datos['ct_riego'])
    ct_fqui = convertir_opcion_multiple(datos['ct_fqui'])
    ct_pqui = convertir_opcion_multiple(datos['ct_pqui'])

    # Almacenar los datos del usuario y el resultado de la predicción en la base de datos
    cur = mysql.connection.cursor()
    cur.execute(
        'INSERT INTO usuarios (nombre, apellido, ciudad, provincia, canton, recinto, nombre_finca, parroquia, ct_prepa_suelo, ct_k510ha, ct_k511ha, ct_afecta_prod, ct_riego, su_fertilizada, ct_fqui, ct_fqui_npk, ct_pqui, su_plaguicidas, ventas, resultado_prediccion) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (nombre, apellido, ciudad, provincia, canton, recinto, nombre_finca, parroquia, ct_prepa_suelo, ct_k510ha, ct_k511ha, ct_afecta_prod, ct_riego,
         su_fertilizada, ct_fqui, ct_fqui_npk, ct_pqui, su_plaguicidas, ventas, prediccion[0]))
    mysql.connection.commit()
    cur.close()

    # Devolver el resultado de la predicción en formato JSON
    return jsonify({'prediccion': prediccion[0]})

# Ruta para recibir los datos ingresados por el usuario en /datos
@app.route('/datos', methods=['POST'])
def guardar_datos():
    if request.method == 'POST':
        datos = request.form

    global datos_usuario
    datos_usuario['nombre'] = datos['nombre']
    datos_usuario['apellido'] = datos['apellido']
    datos_usuario['ciudad'] = datos['ciudad']
    datos_usuario['provincia'] = datos['provincia']
    datos_usuario['canton'] = datos['canton']
    datos_usuario['recinto'] = datos['recinto']
    datos_usuario['nombre_finca'] = datos['nombre_finca']
    datos_usuario['parroquia'] = datos['parroquia']
    # Agrega aquí los demás campos de usuario que estás recolectando

    # Redirige al usuario a la página index.html
    return redirect('/index')
@app.route('/verificar', methods=['GET', 'POST'])
def verificar():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'agricultura':
            return redirect('/admin')
        else:
            return "Contraseña incorrecta"
    return render_template('verificar.html')

# Ruta para la página de datos.html (para el botón "Usuario")
@app.route('/usuario')
def usuario():
    return render_template('datos.html')

# Ruta para redireccionar a la página principal (para el botón "Administrador")
@app.route('/index')
def redireccionar():
    return render_template('index.html')

@app.route('/resultados')
def resultado():
    usuario = obtener_usuario()
    return render_template('resultados.html', usuario=usuario)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
def admin():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios')
        data = cur.fetchall()
        cur.close()

    return render_template('admin.html', data=data)

@app.route('/get_user/<int:user_id>')
def get_user(user_id):
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE id = %s', (user_id,))
        user_data = cur.fetchone()
        cur.close()

    return jsonify(user_data)


# Ruta para editar los datos de un usuario específico
@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    if request.method == 'POST':
        datos = request.form
        nombre = datos['nombre']
        apellido = datos['apellido']
        ciudad = datos['ciudad']
        provincia = datos['provincia']
        recinto = datos['recinto']
        nombre_finca = datos['nombre_finca']
        canton = datos['canton']
        parroquia = datos['parroquia']
        ct_prepa_suelo = datos['ct_prepa_suelo']
        ct_k510ha = float(datos['ct_k510ha'])
        ct_k511ha = float(datos['ct_k511ha'])
        ct_afecta_prod = datos['ct_afecta_prod']
        ct_riego = datos['ct_riego']
        su_fertilizada = float(datos['su_fertilizada'])
        ct_fqui = datos['ct_fqui']
        ct_fqui_npk = float(datos['ct_fqui_npk'])
        ct_pqui = datos['ct_pqui']
        su_plaguicidas = float(datos['su_plaguicidas'])
        ventas = float(datos['ventas'])
        resultado_prediccion = float(datos['resultado_prediccion'])
        comentario = (datos['comentario'])
        # Agregar aquí los demás campos de usuario que estás recolectando

        # Actualizar los datos en la tabla "usuarios" de la base de datos
        cur = mysql.connection.cursor()
        cur.execute(
            'UPDATE usuarios SET nombre=%s, apellido=%s, ciudad=%s, provincia=%s, recinto=%s, nombre_finca=%s, canton=%s, parroquia=%s, ct_prepa_suelo=%s, ct_k510ha=%s, ct_k511ha=%s, ct_afecta_prod=%s, ct_riego=%s, su_fertilizada=%s, ct_fqui=%s, ct_fqui_npk=%s, ct_pqui=%s, su_plaguicidas=%s, ventas=%s, resultado_prediccion=%s,comentario=%s WHERE id=%s',
            (nombre, apellido, ciudad, provincia, recinto, nombre_finca, canton, parroquia, ct_prepa_suelo, ct_k510ha, ct_k511ha, ct_afecta_prod,
            ct_riego, su_fertilizada, ct_fqui, ct_fqui_npk, ct_pqui, su_plaguicidas, ventas, resultado_prediccion,comentario,id))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Usuario actualizado correctamente'}), 200


# Ruta para eliminar los datos de un usuario específico
@app.route('/eliminar/<int:id>')
def eliminar(id):
    # Eliminar los datos del usuario de la tabla "usuarios" de la base de datos
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE id=%s', (id,))
    mysql.connection.commit()
    cur.close()

    return redirect('/admin')

# Ruta para agregar nuevos datos de usuario
@app.route('/agregar', methods=['GET','POST'])
def agregar():
    if request.method == 'POST':
        datos = request.form
        nombre = datos['nombre']
        apellido = datos['apellido']
        ciudad = datos['ciudad']
        provincia = datos['provincia']
        recinto = datos['recinto']
        nombre_finca = datos['nombre_finca']
        canton = datos['canton']
        parroquia = datos['parroquia']
        ct_prepa_suelo = datos['ct_prepa_suelo']
        ct_k510ha = float(datos['ct_k510ha'])
        ct_k511ha = float(datos['ct_k511ha'])
        ct_afecta_prod = datos['ct_afecta_prod']
        ct_riego = datos['ct_riego']
        su_fertilizada = float(datos['su_fertilizada'])
        ct_fqui = datos['ct_fqui']
        ct_fqui_npk = float(datos['ct_fqui_npk'])
        ct_pqui = datos['ct_pqui']
        su_plaguicidas = float(datos['su_plaguicidas'])
        ventas = float(datos['ventas'])
        resultado_prediccion = float(datos['resultado_prediccion'])
        comentario = (datos['comentario'])


        #Transformas a floats:
        # Guardar los datos del usuario y el resultado de la predicción en la base de datos
        ct_prepa_suelo = convertir_opcion_multiple(datos['ct_prepa_suelo'])
        ct_afecta_prod = convertir_opcion_multiple2(datos['ct_afecta_prod'])
        ct_riego = convertir_opcion_multiple(datos['ct_riego'])
        ct_fqui = convertir_opcion_multiple(datos['ct_fqui'])
        ct_pqui = convertir_opcion_multiple(datos['ct_pqui'])

        # Insertar nuevos datos en la tabla "usuarios" de la base de datos
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO usuarios (nombre, apellido, ciudad, provincia, canton, recinto, nombre_finca, parroquia, ct_prepa_suelo, ct_k510ha, ct_k511ha, ct_afecta_prod, ct_riego, su_fertilizada, ct_fqui, ct_fqui_npk, ct_pqui, su_plaguicidas, ventas, resultado_prediccion, comentario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (nombre, apellido, ciudad, provincia, canton, recinto, nombre_finca, parroquia, ct_prepa_suelo, ct_k510ha,
             ct_k511ha, ct_afecta_prod, ct_riego,
             su_fertilizada, ct_fqui, ct_fqui_npk, ct_pqui, su_plaguicidas, ventas, resultado_prediccion,comentario))
        mysql.connection.commit()
        cur.close()

        return redirect('/admin')
    else:
        return render_template('agregar.html')

@app.route('/obtener_usuario', methods=['GET'])
def obtener_usuario():
    if request.method == 'GET':
        usuario_id = request.args.get('id')
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE id=%s', (usuario_id,))
        data = cur.fetchone()
        cur.close()
        return jsonify(data)


@app.route('/enviar_comentario', methods=['POST'])
def enviar_comentario():
    if request.method == 'POST':
        data = request.get_json()
        comentario = data.get('comentario')

        try:
            # Obtener el último ID de la tabla usuarios
            cur = mysql.connection.cursor()
            cur.execute("SELECT id FROM usuarios ORDER BY id DESC LIMIT 1")
            ultimo_id = cur.fetchone()
            cur.close()

            if ultimo_id:
                usuario_id = ultimo_id['id']

                # Actualizar la fila correspondiente en la base de datos
                cur = mysql.connection.cursor()
                cur.execute('UPDATE usuarios SET comentario = %s WHERE id = %s', (comentario, usuario_id))
                mysql.connection.commit()
                cur.close()

                # Devolver una respuesta al cliente
                return jsonify({'message': 'Comentario enviado exitosamente'})
            else:
                return jsonify({'error': 'No se pudo obtener el último ID'})

        except Exception as e:
            print(e)
            return jsonify({'error': 'Error al actualizar el comentario'})

    return jsonify({'error': 'Método no permitido'})
if __name__ == '__main__':
    app.run(debug=True)

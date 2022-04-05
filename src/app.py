from logging import exception
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config

app=Flask(__name__)

conexion = MySQL(app)

#Función lista de cursos

@app.route('/cursos')
def listar_cursos():
    try:
        cursor=conexion.connection.cursor()
        sql = "SELECT codigo, nombre, creditos FROM cursos"
        cursor.execute(sql)
        datos=cursor.fetchall()
        cursos=[]
        for fila in datos:
            curso= {'codigo': fila[0], 'nombre':fila[1], 'creditos':fila[2]}
            cursos.append(curso)

        return jsonify({'cursos': cursos, 'mensaje':"Estos son los cursos listados"})

    except exception as e:
        return jsonify({'mensaje': "error al listar"})

@app.route('/cursos/<codigo>', methods =['GET'])
def leer_curso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT codigo, nombre, creditos FROM cursos WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos!= None:
            curso = {'codigo':datos[0], 'nombre':datos[1], 'creditos':datos[2]}
            return jsonify({'curso':curso,'mensaje':"Curso Encontrado."})
        else:
            return jsonify({'mensaje':"Curso no encontrado."})

    except Exception as e:
        return jsonify({'mensaje':"Error"})

@app.route('/cursos', methods =['POST'])
def registrar_curso():
    try:
        cursor=conexion.connection.cursor()
        sql="""INSERT INTO cursos(codigo, nombre, creditos) VALUES ('{0}','{1}',{2})""".format(request.json['codigo'],request.json['nombre'],request.json['creditos'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify ({'mensaje': "curso registrado."})
    except Exception as e:
        return jsonify({'mensaje':"Error"})

@app.route('/cursos/<codigo>',methods =['PUT'])
def modificar_curso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql="UPDATE cursos SET nombre = '{0}', creditos = '{1}' WHERE codigo = '{2}'".format(request.json['nombre'], request.json['creditos'], codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return({'mensaje':"Curso actualizado."})
    except Exception as e:
        return jsonify({'mensaje':"Error"})

@app.route('/cursos/<codigo>',methods =['DELETE'])
def eliminar_curso(codigo):
    try:
        cursor=conexion.connection.cursor()
        sql=" DELETE FROM cursos WHERE codigo = '{0}'".format(codigo)
        cursor.execute(sql)
        conexion.connection.commit()
        return({'mensaje':"Curso eliminado."})
    except Exception as e:
        return jsonify({'mensaje':"Error"})


def no_encontrada(error):
    return "<h1> La página no existe </h2>",404


if __name__=='__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,no_encontrada)
    app.run()
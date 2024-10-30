# import sqlite3
#
# # Conexión a una base de datos SQLite
# conn = sqlite3.connect("example.db")
# cursor = conn.cursor()
#
#
# # Función segura contra SQL Injection
# def obtener_usuario_seguro(usuario_id: str) -> list:
#     query = "SELECT * FROM usuarios WHERE id = ?"
#     cursor.execute(query, (usuario_id,))
#
#     return cursor.fetchall()
#
#
# # Ingreso de usuario
# user_input = "1 OR 1=1"
#
# # Esto ya no permitirá la inyección SQL
# resultados = obtener_usuario_seguro(user_input)
# print(resultados)

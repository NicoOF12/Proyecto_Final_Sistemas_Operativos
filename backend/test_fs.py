from models.filesystem.sistema_de_archivos import SistemaArchivos

fs = SistemaArchivos()

print(fs.ls("/"))
print(fs.mkdir("docs"))
print(fs.ls("/"))
print(fs.cd("/docs"))
print(fs.crear_archivo("notas.txt", "Hola mundo"))
print(fs.leer_archivo("notas.txt"))
print(fs.escribir_archivo("notas.txt", "Nuevo contenido"))
print(fs.leer_archivo("notas.txt"))

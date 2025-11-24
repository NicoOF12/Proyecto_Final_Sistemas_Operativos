from models.filesystem.sistema_de_archivos import SistemaArchivos

fs = SistemaArchivos()
print("Usuarios disponibles:", fs.listar_usuarios())
print("Usuario actual:", fs.usuario_actual)

# 1. su a usuario1 y crear archivo privado
print("\n--> su usuario1")
print(fs.su("usuario1"))
print("mkdir /home/usuario1/docs:", fs.mkdir("/home/usuario1/docs"))
print("create secret 600:", fs.crear_archivo("/home/usuario1/docs/secret.txt", "contenido secreto", permisos="600"))

# 2. su usuario2 y tratar de leer -> DENEGADO
print("\n--> su usuario2")
print(fs.su("usuario2"))
print("read secret as usuario2:", fs.read("/home/usuario1/docs/secret.txt"))

# 3. su usuario1 y leer -> OK
print("\n--> su usuario1")
print(fs.su("usuario1"))
print("read secret as usuario1:", fs.read("/home/usuario1/docs/secret.txt"))

# 4. su root y chmod 644
print("\n--> su root")
print(fs.su("root"))
print("chmod to 644:", fs.chmod("/home/usuario1/docs/secret.txt", "644"))

# 5. su usuario2 y leer -> OK ahora
print("\n--> su usuario2")
print(fs.su("usuario2"))
print("read secret as usuario2:", fs.read("/home/usuario1/docs/secret.txt"))

# 6. probar rm por usuario2 en home/usuario1 -> denegado
print("\n--> intentar rm por usuario2 en /home/usuario1/docs/secret.txt")
print(fs.rm("/home/usuario1/docs/secret.txt"))

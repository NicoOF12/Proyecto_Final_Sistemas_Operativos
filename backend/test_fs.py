from models.filesystem.sistema_de_archivos import SistemaArchivos

fs = SistemaArchivos()

print("=" * 60)
print("TEST DE PERMISOS DEL SISTEMA DE ARCHIVOS")
print("=" * 60)

# 1. Verificar estructura inicial
print("\n1. Estructura inicial como ROOT:")
print(f"   Usuario actual: {fs.usuario_actual.nombre}")
print(f"   Path actual: {fs.pwd()}")
print(f"   Contenido de /:", fs.ls("/"))

# 2. Root puede crear en /
print("\n2. ROOT crea directorio en /:")
result = fs.mkdir("/test-root", permisos="755")
print(f"   {result}")

# 3. Cambiar a usuario1
print("\n3. Cambiar a usuario1:")
print(f"   {fs.su('usuario1')}")
print(f"   Usuario actual: {fs.usuario_actual.nombre}")

# 4. usuario1 intenta crear en / (debería funcionar con permisos 777)
print("\n4. usuario1 crea directorio en /:")
result = fs.mkdir("/test-usuario1", permisos="755")
print(f"   {result}")

# 5. usuario1 crea archivo en /
print("\n5. usuario1 crea archivo en /:")
result = fs.crear_archivo("/archivo-usuario1.txt", "contenido test", permisos="644")
print(f"   {result}")

# 6. Verificar contenido de /
print("\n6. Contenido de / después de las operaciones:")
result = fs.ls("/")
print(f"   Directorios: {[d['nombre'] for d in result.get('directorios', [])]}")
print(f"   Archivos: {[a['nombre'] for a in result.get('archivos', [])]}")

# 7. usuario1 en su home
print("\n7. usuario1 va a su directorio home:")
fs.cd("/home/usuario1")
print(f"   Path actual: {fs.pwd()}")

# 8. usuario1 crea en su home
print("\n8. usuario1 crea directorio en su home:")
result = fs.mkdir("mis-docs", permisos="700")
print(f"   {result}")

# 9. usuario1 crea archivo en su home
print("\n9. usuario1 crea archivo en su home:")
result = fs.crear_archivo("nota.txt", "mi nota privada", permisos="600")
print(f"   {result}")

# 10. Ver contenido de /home/usuario1
print("\n10. Contenido de /home/usuario1:")
result = fs.ls(".")
print(f"   Directorios: {[d['nombre'] for d in result.get('directorios', [])]}")
print(f"   Archivos: {[a['nombre'] for a in result.get('archivos', [])]}")

# 11. Cambiar a usuario2
print("\n11. Cambiar a usuario2:")
fs.su("usuario2")
print(f"   Usuario actual: {fs.usuario_actual.nombre}")

# 12. usuario2 intenta leer archivo de usuario1
print("\n12. usuario2 intenta leer nota.txt de usuario1 (debería fallar):")
result = fs.read("/home/usuario1/nota.txt")
print(f"   {result}")

# 13. usuario2 crea en su home
print("\n13. usuario2 va a su home y crea archivo:")
fs.cd("/home/usuario2")
result = fs.crear_archivo("publico.txt", "archivo publico", permisos="644")
print(f"   {result}")

print("\n" + "=" * 60)
print("TEST COMPLETADO")
print("=" * 60)
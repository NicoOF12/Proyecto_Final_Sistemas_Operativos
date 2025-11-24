"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Folder, File, FolderPlus, FilePlus, Trash2, User, Shield, Terminal } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

const API_BASE = "http://localhost:8000"

export default function FileSystem() {
  const [currentPath, setCurrentPath] = useState("/")
  const [currentUser, setCurrentUser] = useState("root")
  const [files, setFiles] = useState<any[]>([])
  const [users, setUsers] = useState<string[]>([])
  const { toast } = useToast()

  // Form states
  const [newDir, setNewDir] = useState({ name: "", permisos: "755" })
  const [newFile, setNewFile] = useState({ name: "", contenido: "", permisos: "644" })
  const [selectedFile, setSelectedFile] = useState<string>("")

  useEffect(() => {
    fetchPwd()
    fetchUsers()
    fetchFiles()
  }, [])

  const fetchPwd = async () => {
    try {
      const response = await fetch(`${API_BASE}/fs/pwd`)
      const data = await response.json()
      setCurrentPath(data.pwd)
    } catch (error) {
      console.error("Error fetching pwd:", error)
    }
  }

  const fetchUsers = async () => {
    try {
      const response = await fetch(`${API_BASE}/fs/users`)
      const data = await response.json()
      setUsers(data.users)
    } catch (error) {
      console.error("Error fetching users:", error)
    }
  }

  const fetchFiles = async () => {
    try {
      const response = await fetch(`${API_BASE}/fs/ls?ruta=.`)
      const data = await response.json()
      setFiles(data.contenido || [])
    } catch (error) {
      console.error("Error fetching files:", error)
    }
  }

  const handleSwitchUser = async (username: string) => {
    try {
      const response = await fetch(`${API_BASE}/fs/su?username=${username}`, {
        method: "POST",
      })
      if (response.ok) {
        setCurrentUser(username)
        toast({
          title: "Usuario cambiado",
          description: `Sesión iniciada como ${username}`,
        })
        await fetchFiles()
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo cambiar de usuario",
        variant: "destructive",
      })
    }
  }

  const handleCreateDir = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await fetch(`${API_BASE}/fs/mkdir?ruta=${newDir.name}&permisos=${newDir.permisos}`, {
        method: "POST",
      })
      if (response.ok) {
        toast({
          title: "Directorio creado",
          description: `${newDir.name} creado exitosamente`,
        })
        setNewDir({ name: "", permisos: "755" })
        await fetchFiles()
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo crear el directorio",
        variant: "destructive",
      })
    }
  }

  const handleCreateFile = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await fetch(
        `${API_BASE}/fs/create?ruta=${newFile.name}&contenido=${encodeURIComponent(newFile.contenido)}&permisos=${newFile.permisos}`,
        { method: "POST" },
      )
      if (response.ok) {
        toast({
          title: "Archivo creado",
          description: `${newFile.name} creado exitosamente`,
        })
        setNewFile({ name: "", contenido: "", permisos: "644" })
        await fetchFiles()
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo crear el archivo",
        variant: "destructive",
      })
    }
  }

  const handleDeleteItem = async (path: string) => {
    try {
      const response = await fetch(`${API_BASE}/fs/rm?ruta=${path}`, {
        method: "POST",
      })
      if (response.ok) {
        toast({
          title: "Eliminado",
          description: "Elemento eliminado exitosamente",
        })
        await fetchFiles()
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo eliminar",
        variant: "destructive",
      })
    }
  }

  return (
    <div className="grid lg:grid-cols-3 gap-6">
      {/* Left Column - File Operations */}
      <div className="lg:col-span-2 space-y-4">
        {/* Terminal Info */}
        <Card className="border-border bg-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Terminal className="w-5 h-5" />
              Terminal
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="gap-1">
                <User className="w-3 h-3" />
                {currentUser}
              </Badge>
              <span className="text-muted-foreground">@</span>
              <span className="font-mono text-sm text-primary">{currentPath}</span>
            </div>

            <Separator />

            <div className="flex flex-wrap gap-2">
              {users.map((user) => (
                <Button
                  key={user}
                  variant={user === currentUser ? "default" : "outline"}
                  size="sm"
                  onClick={() => handleSwitchUser(user)}
                  className="gap-1"
                >
                  <User className="w-3 h-3" />
                  {user}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Files List */}
        <Card className="border-border bg-card">
          <CardHeader>
            <CardTitle>Archivos y Directorios</CardTitle>
            <CardDescription>Contenido del directorio actual</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {files.length > 0 ? (
                files.map((item, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-3 rounded-lg border border-border bg-secondary/30 hover:bg-secondary/50 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      {item.tipo === "directorio" ? (
                        <Folder className="w-5 h-5 text-primary" />
                      ) : (
                        <File className="w-5 h-5 text-muted-foreground" />
                      )}
                      <div>
                        <p className="font-medium">{item.nombre}</p>
                        <div className="flex items-center gap-2 text-xs text-muted-foreground">
                          <Shield className="w-3 h-3" />
                          {item.permisos}
                          <span>•</span>
                          <User className="w-3 h-3" />
                          {item.propietario}
                        </div>
                      </div>
                    </div>
                    <Button variant="ghost" size="icon" onClick={() => handleDeleteItem(item.nombre)}>
                      <Trash2 className="w-4 h-4 text-destructive" />
                    </Button>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  <Folder className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>Directorio vacío</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Right Column - Create Forms */}
      <div className="space-y-4">
        {/* Create Directory */}
        <Card className="border-border bg-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FolderPlus className="w-5 h-5" />
              Crear Directorio
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleCreateDir} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="dirname">Nombre</Label>
                <Input
                  id="dirname"
                  placeholder="mi-directorio"
                  value={newDir.name}
                  onChange={(e) => setNewDir({ ...newDir, name: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="dirpermisos">Permisos</Label>
                <Input
                  id="dirpermisos"
                  placeholder="755"
                  value={newDir.permisos}
                  onChange={(e) => setNewDir({ ...newDir, permisos: e.target.value })}
                />
              </div>
              <Button type="submit" className="w-full">
                <FolderPlus className="w-4 h-4 mr-2" />
                Crear Directorio
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Create File */}
        <Card className="border-border bg-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FilePlus className="w-5 h-5" />
              Crear Archivo
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleCreateFile} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="filename">Nombre</Label>
                <Input
                  id="filename"
                  placeholder="archivo.txt"
                  value={newFile.name}
                  onChange={(e) => setNewFile({ ...newFile, name: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="filecontent">Contenido</Label>
                <Textarea
                  id="filecontent"
                  placeholder="Contenido del archivo..."
                  value={newFile.contenido}
                  onChange={(e) => setNewFile({ ...newFile, contenido: e.target.value })}
                  rows={4}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="filepermisos">Permisos</Label>
                <Input
                  id="filepermisos"
                  placeholder="644"
                  value={newFile.permisos}
                  onChange={(e) => setNewFile({ ...newFile, permisos: e.target.value })}
                />
              </div>
              <Button type="submit" className="w-full">
                <FilePlus className="w-4 h-4 mr-2" />
                Crear Archivo
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

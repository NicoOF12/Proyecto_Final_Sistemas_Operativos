"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Play, TrendingUp, CheckCircle2 } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

const API_BASE = "http://localhost:8000"

interface ProcessResult {
  pid: number
  tiempo_espera: number
  tiempo_finalizacion: number
  tiempo_retorno: number
  rafaga_cpu: number
  tiempo_llegada: number
}

export default function SchedulerControl({ onExecute }: { onExecute: () => void }) {
  const [results, setResults] = useState<ProcessResult[]>([])
  const [algorithm, setAlgorithm] = useState<string>("")
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()

  const executeAlgorithm = async (algo: string) => {
    setLoading(true)
    setAlgorithm(algo)

    try {
      const response = await fetch(`${API_BASE}/planificar/${algo}`, {
        method: "POST",
      })

      if (response.ok) {
        const data = await response.json()
        setResults(data)
        toast({
          title: "Algoritmo ejecutado",
          description: `${algo.toUpperCase()} ejecutado exitosamente`,
        })
        onExecute()
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo ejecutar el algoritmo",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  const calculateMetrics = () => {
    if (results.length === 0) return null

    const avgWaitTime = results.reduce((sum, p) => sum + p.tiempo_espera, 0) / results.length
    const avgTurnaround = results.reduce((sum, p) => sum + p.tiempo_retorno, 0) / results.length

    return { avgWaitTime, avgTurnaround }
  }

  const metrics = calculateMetrics()

  return (
    <div className="space-y-4">
      {/* Algorithm Selection Card */}
      <Card className="border-border bg-card">
        <CardHeader>
          <CardTitle>Algoritmos de Planificación</CardTitle>
          <CardDescription>Ejecutar algoritmos sobre los procesos en cola de listos</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <Button
            onClick={() => executeAlgorithm("fcfs")}
            disabled={loading}
            className="w-full justify-start gap-2"
            variant={algorithm === "fcfs" ? "default" : "outline"}
          >
            <Play className="w-4 h-4" />
            First Come First Served (FCFS)
          </Button>

          <Button
            onClick={() => executeAlgorithm("sjf")}
            disabled={loading}
            className="w-full justify-start gap-2"
            variant={algorithm === "sjf" ? "default" : "outline"}
          >
            <Play className="w-4 h-4" />
            Shortest Job First (SJF)
          </Button>

          <Button
            onClick={() => executeAlgorithm("rr")}
            disabled={loading}
            className="w-full justify-start gap-2"
            variant={algorithm === "rr" ? "default" : "outline"}
          >
            <Play className="w-4 h-4" />
            Round Robin (RR) - Quantum: 2
          </Button>
        </CardContent>
      </Card>

      {/* Metrics Card */}
      {metrics && (
        <Card className="border-border bg-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5" />
              Métricas Globales
            </CardTitle>
            <CardDescription>Algoritmo: {algorithm.toUpperCase()}</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground">Tiempo Espera Promedio</p>
                <p className="text-2xl font-bold text-primary">{metrics.avgWaitTime.toFixed(2)}</p>
              </div>
              <div className="space-y-1">
                <p className="text-sm text-muted-foreground">Turnaround Promedio</p>
                <p className="text-2xl font-bold text-accent">{metrics.avgTurnaround.toFixed(2)}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Results Table Card */}
      {results.length > 0 && (
        <Card className="border-border bg-card">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5" />
              Resultados de Ejecución
            </CardTitle>
            <CardDescription>Detalles de cada proceso</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg border border-border overflow-hidden">
              <Table>
                <TableHeader>
                  <TableRow className="bg-muted/50">
                    <TableHead>PID</TableHead>
                    <TableHead>Llegada</TableHead>
                    <TableHead>Ráfaga</TableHead>
                    <TableHead>Espera</TableHead>
                    <TableHead>Finalización</TableHead>
                    <TableHead>Retorno</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {results.map((process) => (
                    <TableRow key={process.pid}>
                      <TableCell className="font-medium">
                        <Badge variant="outline">{process.pid}</Badge>
                      </TableCell>
                      <TableCell>{process.tiempo_llegada}</TableCell>
                      <TableCell>{process.rafaga_cpu}</TableCell>
                      <TableCell className="text-warning font-medium">{process.tiempo_espera}</TableCell>
                      <TableCell>{process.tiempo_finalizacion}</TableCell>
                      <TableCell className="text-success font-medium">{process.tiempo_retorno}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

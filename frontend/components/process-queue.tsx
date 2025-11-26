"use client";

import type React from "react";

import { useState, useEffect } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Plus, RefreshCw, Lock, Unlock } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const API_BASE = "http://localhost:8000";

interface Process {
  PID: number;
  Estado: string;
}

interface QueueData {
  cola_listos: number[];
  cola_bloqueados: number[];
}

export default function ProcessQueue({ onUpdate }: { onUpdate: () => void }) {
  const [processes, setProcesses] = useState<Process[]>([]);
  const [queueData, setQueueData] = useState<QueueData>({
    cola_listos: [],
    cola_bloqueados: [],
  });
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  // Form state
  const [newProcess, setNewProcess] = useState({
    PID: "",
    tiempo_llegada: "",
    rafaga_cpu: "",
    usuario: "",
  });

  const fetchProcesses = async () => {
    try {
      const response = await fetch(`${API_BASE}/colas/procesos`);
      const data = await response.json();
      setProcesses(data);
    } catch (error) {
      console.error("Error fetching processes:", error);
    }
  };

  const fetchQueues = async () => {
    try {
      const response = await fetch(`${API_BASE}/colas/mostrar`);
      const data = await response.json();
      setQueueData(data);
    } catch (error) {
      console.error("Error fetching queues:", error);
    }
  };

  useEffect(() => {
    fetchProcesses();
    fetchQueues();
  }, []);

  const handleAddProcess = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}/colas/agregar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          PID: Number.parseInt(newProcess.PID),
          tiempo_llegada: Number.parseInt(newProcess.tiempo_llegada),
          rafaga_cpu: Number.parseInt(newProcess.rafaga_cpu),
          usuario: newProcess.usuario,
        }),
      });

      if (response.ok) {
        toast({
          title: "Proceso agregado",
          description: `Proceso PID ${newProcess.PID} agregado exitosamente`,
        });
        setNewProcess({
          PID: "",
          tiempo_llegada: "",
          rafaga_cpu: "",
          usuario: "",
        });
        await fetchProcesses();
        await fetchQueues();
        onUpdate();
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo agregar el proceso",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleBlockProcess = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/colas/bloquear`, {
        method: "POST",
      });
      if (response.ok) {
        toast({
          title: "Proceso bloqueado",
          description: "Proceso movido a cola de bloqueados",
        });
        await fetchProcesses();
        await fetchQueues();
        onUpdate();
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "No hay procesos para bloquear",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleUnblockProcess = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/colas/desbloquear`, {
        method: "POST",
      });
      if (response.ok) {
        toast({
          title: "Proceso desbloqueado",
          description: "Proceso movido a cola de listos",
        });
        await fetchProcesses();
        await fetchQueues();
        onUpdate();
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "No hay procesos bloqueados",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setLoading(true);
    await fetchProcesses();
    await fetchQueues();
    setLoading(false);
  };

  return (
    <div className="space-y-4">
      {/* Add Process Card */}
      <Card className="border-border bg-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Plus className="w-5 h-5" />
            Agregar Proceso
          </CardTitle>
          <CardDescription>
            Crear un nuevo proceso en la cola de listos
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleAddProcess} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="pid">PID</Label>
                <Input
                  id="pid"
                  type="number"
                  placeholder="1"
                  value={newProcess.PID}
                  onChange={(e) =>
                    setNewProcess({ ...newProcess, PID: e.target.value })
                  }
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="llegada">Tiempo Llegada</Label>
                <Input
                  id="llegada"
                  type="number"
                  placeholder="0"
                  value={newProcess.tiempo_llegada}
                  onChange={(e) =>
                    setNewProcess({
                      ...newProcess,
                      tiempo_llegada: e.target.value,
                    })
                  }
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="rafaga">Ráfaga CPU</Label>
                <Input
                  id="rafaga"
                  type="number"
                  placeholder="5"
                  value={newProcess.rafaga_cpu}
                  onChange={(e) =>
                    setNewProcess({ ...newProcess, rafaga_cpu: e.target.value })
                  }
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="usuario">Usuario</Label>
                <Input
                  id="usuario"
                  placeholder="usuario1"
                  value={newProcess.usuario}
                  onChange={(e) =>
                    setNewProcess({ ...newProcess, usuario: e.target.value })
                  }
                  required
                />
              </div>
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              <Plus className="w-4 h-4 mr-2" />
              Agregar a Cola
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Queue Management Card */}
      <Card className="border-border bg-card">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Colas de Procesos</CardTitle>
              <CardDescription>Gestionar estado de procesos</CardDescription>
            </div>
            <Button
              variant="outline"
              size="icon"
              onClick={handleRefresh}
              disabled={loading}
            >
              <RefreshCw
                className={`w-4 h-4 ${loading ? "animate-spin" : ""}`}
              />
            </Button>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Ready Queue */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label className="text-sm font-medium flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-success" />
                Cola de Listos
              </Label>
              <Badge variant="secondary">{queueData.cola_listos.length}</Badge>
            </div>
            <div className="flex flex-wrap gap-2 min-h-[40px] p-3 rounded-lg border border-border bg-secondary/50">
              {queueData.cola_listos.length > 0 ? (
                queueData.cola_listos.map((pid) => (
                  <Badge
                    key={pid}
                    className="bg-success/20 text-success border-success/30"
                  >
                    PID {pid}
                  </Badge>
                ))
              ) : (
                <span className="text-sm text-muted-foreground">
                  Sin procesos listos
                </span>
              )}
            </div>
          </div>

          <Separator />

          {/* Blocked Queue */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label className="text-sm font-medium flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-warning" />
                Cola de Bloqueados
              </Label>
              <Badge variant="secondary">
                {queueData.cola_bloqueados.length}
              </Badge>
            </div>
            <div className="flex flex-wrap gap-2 min-h-[40px] p-3 rounded-lg border border-border bg-secondary/50">
              {queueData.cola_bloqueados.length > 0 ? (
                queueData.cola_bloqueados.map((pid) => (
                  <Badge
                    key={pid}
                    className="bg-warning/20 text-warning border-warning/30"
                  >
                    PID {pid}
                  </Badge>
                ))
              ) : (
                <span className="text-sm text-muted-foreground">
                  Sin procesos bloqueados
                </span>
              )}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 pt-2">
            <Button
              variant="outline"
              onClick={handleBlockProcess}
              disabled={loading || queueData.cola_listos.length === 0}
              className="gap-2 bg-transparent"
            >
              <Lock className="w-4 h-4" />
              Bloquear
            </Button>
            <Button
              variant="outline"
              onClick={handleUnblockProcess}
              disabled={loading || queueData.cola_bloqueados.length === 0}
              className="gap-2 bg-transparent"
            >
              <Unlock className="w-4 h-4" />
              Desbloquear
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

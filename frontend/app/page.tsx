"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import ProcessQueue from "@/components/process-queue"
import SchedulerControl from "@/components/scheduler-control"
import FileSystem from "@/components/file-system"
import { Cpu, HardDrive } from "lucide-react"

export default function Home() {
  const [refreshTrigger, setRefreshTrigger] = useState(0)

  const handleRefresh = () => {
    setRefreshTrigger((prev) => prev + 1)
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="flex items-center justify-center w-10 h-10 rounded-lg bg-primary/10">
              <Cpu className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-balance">Simulador de Planificación de Procesos</h1>
              <p className="text-sm text-muted-foreground">FCFS • SJF • Round Robin</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        <Tabs defaultValue="scheduler" className="w-full">
          <TabsList className="grid w-full max-w-md mx-auto grid-cols-2 mb-6">
            <TabsTrigger value="scheduler" className="gap-2">
              <Cpu className="w-4 h-4" />
              Planificador
            </TabsTrigger>
            <TabsTrigger value="filesystem" className="gap-2">
              <HardDrive className="w-4 h-4" />
              Sistema de Archivos
            </TabsTrigger>
          </TabsList>

          <TabsContent value="scheduler" className="space-y-6">
            <div className="grid lg:grid-cols-2 gap-6">
              {/* Process Queue Section */}
              <ProcessQueue key={refreshTrigger} onUpdate={handleRefresh} />

              {/* Scheduler Control Section */}
              <SchedulerControl onExecute={handleRefresh} />
            </div>
          </TabsContent>

          <TabsContent value="filesystem">
            <FileSystem />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}

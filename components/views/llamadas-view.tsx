"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Phone, Clock, User } from "lucide-react"

interface LlamadasViewProps {
  subSection: string
}

export function LlamadasView({ subSection }: LlamadasViewProps) {
  const [activeTab, setActiveTab] = useState("todas")

  const llamadas = [
    {
      id: 1,
      cliente: "Juan Pérez",
      agente: "María García",
      duracion: "5:23",
      estado: "completada",
      tipo: "entrante",
      fecha: "2024-01-16 10:30",
    },
    {
      id: 2,
      cliente: "Ana Martínez",
      agente: "Carlos López",
      duracion: "3:45",
      estado: "en-curso",
      tipo: "saliente",
      fecha: "2024-01-16 11:15",
    },
    {
      id: 3,
      cliente: "Pedro Gómez",
      agente: "Laura Sánchez",
      duracion: "0:00",
      estado: "perdida",
      tipo: "entrante",
      fecha: "2024-01-16 09:45",
    },
    {
      id: 4,
      cliente: "Sofía Torres",
      agente: "Roberto Díaz",
      duracion: "8:12",
      estado: "completada",
      tipo: "entrante",
      fecha: "2024-01-16 08:20",
    },
    {
      id: 5,
      cliente: "Miguel Ruiz",
      agente: "María García",
      duracion: "4:56",
      estado: "completada",
      tipo: "saliente",
      fecha: "2024-01-16 07:30",
    },
  ]

  if (subSection === "historial") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="todas"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Todas
              </TabsTrigger>
              <TabsTrigger
                value="completadas"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Completadas
              </TabsTrigger>
              <TabsTrigger
                value="perdidas"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Perdidas
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="todas" className="m-0 p-6 space-y-6">
              <div>
                <h2 className="text-3xl font-semibold text-balance">Historial de Llamadas</h2>
                <p className="text-muted-foreground mt-1">Registro completo de todas las llamadas</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="p-6 bg-card border-border">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">Total Hoy</p>
                      <p className="text-2xl font-semibold mt-1">156</p>
                    </div>
                    <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                      <Phone className="w-6 h-6 text-primary" />
                    </div>
                  </div>
                </Card>

                <Card className="p-6 bg-card border-border">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">Duración Total</p>
                      <p className="text-2xl font-semibold mt-1">12h 34m</p>
                    </div>
                    <div className="w-12 h-12 bg-success/10 rounded-lg flex items-center justify-center">
                      <Clock className="w-6 h-6 text-success" />
                    </div>
                  </div>
                </Card>

                <Card className="p-6 bg-card border-border">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">Tasa de Respuesta</p>
                      <p className="text-2xl font-semibold mt-1">94.2%</p>
                    </div>
                    <div className="w-12 h-12 bg-warning/10 rounded-lg flex items-center justify-center">
                      <User className="w-6 h-6 text-warning" />
                    </div>
                  </div>
                </Card>
              </div>

              <Card className="bg-card border-border">
                <div className="p-4 border-b border-border">
                  <h3 className="font-semibold">Llamadas Recientes</h3>
                </div>
                <div className="divide-y divide-border">
                  {llamadas.map((llamada) => (
                    <div key={llamada.id} className="p-4 hover:bg-secondary/30 transition-colors">
                      <div className="flex items-center justify-between gap-4">
                        <div className="flex items-center gap-4 flex-1">
                          <div
                            className={`w-10 h-10 rounded-full flex items-center justify-center ${
                              llamada.estado === "completada"
                                ? "bg-success/10"
                                : llamada.estado === "en-curso"
                                  ? "bg-primary/10"
                                  : "bg-destructive/10"
                            }`}
                          >
                            <Phone
                              className={`w-5 h-5 ${
                                llamada.estado === "completada"
                                  ? "text-success"
                                  : llamada.estado === "en-curso"
                                    ? "text-primary"
                                    : "text-destructive"
                              }`}
                            />
                          </div>

                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-2 mb-1">
                              <p className="font-medium">{llamada.cliente}</p>
                              <Badge
                                variant={llamada.tipo === "entrante" ? "default" : "secondary"}
                                className="text-xs"
                              >
                                {llamada.tipo}
                              </Badge>
                            </div>
                            <p className="text-sm text-muted-foreground">Agente: {llamada.agente}</p>
                          </div>
                        </div>

                        <div className="flex items-center gap-6 text-sm">
                          <div className="text-right">
                            <p className="text-muted-foreground">Duración</p>
                            <p className="font-medium">{llamada.duracion}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-muted-foreground">Fecha</p>
                            <p className="font-medium">{llamada.fecha}</p>
                          </div>
                          <Badge
                            variant={
                              llamada.estado === "completada"
                                ? "default"
                                : llamada.estado === "en-curso"
                                  ? "secondary"
                                  : "destructive"
                            }
                          >
                            {llamada.estado}
                          </Badge>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </TabsContent>

            <TabsContent value="completadas" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Llamadas Completadas</h2>
                  <p className="text-muted-foreground mt-1">Llamadas finalizadas exitosamente</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Lista de llamadas completadas...</p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="perdidas" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Llamadas Perdidas</h2>
                  <p className="text-muted-foreground mt-1">Llamadas no atendidas</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Lista de llamadas perdidas...</p>
                </Card>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  if (subSection === "activas") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="todas"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                En Curso
              </TabsTrigger>
              <TabsTrigger
                value="espera"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                En Espera
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="todas" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Llamadas Activas</h2>
                  <p className="text-muted-foreground mt-1">Llamadas en curso en este momento</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Monitoreo de llamadas activas...</p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="espera" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Llamadas en Espera</h2>
                  <p className="text-muted-foreground mt-1">Llamadas esperando ser atendidas</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Cola de espera...</p>
                </Card>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  if (subSection === "programadas") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="todas"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Próximas
              </TabsTrigger>
              <TabsTrigger
                value="calendario"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Calendario
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="todas" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Llamadas Programadas</h2>
                  <p className="text-muted-foreground mt-1">Llamadas agendadas para más tarde</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Lista de llamadas programadas...</p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="calendario" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Calendario de Llamadas</h2>
                  <p className="text-muted-foreground mt-1">Vista de calendario</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Vista de calendario...</p>
                </Card>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  return null
}

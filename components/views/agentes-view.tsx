"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Headphones, Star, Phone, Clock } from "lucide-react"

interface AgentesViewProps {
  subSection: string
}

export function AgentesView({ subSection }: AgentesViewProps) {
  const [activeTab, setActiveTab] = useState("todos")

  const agentes = [
    {
      id: 1,
      nombre: "María García",
      estado: "disponible",
      llamadas: 23,
      duracion: "2h 45m",
      rating: 4.8,
      especialidad: "Soporte Técnico",
    },
    {
      id: 2,
      nombre: "Carlos López",
      estado: "en-llamada",
      llamadas: 18,
      duracion: "2h 12m",
      rating: 4.6,
      especialidad: "Ventas",
    },
    {
      id: 3,
      nombre: "Laura Sánchez",
      estado: "disponible",
      llamadas: 31,
      duracion: "3h 20m",
      rating: 4.9,
      especialidad: "Atención al Cliente",
    },
    {
      id: 4,
      nombre: "Roberto Díaz",
      estado: "descanso",
      llamadas: 15,
      duracion: "1h 45m",
      rating: 4.7,
      especialidad: "Soporte Técnico",
    },
    {
      id: 5,
      nombre: "Elena Morales",
      estado: "disponible",
      llamadas: 27,
      duracion: "2h 55m",
      rating: 4.8,
      especialidad: "Ventas",
    },
  ]

  if (subSection === "lista") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="todos"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Todos
              </TabsTrigger>
              <TabsTrigger
                value="disponibles"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Disponibles
              </TabsTrigger>
              <TabsTrigger
                value="ocupados"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Ocupados
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="todos" className="m-0 p-6 space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Todos los Agentes</h2>
                  <p className="text-muted-foreground mt-1">Gestión y monitoreo de agentes del call center</p>
                </div>
                <Button className="gap-2">
                  <Headphones className="w-4 h-4" />
                  Nuevo Agente
                </Button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card className="p-6 bg-card border-border">
                  <p className="text-sm text-muted-foreground">Total Agentes</p>
                  <p className="text-3xl font-semibold mt-2">24</p>
                </Card>
                <Card className="p-6 bg-card border-border">
                  <p className="text-sm text-muted-foreground">Disponibles</p>
                  <p className="text-3xl font-semibold mt-2 text-success">18</p>
                </Card>
                <Card className="p-6 bg-card border-border">
                  <p className="text-sm text-muted-foreground">En Llamada</p>
                  <p className="text-3xl font-semibold mt-2 text-primary">5</p>
                </Card>
                <Card className="p-6 bg-card border-border">
                  <p className="text-sm text-muted-foreground">Descanso</p>
                  <p className="text-3xl font-semibold mt-2 text-muted-foreground">1</p>
                </Card>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {agentes.map((agente) => (
                  <Card key={agente.id} className="p-6 bg-card border-border">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-4">
                        <div className="w-14 h-14 bg-primary/10 rounded-full flex items-center justify-center">
                          <span className="text-lg font-semibold text-primary">
                            {agente.nombre
                              .split(" ")
                              .map((n) => n[0])
                              .join("")}
                          </span>
                        </div>
                        <div>
                          <h3 className="font-semibold text-lg">{agente.nombre}</h3>
                          <p className="text-sm text-muted-foreground">{agente.especialidad}</p>
                        </div>
                      </div>
                      <Badge
                        variant={
                          agente.estado === "disponible"
                            ? "default"
                            : agente.estado === "en-llamada"
                              ? "secondary"
                              : "outline"
                        }
                      >
                        {agente.estado}
                      </Badge>
                    </div>

                    <div className="grid grid-cols-3 gap-4 mb-4">
                      <div className="text-center p-3 bg-secondary/50 rounded-lg">
                        <Phone className="w-4 h-4 text-muted-foreground mx-auto mb-1" />
                        <p className="text-xl font-semibold">{agente.llamadas}</p>
                        <p className="text-xs text-muted-foreground">Llamadas</p>
                      </div>
                      <div className="text-center p-3 bg-secondary/50 rounded-lg">
                        <Clock className="w-4 h-4 text-muted-foreground mx-auto mb-1" />
                        <p className="text-xl font-semibold">{agente.duracion}</p>
                        <p className="text-xs text-muted-foreground">Duración</p>
                      </div>
                      <div className="text-center p-3 bg-secondary/50 rounded-lg">
                        <Star className="w-4 h-4 text-warning mx-auto mb-1 fill-warning" />
                        <p className="text-xl font-semibold">{agente.rating}</p>
                        <p className="text-xs text-muted-foreground">Rating</p>
                      </div>
                    </div>

                    <Button variant="outline" className="w-full bg-transparent">
                      Ver Detalles
                    </Button>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="disponibles" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Agentes Disponibles</h2>
                  <p className="text-muted-foreground mt-1">Agentes listos para atender llamadas</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Lista de agentes disponibles...</p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="ocupados" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Agentes Ocupados</h2>
                  <p className="text-muted-foreground mt-1">Agentes actualmente en llamada</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Lista de agentes ocupados...</p>
                </Card>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  if (subSection === "rendimiento") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="todos"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Métricas
              </TabsTrigger>
              <TabsTrigger
                value="ranking"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Ranking
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="todos" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Métricas de Rendimiento</h2>
                  <p className="text-muted-foreground mt-1">Análisis detallado del desempeño</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Métricas de rendimiento...</p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="ranking" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Ranking de Agentes</h2>
                  <p className="text-muted-foreground mt-1">Clasificación por desempeño</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Tabla de ranking...</p>
                </Card>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  if (subSection === "horarios") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="todos"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Calendario
              </TabsTrigger>
              <TabsTrigger
                value="turnos"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Turnos
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="todos" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Calendario de Horarios</h2>
                  <p className="text-muted-foreground mt-1">Gestión de turnos y disponibilidad</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Calendario de horarios...</p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="turnos" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Gestión de Turnos</h2>
                  <p className="text-muted-foreground mt-1">Asignación y configuración de turnos</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Gestión de turnos...</p>
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

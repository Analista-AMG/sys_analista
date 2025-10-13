"use client"

import { Card } from "@/components/ui/card"
import { Phone, PhoneIncoming, PhoneMissed, Clock, TrendingUp, TrendingDown } from "lucide-react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useState } from "react"

interface DashboardViewProps {
  subSection: string
}

export function DashboardView({ subSection }: DashboardViewProps) {
  const [activeTab, setActiveTab] = useState("general")

  const stats = [
    { label: "Llamadas Totales", value: "1,234", change: "+12%", trend: "up", icon: Phone },
    { label: "Llamadas Activas", value: "23", change: "+5", trend: "up", icon: PhoneIncoming },
    { label: "Llamadas Perdidas", value: "45", change: "-8%", trend: "down", icon: PhoneMissed },
    { label: "Tiempo Promedio", value: "4:32", change: "-15s", trend: "down", icon: Clock },
  ]

  if (subSection === "resumen") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="general"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Vista General
              </TabsTrigger>
              <TabsTrigger
                value="estadisticas"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Estadísticas
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="general" className="m-0 p-6 space-y-6">
              <div>
                <h2 className="text-3xl font-semibold text-balance">Resumen General</h2>
                <p className="text-muted-foreground mt-1">Vista general del call center en tiempo real</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {stats.map((stat) => {
                  const Icon = stat.icon
                  const TrendIcon = stat.trend === "up" ? TrendingUp : TrendingDown

                  return (
                    <Card key={stat.label} className="p-6 bg-card border-border">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="text-sm text-muted-foreground">{stat.label}</p>
                          <p className="text-3xl font-semibold mt-2">{stat.value}</p>
                          <div className="flex items-center gap-1 mt-2">
                            <TrendIcon
                              className={`w-3 h-3 ${stat.trend === "up" ? "text-success" : "text-destructive"}`}
                            />
                            <span
                              className={`text-xs font-medium ${stat.trend === "up" ? "text-success" : "text-destructive"}`}
                            >
                              {stat.change}
                            </span>
                            <span className="text-xs text-muted-foreground ml-1">vs ayer</span>
                          </div>
                        </div>
                        <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                          <Icon className="w-5 h-5 text-primary" />
                        </div>
                      </div>
                    </Card>
                  )
                })}
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="p-6 bg-card border-border">
                  <h3 className="text-lg font-semibold mb-4">Actividad Reciente</h3>
                  <div className="space-y-4">
                    {[
                      {
                        agent: "María García",
                        action: "Llamada completada",
                        client: "Juan Pérez",
                        time: "Hace 2 min",
                        status: "success",
                      },
                      {
                        agent: "Carlos López",
                        action: "Llamada en curso",
                        client: "Ana Martínez",
                        time: "5:23",
                        status: "active",
                      },
                      {
                        agent: "Laura Sánchez",
                        action: "Llamada perdida",
                        client: "Pedro Gómez",
                        time: "Hace 8 min",
                        status: "missed",
                      },
                      {
                        agent: "Roberto Díaz",
                        action: "Llamada completada",
                        client: "Sofía Torres",
                        time: "Hace 12 min",
                        status: "success",
                      },
                    ].map((activity, i) => (
                      <div key={i} className="flex items-center gap-4 p-3 rounded-lg bg-secondary/50">
                        <div
                          className={`w-2 h-2 rounded-full ${
                            activity.status === "success"
                              ? "bg-success"
                              : activity.status === "active"
                                ? "bg-primary animate-pulse"
                                : "bg-destructive"
                          }`}
                        />
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium">{activity.agent}</p>
                          <p className="text-xs text-muted-foreground">
                            {activity.action} - {activity.client}
                          </p>
                        </div>
                        <span className="text-xs text-muted-foreground">{activity.time}</span>
                      </div>
                    ))}
                  </div>
                </Card>

                <Card className="p-6 bg-card border-border">
                  <h3 className="text-lg font-semibold mb-4">Agentes Disponibles</h3>
                  <div className="space-y-4">
                    {[
                      { name: "María García", status: "Disponible", calls: 12, rating: 4.8 },
                      { name: "Carlos López", status: "En llamada", calls: 8, rating: 4.6 },
                      { name: "Laura Sánchez", status: "Disponible", calls: 15, rating: 4.9 },
                      { name: "Roberto Díaz", status: "Descanso", calls: 10, rating: 4.7 },
                    ].map((agent, i) => (
                      <div key={i} className="flex items-center gap-4 p-3 rounded-lg bg-secondary/50">
                        <div className="w-10 h-10 bg-muted rounded-full flex items-center justify-center">
                          <span className="text-sm font-semibold">
                            {agent.name
                              .split(" ")
                              .map((n) => n[0])
                              .join("")}
                          </span>
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium">{agent.name}</p>
                          <p className="text-xs text-muted-foreground">
                            {agent.calls} llamadas hoy • ⭐ {agent.rating}
                          </p>
                        </div>
                        <span
                          className={`text-xs px-2 py-1 rounded-full ${
                            agent.status === "Disponible"
                              ? "bg-success/20 text-success"
                              : agent.status === "En llamada"
                                ? "bg-primary/20 text-primary"
                                : "bg-muted text-muted-foreground"
                          }`}
                        >
                          {agent.status}
                        </span>
                      </div>
                    ))}
                  </div>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="estadisticas" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Estadísticas del Resumen</h2>
                  <p className="text-muted-foreground mt-1">Datos estadísticos detallados</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Contenido de estadísticas del resumen...</p>
                </Card>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  if (subSection === "metricas") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="general"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Tiempo Real
              </TabsTrigger>
              <TabsTrigger
                value="historico"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Histórico
              </TabsTrigger>
              <TabsTrigger
                value="comparativo"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Comparativo
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="general" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Métricas en Tiempo Real</h2>
                  <p className="text-muted-foreground mt-1">Monitoreo en vivo del rendimiento</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Contenido de métricas en tiempo real...</p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="historico" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Métricas Históricas</h2>
                  <p className="text-muted-foreground mt-1">Análisis de datos pasados</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Contenido de métricas históricas...</p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="comparativo" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Análisis Comparativo</h2>
                  <p className="text-muted-foreground mt-1">Comparación de períodos</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Contenido de análisis comparativo...</p>
                </Card>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  if (subSection === "graficos") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="general"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Barras
              </TabsTrigger>
              <TabsTrigger
                value="lineas"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Líneas
              </TabsTrigger>
              <TabsTrigger
                value="circular"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Circular
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="general" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Gráficos de Barras</h2>
                  <p className="text-muted-foreground mt-1">Visualización en barras</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Contenido de gráficos de barras...</p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="lineas" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Gráficos de Líneas</h2>
                  <p className="text-muted-foreground mt-1">Tendencias y evolución</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Contenido de gráficos de líneas...</p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="circular" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Gráficos Circulares</h2>
                  <p className="text-muted-foreground mt-1">Distribución porcentual</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Contenido de gráficos circulares...</p>
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

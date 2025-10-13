"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Download, TrendingUp, TrendingDown } from "lucide-react"

interface ReportesViewProps {
  subSection: string
}

export function ReportesView({ subSection }: ReportesViewProps) {
  const [activeTab, setActiveTab] = useState("resumen")

  if (subSection === "general") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="resumen"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Resumen
              </TabsTrigger>
              <TabsTrigger
                value="detalles"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Detalles
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="resumen" className="m-0 p-6 space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Reporte General</h2>
                  <p className="text-muted-foreground mt-1">Análisis y estadísticas del call center</p>
                </div>
                <Button className="gap-2">
                  <Download className="w-4 h-4" />
                  Exportar Reporte
                </Button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {[
                  { label: "Llamadas del Mes", value: "3,456", change: "+18%", trend: "up" },
                  { label: "Satisfacción Cliente", value: "92%", change: "+3%", trend: "up" },
                  { label: "Tiempo Promedio", value: "4:32", change: "-12%", trend: "down" },
                  { label: "Tasa de Resolución", value: "87%", change: "+5%", trend: "up" },
                ].map((stat, i) => (
                  <Card key={i} className="p-6 bg-card border-border">
                    <p className="text-sm text-muted-foreground">{stat.label}</p>
                    <p className="text-3xl font-semibold mt-2">{stat.value}</p>
                    <div className="flex items-center gap-1 mt-2">
                      {stat.trend === "up" ? (
                        <TrendingUp className="w-3 h-3 text-success" />
                      ) : (
                        <TrendingDown className="w-3 h-3 text-destructive" />
                      )}
                      <span
                        className={`text-xs font-medium ${stat.trend === "up" ? "text-success" : "text-destructive"}`}
                      >
                        {stat.change}
                      </span>
                      <span className="text-xs text-muted-foreground ml-1">vs mes anterior</span>
                    </div>
                  </Card>
                ))}
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="p-6 bg-card border-border">
                  <h3 className="text-lg font-semibold mb-4">Rendimiento por Agente</h3>
                  <div className="space-y-4">
                    {[
                      { nombre: "Laura Sánchez", llamadas: 156, rating: 4.9 },
                      { nombre: "María García", llamadas: 142, rating: 4.8 },
                      { nombre: "Elena Morales", llamadas: 138, rating: 4.8 },
                      { nombre: "Carlos López", llamadas: 125, rating: 4.6 },
                      { nombre: "Roberto Díaz", llamadas: 118, rating: 4.7 },
                    ].map((agente, i) => (
                      <div key={i} className="flex items-center gap-4">
                        <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center text-xs font-semibold text-primary">
                          {i + 1}
                        </div>
                        <div className="flex-1">
                          <p className="font-medium">{agente.nombre}</p>
                          <div className="flex items-center gap-4 mt-1">
                            <span className="text-xs text-muted-foreground">{agente.llamadas} llamadas</span>
                            <span className="text-xs text-muted-foreground">⭐ {agente.rating}</span>
                          </div>
                        </div>
                        <div className="w-24 h-2 bg-secondary rounded-full overflow-hidden">
                          <div className="h-full bg-primary" style={{ width: `${(agente.llamadas / 156) * 100}%` }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>

                <Card className="p-6 bg-card border-border">
                  <h3 className="text-lg font-semibold mb-4">Distribución de Llamadas</h3>
                  <div className="space-y-4">
                    {[
                      { tipo: "Soporte Técnico", cantidad: 1245, porcentaje: 36, color: "bg-primary" },
                      { tipo: "Ventas", cantidad: 1089, porcentaje: 31, color: "bg-success" },
                      { tipo: "Atención al Cliente", cantidad: 876, porcentaje: 25, color: "bg-warning" },
                      { tipo: "Otros", cantidad: 246, porcentaje: 8, color: "bg-muted" },
                    ].map((item, i) => (
                      <div key={i}>
                        <div className="flex items-center justify-between mb-2">
                          <span className="text-sm font-medium">{item.tipo}</span>
                          <span className="text-sm text-muted-foreground">
                            {item.cantidad} ({item.porcentaje}%)
                          </span>
                        </div>
                        <div className="w-full h-2 bg-secondary rounded-full overflow-hidden">
                          <div className={`h-full ${item.color}`} style={{ width: `${item.porcentaje}%` }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="detalles" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Detalles del Reporte</h2>
                  <p className="text-muted-foreground mt-1">Información detallada</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Detalles completos...</p>
                </Card>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  if (subSection === "mensual") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="resumen"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Este Mes
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
            <TabsContent value="resumen" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Reporte Mensual</h2>
                  <p className="text-muted-foreground mt-1">Estadísticas del mes actual</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Datos mensuales...</p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="comparativo" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Comparativo Mensual</h2>
                  <p className="text-muted-foreground mt-1">Comparación con meses anteriores</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Análisis comparativo...</p>
                </Card>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  if (subSection === "personalizado") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="resumen"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Constructor
              </TabsTrigger>
              <TabsTrigger
                value="plantillas"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Plantillas
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="resumen" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Constructor de Reportes</h2>
                  <p className="text-muted-foreground mt-1">Crea reportes con filtros personalizados</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Constructor de reportes...</p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="plantillas" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Plantillas de Reportes</h2>
                  <p className="text-muted-foreground mt-1">Plantillas predefinidas</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Galería de plantillas...</p>
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

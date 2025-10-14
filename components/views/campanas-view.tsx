"use client"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useState } from "react"
import {  Clock3, TrendingUp, TrendingUpDown} from "lucide-react";


interface CampanasViewProps {
  subSection: string
}

export function CampanasView({ subSection }: CampanasViewProps) {
  const [selectedDashboard, setSelectedDashboard] = useState("activaciones")

  const renderActivacionesContent = () => {
    return (
      <div className="p-6">
        
          <Tabs defaultValue="dia-actual" className="w-full">
            <div className="flex justify-center">
              <TabsList className="mb-6 flex justify-center space-x-2 rounded-lg p-1">
                <TabsTrigger value="dia-actual" className="px-8 py-2">Día Actual</TabsTrigger>
                <TabsTrigger value="dashboard" className="px-8 py-2">Dashboard</TabsTrigger>
                <TabsTrigger value="descargas" className="px-8 py-2">Descargas</TabsTrigger>
              </TabsList>
            </div>
          <TabsContent value="dia-actual" className="space-y-6">
            <div className="mb-6">
              <h2 className="text-2xl font-semibold text-foreground mb-1 text-center">Métricas del Día Actual</h2>
              <p className="text-sm text-muted-foreground text-center">Indicadores en tiempo real del call center</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card className="p-4 flex flex-col justify-between">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-sm text-muted-foreground">TMO</p>
                    <p className="text-sm text-muted-foreground">Tiempo medio de operación</p>
                  </div>
                  <Clock3 className="w-5 h-5 text-blue-500" />
                </div>
                <p className="text-2xl font-bold text-foreground mt-2">05:32</p>
              </Card>
              <Card className="p-4 flex flex-col justify-between">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-sm text-muted-foreground">TME</p>
                    <p className="text-sm text-muted-foreground">Tiempo medio de espera</p>
                  </div>
                  <Clock3 className="w-5 h-5 text-blue-500" />
                </div>
                <p className="text-2xl font-bold text-foreground mt-2">01:45</p>
              </Card>
              <Card className="p-4 flex flex-col justify-between">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-sm text-muted-foreground">Casos del día</p>
                    <p className="text-sm text-muted-foreground">Total procesado</p>
                  </div>
                  <TrendingUp className="w-5 h-5 text-blue-500" />
                </div>
                <p className="text-2xl font-bold text-foreground mt-2">342</p>
              </Card>
              <Card className="p-4 flex flex-col justify-between">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="text-sm text-muted-foreground">Promedio Diario</p>
                    <p className="text-sm text-muted-foreground">Últimos 30 días</p>
                  </div>
                  <TrendingUpDown className="w-5 h-5 text-blue-500" />
                </div>
                <p className="text-2xl font-bold text-foreground mt-2">298</p>
                <p className="text-sm text-foreground -mt-5">casos/día</p>
              </Card>
            </div>

            <Card className="p-6">
              <h3 className="text-lg font-semibold text-foreground mb-4">Gestiones del Día</h3>
              <div className="space-y-3">
                {[1, 2, 3, 4, 5, 6].map((i) => (
                  <div key={i} className="flex items-center justify-between p-3 bg-secondary/50 rounded-lg">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-foreground">Cliente #{2000 + i}</p>
                      <p className="text-xs text-muted-foreground">
                        Hora: {8 + i}:30 AM - Analista: {i % 2 === 0 ? "María García" : "Carlos López"}
                      </p>
                    </div>
                    <Badge variant={i % 3 === 0 ? "default" : i % 3 === 1 ? "secondary" : "outline"}>
                      {i % 3 === 0 ? "Completado" : i % 3 === 1 ? "En Proceso" : "Pendiente"}
                    </Badge>
                  </div>
                ))}
              </div>
            </Card>
          </TabsContent>

          <TabsContent value="dashboard" className="space-y-6">
            <div className="mb-6">
              <h3 className="text-2xl font-semibold text-foreground mb-4">Dashboard de Activaciones</h3>

              <div className="mb-4">
                <label className="text-sm text-muted-foreground mb-2 block">Seleccionar Dashboard</label>
                <Select value={selectedDashboard} onValueChange={setSelectedDashboard}>
                  <SelectTrigger className="w-full md:w-[300px]">
                    <SelectValue placeholder="Selecciona un dashboard" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="activaciones">Dashboard Activaciones</SelectItem>
                    <SelectItem value="general">Dashboard General</SelectItem>
                    <SelectItem value="analistas">Dashboard Analistas</SelectItem>
                    <SelectItem value="historico">Dashboard Histórico</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <Card className="p-0 overflow-hidden">
              <iframe
                src="https://app.powerbi.com/view?r=eyJrIjoiYjFjNDIzNzUtODhhMy00ZGYxLWI3NWEtODJiYTA0YTAzOTk0IiwidCI6IjVhZTRkNjc0LWU2ZGEtNDBjMS1iNTNjLWY3NDNhNTc0OWY1ZCIsImMiOjR9"
                className="w-full h-[800px] border-0"
                allowFullScreen
              />
            </Card>
          </TabsContent>

          <TabsContent value="descargas" className="space-y-6">
            <Card className="p-6">
              <h3 className="text-lg font-semibold text-foreground mb-4">Reportes Disponibles</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-foreground">Reporte Diario</p>
                    <p className="text-xs text-muted-foreground">Gestiones del día actual</p>
                  </div>
                  <Button size="sm">Descargar Excel</Button>
                </div>
                <div className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-foreground">Reporte Semanal</p>
                    <p className="text-xs text-muted-foreground">Resumen de la última semana</p>
                  </div>
                  <Button size="sm">Descargar Excel</Button>
                </div>
                <div className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-foreground">Reporte Mensual</p>
                    <p className="text-xs text-muted-foreground">Estadísticas del mes</p>
                  </div>
                  <Button size="sm">Descargar Excel</Button>
                </div>
                <div className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-foreground">Reporte por Analista</p>
                    <p className="text-xs text-muted-foreground">Rendimiento individual</p>
                  </div>
                  <Button size="sm">Descargar Excel</Button>
                </div>
                <div className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-foreground">Base de Datos Completa</p>
                    <p className="text-xs text-muted-foreground">Todas las gestiones registradas</p>
                  </div>
                  <Button size="sm">Descargar Excel</Button>
                </div>
              </div>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    )
  }

  const renderCampanaContent = (campana: string) => {
    return (
      <div className="p-6 space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground mb-1">{campana}</h2>
          <p className="text-sm text-muted-foreground">Gestión de campaña {campana}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Card className="p-4">
            <p className="text-sm text-muted-foreground">Gestiones Totales</p>
            <p className="text-2xl font-bold text-foreground mt-2">1,234</p>
          </Card>
          <Card className="p-4">
            <p className="text-sm text-muted-foreground">Efectividad</p>
            <p className="text-2xl font-bold text-foreground mt-2">85%</p>
          </Card>
          <Card className="p-4">
            <p className="text-sm text-muted-foreground">Analistas Asignados</p>
            <p className="text-2xl font-bold text-foreground mt-2">8</p>
          </Card>
        </div>

        <Card className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-foreground">Gestiones Recientes</h3>
            <Button size="sm">Ver Todas</Button>
          </div>
          <div className="space-y-3">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="flex items-center justify-between p-3 bg-secondary/50 rounded-lg">
                <div className="flex-1">
                  <p className="text-sm font-medium text-foreground">Cliente #{1000 + i}</p>
                  <p className="text-xs text-muted-foreground">Analista: Juan Pérez</p>
                </div>
                <Badge variant={i % 2 === 0 ? "default" : "secondary"}>
                  {i % 2 === 0 ? "Completado" : "En Proceso"}
                </Badge>
              </div>
            ))}
          </div>
        </Card>
      </div>
    )
  }

  if (subSection === "activaciones") return renderActivacionesContent()
  if (subSection === "aghaso") return renderCampanaContent("Aghaso")
  if (subSection === "delivery") return renderCampanaContent("Delivery")
  if (subSection === "foto-corporativo") return renderCampanaContent("Foto Corporativo")
  if (subSection === "foto-alambrico") return renderCampanaContent("Foto Alambrico")

  return null
}

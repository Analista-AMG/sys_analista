"use client"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"

interface CampanasViewProps {
  subSection: string
}

export function CampanasView({ subSection }: CampanasViewProps) {
  const renderActivacionesContent = () => {
    return (
      <div className="p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-semibold text-foreground mb-1">Activaciones</h2>
          <p className="text-sm text-muted-foreground">Gestión de campaña Activaciones</p>
        </div>

        <Tabs defaultValue="dia-actual" className="w-full">
          <TabsList className="mb-6">
            <TabsTrigger value="dia-actual">Día Actual</TabsTrigger>
            <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            <TabsTrigger value="descargas">Descargas</TabsTrigger>
          </TabsList>

          <TabsContent value="dia-actual" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">Gestiones Hoy</p>
                <p className="text-2xl font-bold text-foreground mt-2">156</p>
              </Card>
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">Efectividad</p>
                <p className="text-2xl font-bold text-foreground mt-2">92%</p>
              </Card>
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">En Proceso</p>
                <p className="text-2xl font-bold text-foreground mt-2">23</p>
              </Card>
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">Completadas</p>
                <p className="text-2xl font-bold text-foreground mt-2">133</p>
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
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">Gestiones Totales</p>
                <p className="text-2xl font-bold text-foreground mt-2">1,234</p>
              </Card>
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">Efectividad Promedio</p>
                <p className="text-2xl font-bold text-foreground mt-2">85%</p>
              </Card>
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">Analistas Asignados</p>
                <p className="text-2xl font-bold text-foreground mt-2">8</p>
              </Card>
            </div>

            <Card className="p-6">
              <h3 className="text-lg font-semibold text-foreground mb-4">Rendimiento por Analista</h3>
              <div className="space-y-3">
                {["María García", "Carlos López", "Ana Martínez", "Juan Pérez", "Laura Sánchez"].map((nombre, i) => (
                  <div key={i} className="flex items-center justify-between p-3 bg-secondary/50 rounded-lg">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-foreground">{nombre}</p>
                      <p className="text-xs text-muted-foreground">Gestiones: {150 + i * 20}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-bold text-foreground">{85 + i * 2}%</p>
                      <p className="text-xs text-muted-foreground">Efectividad</p>
                    </div>
                  </div>
                ))}
              </div>
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

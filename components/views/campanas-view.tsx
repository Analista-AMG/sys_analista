"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"

interface CampanasViewProps {
  subSection: string
}

export function CampanasView({ subSection }: CampanasViewProps) {
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

  if (subSection === "activaciones") return renderCampanaContent("Activaciones")
  if (subSection === "aghaso") return renderCampanaContent("Aghaso")
  if (subSection === "delivery") return renderCampanaContent("Delivery")
  if (subSection === "foto-corporativo") return renderCampanaContent("Foto Corporativo")
  if (subSection === "foto-alambrico") return renderCampanaContent("Foto Alambrico")

  return null
}

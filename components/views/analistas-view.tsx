"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { User, Clock } from "lucide-react"

interface AnalistasViewProps {
  subSection: string
}

export function AnalistasView({ subSection }: AnalistasViewProps) {
  if (subSection === "lista") {
    return (
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-foreground mb-1">Lista de Analistas</h2>
            <p className="text-sm text-muted-foreground">Gestión de analistas del sistema</p>
          </div>
          <Button>Agregar Analista</Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Card key={i} className="p-6">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
                  <User className="w-6 h-6 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-foreground">Analista {i}</h3>
                  <p className="text-sm text-muted-foreground">analista{i}@sys.com</p>
                  <div className="flex items-center gap-2 mt-3">
                    <Badge variant={i % 2 === 0 ? "default" : "secondary"}>
                      {i % 2 === 0 ? "Activo" : "Disponible"}
                    </Badge>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  if (subSection === "rendimiento") {
    return (
      <div className="p-6 space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground mb-1">Rendimiento</h2>
          <p className="text-sm text-muted-foreground">Métricas de rendimiento de analistas</p>
        </div>

        <div className="space-y-4">
          {[1, 2, 3, 4, 5].map((i) => (
            <Card key={i} className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">Analista {i}</h3>
                    <p className="text-sm text-muted-foreground">Campaña: Activaciones</p>
                  </div>
                </div>
                <div className="flex items-center gap-6">
                  <div className="text-center">
                    <p className="text-sm text-muted-foreground">Gestiones</p>
                    <p className="text-lg font-bold text-foreground">{20 + i * 5}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-muted-foreground">Efectividad</p>
                    <p className="text-lg font-bold text-foreground">{80 + i}%</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-muted-foreground">Tiempo Prom.</p>
                    <p className="text-lg font-bold text-foreground">{5 + i} min</p>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  if (subSection === "horarios") {
    return (
      <div className="p-6 space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground mb-1">Horarios</h2>
          <p className="text-sm text-muted-foreground">Gestión de horarios de analistas</p>
        </div>

        <Card className="p-6">
          <div className="space-y-4">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">Analista {i}</h3>
                    <p className="text-sm text-muted-foreground">Turno: Mañana</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-muted-foreground" />
                  <span className="text-sm text-foreground">08:00 - 16:00</span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    )
  }

  return null
}

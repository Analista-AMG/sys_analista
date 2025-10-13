"use client"

import { Card } from "@/components/ui/card"
import { BarChart3, Users, Phone, TrendingUp } from "lucide-react"

interface InicioViewProps {
  subSection: string
}

export function InicioView({ subSection }: InicioViewProps) {
  if (subSection === "dashboard") {
    return (
      <div className="p-6 space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground mb-1">Dashboard</h2>
          <p className="text-sm text-muted-foreground">Vista general del sistema</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Analistas</p>
                <p className="text-3xl font-bold text-foreground mt-2">24</p>
              </div>
              <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center">
                <Users className="w-6 h-6 text-primary" />
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Campañas Activas</p>
                <p className="text-3xl font-bold text-foreground mt-2">5</p>
              </div>
              <div className="w-12 h-12 bg-blue-500/10 rounded-lg flex items-center justify-center">
                <BarChart3 className="w-6 h-6 text-blue-500" />
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Gestiones Hoy</p>
                <p className="text-3xl font-bold text-foreground mt-2">156</p>
              </div>
              <div className="w-12 h-12 bg-green-500/10 rounded-lg flex items-center justify-center">
                <Phone className="w-6 h-6 text-green-500" />
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Efectividad</p>
                <p className="text-3xl font-bold text-foreground mt-2">87%</p>
              </div>
              <div className="w-12 h-12 bg-orange-500/10 rounded-lg flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-orange-500" />
              </div>
            </div>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="p-6">
            <h3 className="text-lg font-semibold text-foreground mb-4">Actividad Reciente</h3>
            <div className="space-y-4">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="flex items-center gap-3 pb-3 border-b border-border last:border-0">
                  <div className="w-2 h-2 bg-primary rounded-full" />
                  <div className="flex-1">
                    <p className="text-sm text-foreground">Nueva gestión completada</p>
                    <p className="text-xs text-muted-foreground">Hace {i * 5} minutos</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card className="p-6">
            <h3 className="text-lg font-semibold text-foreground mb-4">Campañas Activas</h3>
            <div className="space-y-3">
              {["Activaciones", "Aghaso", "Delivery", "Foto Corporativo", "Foto Alambrico"].map((campana) => (
                <div key={campana} className="flex items-center justify-between p-3 bg-secondary/50 rounded-lg">
                  <span className="text-sm font-medium text-foreground">{campana}</span>
                  <span className="text-xs text-muted-foreground">Activa</span>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    )
  }

  if (subSection === "resumen") {
    return (
      <div className="p-6 space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground mb-1">Resumen</h2>
          <p className="text-sm text-muted-foreground">Resumen general de operaciones</p>
        </div>

        <Card className="p-6">
          <h3 className="text-lg font-semibold text-foreground mb-4">Métricas del Día</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-sm text-muted-foreground mb-2">Gestiones Completadas</p>
              <p className="text-2xl font-bold text-foreground">156</p>
              <p className="text-xs text-green-500 mt-1">+12% vs ayer</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground mb-2">Tiempo Promedio</p>
              <p className="text-2xl font-bold text-foreground">8.5 min</p>
              <p className="text-xs text-red-500 mt-1">+2% vs ayer</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground mb-2">Satisfacción</p>
              <p className="text-2xl font-bold text-foreground">4.7/5</p>
              <p className="text-xs text-green-500 mt-1">+0.2 vs ayer</p>
            </div>
          </div>
        </Card>
      </div>
    )
  }

  return null
}

"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useState } from "react"

interface AnalistasViewProps {
  subSection: string
}

export function AnalistasView({ subSection }: AnalistasViewProps) {
  const getDefaultDates = () => {
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)
    return yesterday.toISOString().split("T")[0]
  }

  const [fechaInicio, setFechaInicio] = useState(getDefaultDates())
  const [fechaFin, setFechaFin] = useState(getDefaultDates())
  const [sistemaSeleccionado, setSistemaSeleccionado] = useState("")
  const [consoleLogs, setConsoleLogs] = useState<string[]>([])

  const addLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString()
    setConsoleLogs((prev) => [...prev, `[${timestamp}] ${message}`])
  }

  const getSystemButtons = () => {
    switch (sistemaSeleccionado) {
      case "salesys":
        return ["General", "Agaso"]
      case "genesys":
        return ["General", "Detallado"]
      case "ipcc":
        return ["Reporte 1", "Reporte 2", "Soporte"]
      default:
        return []
    }
  }

  if (subSection === "conexiones") {
    return (
      <div className="p-6 space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground mb-1">Conexiones</h2>
          <p className="text-sm text-muted-foreground">Consulta de conexiones por rango de fechas</p>
        </div>

        <Card className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="space-y-2">
              <Label htmlFor="fecha-inicio">Fecha Inicio</Label>
              <Input
                id="fecha-inicio"
                type="date"
                value={fechaInicio}
                onChange={(e) => setFechaInicio(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="fecha-fin">Fecha Fin</Label>
              <Input id="fecha-fin" type="date" value={fechaFin} onChange={(e) => setFechaFin(e.target.value)} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="sistema">Sistema</Label>
              <Select value={sistemaSeleccionado} onValueChange={setSistemaSeleccionado}>
                <SelectTrigger id="sistema">
                  <SelectValue placeholder="Seleccionar sistema" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="salesys">SaleSys</SelectItem>
                  <SelectItem value="genesys">Genesys</SelectItem>
                  <SelectItem value="ipcc">IPCC</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {sistemaSeleccionado && (
            <div className="mb-6">
              <Label className="mb-3 block">Opciones de Reporte</Label>
              <div className="flex flex-wrap gap-3">
                {getSystemButtons().map((buttonName) => (
                  <Button
                    key={buttonName}
                    onClick={() =>
                      addLog(
                        `Botón presionado: ${buttonName} - Sistema: ${sistemaSeleccionado.toUpperCase()} - Período: ${fechaInicio} al ${fechaFin}`,
                      )
                    }
                    variant="outline"
                  >
                    {buttonName}
                  </Button>
                ))}
              </div>
            </div>
          )}

          {sistemaSeleccionado && (
            <div className="mt-6">
              <Label className="mb-2 block">Consola de Eventos</Label>
              <div className="bg-black text-green-400 font-mono text-sm p-4 rounded-lg h-64 overflow-y-auto">
                {consoleLogs.length === 0 ? (
                  <div className="text-gray-500">Esperando eventos...</div>
                ) : (
                  consoleLogs.map((log, index) => (
                    <div key={index} className="mb-1">
                      {log}
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </Card>
      </div>
    )
  }

  if (subSection === "campanas") {
    return (
      <div className="p-6 space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground mb-1">Campañas de Analistas</h2>
          <p className="text-sm text-muted-foreground">Gestión de campañas asignadas a analistas</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {["Activaciones", "Aghaso", "Delivery", "Foto Corporativo", "Foto Alambrico", "NPS"].map((campana, i) => (
            <Card key={i} className="p-6">
              <h3 className="text-lg font-semibold text-foreground mb-2">{campana}</h3>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Analistas asignados:</span>
                  <span className="font-semibold text-foreground">{5 + i}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Gestiones hoy:</span>
                  <span className="font-semibold text-foreground">{120 + i * 20}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Efectividad:</span>
                  <span className="font-semibold text-foreground">{75 + i}%</span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  if (subSection === "scraping") {
    return (
      <div className="p-6 space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground mb-1">Scraping</h2>
          <p className="text-sm text-muted-foreground">Extracción y procesamiento de datos</p>
        </div>

        <Card className="p-6">
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
              <div>
                <h3 className="font-semibold text-foreground">Scraping de Gestiones</h3>
                <p className="text-sm text-muted-foreground">Última ejecución: Hace 30 minutos</p>
              </div>
              <Button>Ejecutar</Button>
            </div>

            <div className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
              <div>
                <h3 className="font-semibold text-foreground">Scraping de Clientes</h3>
                <p className="text-sm text-muted-foreground">Última ejecución: Hace 1 hora</p>
              </div>
              <Button>Ejecutar</Button>
            </div>

            <div className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
              <div>
                <h3 className="font-semibold text-foreground">Scraping de Métricas</h3>
                <p className="text-sm text-muted-foreground">Última ejecución: Hace 2 horas</p>
              </div>
              <Button>Ejecutar</Button>
            </div>
          </div>
        </Card>
      </div>
    )
  }

  return null
}

"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useState } from "react"
import { ScrapingPanel } from "@/components/analistas/scraping/scraping-panel"

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

  const clearLogs = () => {
    setConsoleLogs([])
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

  const ConexionesInterface = ({ title, description }: { title: string; description: string }) => (
    <div className="p-6 space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-semibold text-foreground mb-1">{title}</h2>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>

      <div className="flex justify-center">
        <Card className="p-6 w-full max-w-4xl">
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
              <Label className="mb-3 block text-center">Opciones de Reporte</Label>
              <div className="flex flex-wrap gap-4 justify-center">
                {getSystemButtons().map((buttonName) => (
                  <Button
                    key={buttonName}
                    onClick={() =>
                      addLog(
                        `Botón presionado: ${buttonName} - Sistema: ${sistemaSeleccionado.toUpperCase()} - Período: ${fechaInicio} al ${fechaFin}`,
                      )
                    }
                    variant="outline"
                    size="lg"
                    className="min-w-[140px]"
                  >
                    {buttonName}
                  </Button>
                ))}
              </div>
            </div>
          )}

          {sistemaSeleccionado && (
            <div className="mt-6">
              <div className="flex items-center justify-between mb-2">
                <Label>Consola de Eventos</Label>
                <Button onClick={clearLogs} variant="ghost" size="sm">
                  Limpiar Consola
                </Button>
              </div>
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
    </div>
  )

  if (subSection === "conexiones") {
    return <ConexionesInterface title="Conexiones" description="Consulta de conexiones por rango de fechas" />
  }

  if (subSection === "campanas") {
    return <ConexionesInterface title="Campañas de Analistas" description="Consulta de campañas por rango de fechas" />
  }

  if (subSection === "scraping") {
    return <ScrapingPanel />
  }

  return null
}

"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { cn } from "@/lib/utils"
import type {
  ScrapingConfigFormProps,
  Platform,
  PlatformType,
  ScheduleInterval,
  SelectedPlatform,
} from "./types"

const PLATFORMS: Platform[] = [
  {
    id: "salesys",
    name: "SaleSys",
    options: [
      { id: "salesys_general", label: "Reporte General", value: "general" },
      { id: "salesys_agaso", label: "Agaso", value: "agaso" },
      { id: "salesys_clientes", label: "Exportar Clientes", value: "clientes" },
    ],
  },
  {
    id: "laraigo",
    name: "Laraigo",
    options: [
      { id: "laraigo_actividad", label: "Log de Actividad", value: "actividad" },
      { id: "laraigo_productividad", label: "Productividad", value: "productividad" },
      { id: "laraigo_errores", label: "Errores de Sistema", value: "errores" },
    ],
  },
  {
    id: "navicat",
    name: "Navicat",
    options: [
      { id: "navicat_conexiones", label: "Conexiones", value: "conexiones" },
      { id: "navicat_consultas", label: "Consultas SQL", value: "consultas" },
      { id: "navicat_backup", label: "Backup DB", value: "backup" },
    ],
  },
  {
    id: "360",
    name: "360",
    options: [
      { id: "360_ventas", label: "Reporte de Ventas", value: "ventas" },
      { id: "360_agentes", label: "Dashboard Agentes", value: "agentes" },
    ],
  },
]

const SCHEDULE_OPTIONS: { value: ScheduleInterval; label: string }[] = [
  { value: "now", label: "Ejecutar Ahora" },
  { value: "5min", label: "En 5 minutos" },
  { value: "10min", label: "En 10 minutos" },
  { value: "15min", label: "En 15 minutos" },
  { value: "30min", label: "En 30 minutos" },
  { value: "60min", label: "En 60 minutos" },
]

export function ScrapingConfigForm({ onExecute, isExecuting }: ScrapingConfigFormProps) {
  const getDefaultDate = () => {
    const today = new Date()
    return today.toISOString().split("T")[0]
  }

  const [fechaInicio, setFechaInicio] = useState(getDefaultDate())
  const [fechaFin, setFechaFin] = useState(getDefaultDate())
  const [schedule, setSchedule] = useState<ScheduleInterval>("now")
  const [selectedPlatforms, setSelectedPlatforms] = useState<Map<PlatformType, Set<string>>>(new Map())
  const [errors, setErrors] = useState<string[]>([])

  const validateDates = (): boolean => {
    const errors: string[] = []
    const inicio = new Date(fechaInicio)
    const fin = new Date(fechaFin)
    const today = new Date()
    const maxDaysAgo = new Date()
    maxDaysAgo.setDate(maxDaysAgo.getDate() - 30)

    if (fin < inicio) {
      errors.push("La fecha final debe ser mayor o igual a la fecha inicial")
    }

    if (inicio < maxDaysAgo) {
      errors.push("No puedes seleccionar fechas mayores a 30 dias atras")
    }

    if (fin > today) {
      errors.push("No puedes seleccionar fechas futuras")
    }

    setErrors(errors)
    return errors.length === 0
  }

  const togglePlatform = (platformId: PlatformType) => {
    const newSelected = new Map(selectedPlatforms)
    if (newSelected.has(platformId)) {
      newSelected.delete(platformId)
    } else {
      newSelected.set(platformId, new Set())
    }
    setSelectedPlatforms(newSelected)
  }

  const toggleOption = (platformId: PlatformType, optionId: string) => {
    const newSelected = new Map(selectedPlatforms)
    const platformOptions = newSelected.get(platformId) || new Set<string>()

    if (platformOptions.has(optionId)) {
      platformOptions.delete(optionId)
    } else {
      platformOptions.add(optionId)
    }

    if (platformOptions.size === 0) {
      newSelected.delete(platformId)
    } else {
      newSelected.set(platformId, platformOptions)
    }

    setSelectedPlatforms(newSelected)
  }

  const handleExecute = () => {
    if (!validateDates()) {
      return
    }

    if (selectedPlatforms.size === 0) {
      setErrors(["Debes seleccionar al menos una plataforma"])
      return
    }

    const platforms: SelectedPlatform[] = Array.from(selectedPlatforms.entries()).map(
      ([platformId, options]) => ({
        platformId,
        selectedOptions: Array.from(options),
      }),
    )

    onExecute({
      fechaInicio,
      fechaFin,
      platforms,
      schedule,
    })
  }

  return (
    <Card className="p-6">
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="space-y-2">
            <Label htmlFor="fecha-inicio">Fecha Inicio</Label>
            <Input
              id="fecha-inicio"
              type="date"
              value={fechaInicio}
              onChange={(e) => setFechaInicio(e.target.value)}
              disabled={isExecuting}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="fecha-fin">Fecha Fin</Label>
            <Input
              id="fecha-fin"
              type="date"
              value={fechaFin}
              onChange={(e) => setFechaFin(e.target.value)}
              disabled={isExecuting}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="schedule">Programar Ejecucion</Label>
            <Select value={schedule} onValueChange={(value) => setSchedule(value as ScheduleInterval)}>
              <SelectTrigger id="schedule" disabled={isExecuting}>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {SCHEDULE_OPTIONS.map((option) => (
                  <SelectItem key={option.value} value={option.value}>
                    {option.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        {errors.length > 0 && (
          <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4">
            <ul className="list-disc list-inside space-y-1">
              {errors.map((error, index) => (
                <li key={index} className="text-sm text-destructive">
                  {error}
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="space-y-4">
          <Label className="text-base font-semibold">Plataformas y Reportes</Label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {PLATFORMS.map((platform) => {
              const isPlatformSelected = selectedPlatforms.has(platform.id)
              const selectedOptions = selectedPlatforms.get(platform.id) || new Set<string>()

              return (
                <div
                  key={platform.id}
                  className={cn(
                    "border rounded-lg p-4 transition-colors",
                    isPlatformSelected ? "border-primary bg-primary/5" : "border-border",
                  )}
                >
                  <div className="flex items-center space-x-2 mb-3">
                    <Checkbox
                      id={platform.id}
                      checked={isPlatformSelected}
                      onCheckedChange={() => togglePlatform(platform.id)}
                      disabled={isExecuting}
                    />
                    <label
                      htmlFor={platform.id}
                      className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                    >
                      {platform.name}
                    </label>
                  </div>

                  {isPlatformSelected && (
                    <div className="ml-6 space-y-2">
                      {platform.options.map((option) => (
                        <div key={option.id} className="flex items-center space-x-2">
                          <Checkbox
                            id={option.id}
                            checked={selectedOptions.has(option.id)}
                            onCheckedChange={() => toggleOption(platform.id, option.id)}
                            disabled={isExecuting}
                          />
                          <label
                            htmlFor={option.id}
                            className="text-sm text-muted-foreground leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 cursor-pointer"
                          >
                            {option.label}
                          </label>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>

        <div className="flex justify-center pt-4">
          <Button size="lg" onClick={handleExecute} disabled={isExecuting} className="min-w-[200px]">
            {isExecuting ? "Ejecutando..." : "Ejecutar Scraping"}
          </Button>
        </div>
      </div>
    </Card>
  )
}

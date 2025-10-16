"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import type { ScrapingExecutionProps } from "./types"

export function ScrapingExecution({ job, onCancel }: ScrapingExecutionProps) {
  if (!job || job.status !== "in_progress") {
    return null
  }

  const progress = job.progress || 0
  const currentTask = job.currentTask || "Iniciando scraping..."

  const platformNames = job.config.platforms
    .map((p) => {
      const platformLabels: Record<string, string> = {
        salesys: "SaleSys",
        laraigo: "Laraigo",
        navicat: "Navicat",
        "360": "360",
      }
      return platformLabels[p.platformId] || p.platformId
    })
    .join(", ")

  return (
    <Card className="p-6 border-warning bg-warning/5">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-foreground flex items-center gap-2">
              <span className="inline-block w-2 h-2 bg-warning rounded-full animate-pulse"></span>
              Scraping en Ejecucion
            </h3>
            <p className="text-sm text-muted-foreground mt-1">Plataformas: {platformNames}</p>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">{currentTask}</span>
            <span className="font-medium text-foreground">{progress}%</span>
          </div>
          <Progress value={progress} className="h-3" />
        </div>

        <div className="flex items-center justify-between pt-2">
          <div className="text-sm text-muted-foreground">
            <p>
              Periodo: {job.config.fechaInicio} al {job.config.fechaFin}
            </p>
          </div>

          <Button variant="destructive" size="sm" onClick={onCancel}>
            Cancelar Scraping
          </Button>
        </div>
      </div>
    </Card>
  )
}

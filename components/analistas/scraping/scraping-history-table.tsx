"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Eye, RotateCw } from "lucide-react"
import type { ScrapingHistoryTableProps, ScrapingStatus } from "./types"

export function ScrapingHistoryTable({ jobs, onReExecute, onViewDetails }: ScrapingHistoryTableProps) {
  const getStatusVariant = (status: ScrapingStatus): "success" | "warning" | "pending" | "destructive" => {
    switch (status) {
      case "completed":
        return "success"
      case "in_progress":
        return "warning"
      case "pending":
        return "pending"
      case "error":
        return "destructive"
      default:
        return "pending"
    }
  }

  const getStatusLabel = (status: ScrapingStatus): string => {
    switch (status) {
      case "completed":
        return "Completado"
      case "in_progress":
        return "En Proceso"
      case "pending":
        return "Pendiente"
      case "error":
        return "Error"
      default:
        return status
    }
  }

  const formatDate = (date: Date): string => {
    return new Date(date).toLocaleString("es-ES", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  if (jobs.length === 0) {
    return (
      <Card className="p-6">
        <div className="text-center py-8">
          <p className="text-muted-foreground">No hay scrapings ejecutados aun</p>
        </div>
      </Card>
    )
  }

  return (
    <Card className="p-6">
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-foreground">Historial de Scrapings</h3>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Fecha/Hora</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Plataformas</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Archivos</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Estado</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-foreground">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {jobs.map((job) => {
                const platformLabels: Record<string, string> = {
                  salesys: "SaleSys",
                  laraigo: "Laraigo",
                  navicat: "Navicat",
                  "360": "360",
                  ipcc: "IPCC",
                  portal_sbs: "Portal SBS",
                }

                const platformsText = job.config.platforms
                  .map((p) => {
                    const name = platformLabels[p.platformId] || p.platformId
                    const count = p.selectedOptions.length
                    return `${name} (${count})`
                  })
                  .join(", ")

                const filesText =
                  job.generatedFiles.length > 0
                    ? job.generatedFiles.map((f) => f.fileName).join(", ")
                    : "Sin archivos"

                return (
                  <tr key={job.id} className="border-b border-border hover:bg-secondary/50 transition-colors">
                    <td className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap">
                      {formatDate(job.executedAt)}
                    </td>
                    <td className="py-3 px-4 text-sm text-foreground">{platformsText}</td>
                    <td className="py-3 px-4 text-sm text-muted-foreground max-w-[200px] truncate" title={filesText}>
                      {filesText}
                    </td>
                    <td className="py-3 px-4">
                      <Badge variant={getStatusVariant(job.status)}>{getStatusLabel(job.status)}</Badge>
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        {onViewDetails && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => onViewDetails(job)}
                            className="h-8 w-8 p-0"
                            title="Ver detalles"
                          >
                            <Eye className="h-4 w-4" />
                          </Button>
                        )}
                        {onReExecute && job.status !== "in_progress" && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => onReExecute(job)}
                            className="h-8 w-8 p-0"
                            title="Re-ejecutar"
                          >
                            <RotateCw className="h-4 w-4" />
                          </Button>
                        )}
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>

        <div className="text-sm text-muted-foreground text-center pt-2">
          Mostrando los ultimos {jobs.length} scrapings
        </div>
      </div>
    </Card>
  )
}

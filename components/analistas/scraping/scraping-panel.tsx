"use client"

import { useState } from "react"
import { ScrapingConfigForm } from "./scraping-config-form"
import { ScrapingExecution } from "./scraping-execution"
import { ScrapingHistoryTable } from "./scraping-history-table"
import type { ScrapingConfig, ScrapingJob } from "./types"

const MOCK_HISTORY: ScrapingJob[] = [
  {
    id: "1",
    executedAt: new Date(Date.now() - 3600000),
    status: "completed",
    config: {
      fechaInicio: "2025-10-15",
      fechaFin: "2025-10-16",
      platforms: [
        { platformId: "salesys", selectedOptions: ["salesys_general", "salesys_agaso"] },
        { platformId: "laraigo", selectedOptions: ["laraigo_actividad"] },
      ],
      schedule: "now",
    },
    generatedFiles: [
      { fileName: "ventas_salesys.xlsx", filePath: "/exports/ventas_salesys.xlsx", platform: "salesys" },
      { fileName: "logs_laraigo.csv", filePath: "/exports/logs_laraigo.csv", platform: "laraigo" },
    ],
  },
  {
    id: "2",
    executedAt: new Date(Date.now() - 7200000),
    status: "completed",
    config: {
      fechaInicio: "2025-10-14",
      fechaFin: "2025-10-15",
      platforms: [{ platformId: "navicat", selectedOptions: ["navicat_conexiones", "navicat_consultas"] }],
      schedule: "now",
    },
    generatedFiles: [{ fileName: "db_backup.sql", filePath: "/exports/db_backup.sql", platform: "navicat" }],
  },
  {
    id: "3",
    executedAt: new Date(Date.now() - 10800000),
    status: "error",
    config: {
      fechaInicio: "2025-10-13",
      fechaFin: "2025-10-14",
      platforms: [{ platformId: "360", selectedOptions: ["360_ventas"] }],
      schedule: "now",
    },
    generatedFiles: [],
    errorMessage: "Error de conexion con el servidor 360",
  },
]

export function ScrapingPanel() {
  const [currentJob, setCurrentJob] = useState<ScrapingJob | null>(null)
  const [historyJobs, setHistoryJobs] = useState<ScrapingJob[]>(MOCK_HISTORY)

  const handleExecute = (config: ScrapingConfig) => {
    console.log("Ejecutando scraping con configuracion:", config)

    const newJob: ScrapingJob = {
      id: Date.now().toString(),
      executedAt: new Date(),
      status: "in_progress",
      config,
      generatedFiles: [],
      progress: 0,
      currentTask: "Iniciando scraping...",
    }

    setCurrentJob(newJob)
    simulateProgress(newJob)
  }

  const simulateProgress = (job: ScrapingJob) => {
    let progress = 0
    const tasks = [
      "Conectando con servidores...",
      "Autenticando credenciales...",
      "Extrayendo datos...",
      "Procesando informacion...",
      "Generando archivos...",
      "Finalizando...",
    ]

    const interval = setInterval(() => {
      progress += 20
      const taskIndex = Math.floor(progress / 20)

      setCurrentJob((prev) =>
        prev
          ? {
              ...prev,
              progress,
              currentTask: tasks[Math.min(taskIndex, tasks.length - 1)],
            }
          : null,
      )

      if (progress >= 100) {
        clearInterval(interval)
        const completedJob: ScrapingJob = {
          ...job,
          status: "completed",
          progress: 100,
          generatedFiles: [
            {
              fileName: "scraping_result.xlsx",
              filePath: "/exports/scraping_result.xlsx",
              platform: job.config.platforms[0].platformId,
            },
          ],
        }
        setHistoryJobs((prev) => [completedJob, ...prev].slice(0, 10))
        setCurrentJob(null)
      }
    }, 1500)
  }

  const handleCancel = () => {
    console.log("Cancelando scraping...")
    if (currentJob) {
      const cancelledJob: ScrapingJob = {
        ...currentJob,
        status: "error",
        errorMessage: "Cancelado por el usuario",
      }
      setHistoryJobs((prev) => [cancelledJob, ...prev].slice(0, 10))
      setCurrentJob(null)
    }
  }

  const handleReExecute = (job: ScrapingJob) => {
    console.log("Re-ejecutando scraping:", job)
    handleExecute(job.config)
  }

  const handleViewDetails = (job: ScrapingJob) => {
    console.log("Ver detalles de:", job)
    alert(
      `Detalles del scraping:\n\nID: ${job.id}\nFecha: ${job.executedAt}\nEstado: ${job.status}\nArchivos: ${job.generatedFiles.length}`,
    )
  }

  return (
    <div className="p-6 space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-semibold text-foreground mb-1">Scraping de Datos</h2>
        <p className="text-sm text-muted-foreground">Extraccion automatizada de informacion</p>
      </div>

      <ScrapingConfigForm onExecute={handleExecute} isExecuting={currentJob !== null} />

      {currentJob && <ScrapingExecution job={currentJob} onCancel={handleCancel} />}

      <ScrapingHistoryTable jobs={historyJobs} onReExecute={handleReExecute} onViewDetails={handleViewDetails} />
    </div>
  )
}

// Types - Modulo de Scraping

export type ScrapingStatus = "completed" | "in_progress" | "pending" | "error"

export type ScheduleInterval = "now" | "5min" | "10min" | "15min" | "30min" | "60min"

export type PlatformType = "salesys" | "laraigo" | "navicat" | "360" | "ipcc" | "portal_sbs"

export interface PlatformOption {
  id: string
  label: string
  value: string
}

export interface Platform {
  id: PlatformType
  name: string
  options: PlatformOption[]
}

export interface SelectedPlatform {
  platformId: PlatformType
  selectedOptions: string[]
}

export interface ScrapingConfig {
  fechaInicio: string
  fechaFin: string
  platforms: SelectedPlatform[]
  schedule: ScheduleInterval
}

export interface GeneratedFile {
  fileName: string
  filePath: string
  size?: string
  platform: PlatformType
}

export interface ScrapingJob {
  id: string
  executedAt: Date
  config: ScrapingConfig
  status: ScrapingStatus
  generatedFiles: GeneratedFile[]
  errorMessage?: string
  progress?: number
  currentTask?: string
}

export interface ExecutionState {
  isRunning: boolean
  currentJob: ScrapingJob | null
  canCancel: boolean
}

export interface ScrapingConfigFormProps {
  onExecute: (config: ScrapingConfig) => void
  isExecuting: boolean
}

export interface ScrapingExecutionProps {
  job: ScrapingJob | null
  onCancel: () => void
}

export interface ScrapingHistoryTableProps {
  jobs: ScrapingJob[]
  onReExecute?: (job: ScrapingJob) => void
  onViewDetails?: (job: ScrapingJob) => void
}

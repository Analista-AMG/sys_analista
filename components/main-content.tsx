"use client"

import { InicioView } from "@/components/views/inicio-view"
import { CampanasView } from "@/components/views/campanas-view"
import { AnalistasView } from "@/components/views/analistas-view"
import { ConfiguracionView } from "@/components/views/configuracion-view"
import { X } from "lucide-react"
import { Button } from "@/components/ui/button"

interface MainContentProps {
  activeSection: string | null
  activeSubSection: string | null
  openTabs: Array<{ section: string; subSection: string; id: string }>
  onCloseTab: (tabId: string) => void
  onTabClick: (section: string, subSection: string) => void
  onOpenCampaign?: (campaignId: string) => void
}

const getSectionLabel = (section: string, subSection: string) => {
  const labels: Record<string, Record<string, string>> = {
    inicio: {
      main: "Inicio",
    },
    campanas: {
      activaciones: "Activaciones",
      aghaso: "Aghaso",
      delivery: "Delivery",
      "foto-corporativo": "Foto Corporativo",
      "foto-alambrico": "Foto Alambrico",
      nps: "NPS",
      multiskill: "MultiSkill",
      "programacion-seg-fija": "Programación y Seg Fija",
      "soporte-venta-fija": "Soporte Venta Fija y Fibra",
      validaciones: "Validaciones",
    },
    analistas: {
      lista: "Lista de Analistas",
      rendimiento: "Rendimiento",
      horarios: "Horarios",
    },
    configuracion: {
      general: "General",
      usuarios: "Usuarios",
      integraciones: "Integraciones",
    },
  }
  return labels[section]?.[subSection] || subSection
}

export function MainContent({
  activeSection,
  activeSubSection,
  openTabs,
  onCloseTab,
  onTabClick,
  onOpenCampaign,
}: MainContentProps) {
  if (!activeSection || !activeSubSection) {
    return (
      <main className="flex-1 flex items-center justify-center bg-background">
        <div className="text-center">
          <h2 className="text-2xl font-semibold text-foreground mb-2">Bienvenido a Sys-Analistas</h2>
          <p className="text-muted-foreground">Selecciona una opción del menú lateral para comenzar</p>
        </div>
      </main>
    )
  }

  return (
    <main className="flex-1 flex flex-col bg-background">
      {openTabs.length > 0 && (
        <div className="border-b border-border bg-card">
          <div className="flex items-center gap-1 px-4 overflow-x-auto">
            {openTabs.map((tab) => {
              const isActive = activeSection === tab.section && activeSubSection === tab.subSection
              return (
                <div
                  key={tab.id}
                  className={`flex items-center gap-2 px-4 py-3 border-b-2 transition-colors cursor-pointer group ${
                    isActive
                      ? "border-primary bg-secondary/50 text-foreground"
                      : "border-transparent text-muted-foreground hover:text-foreground hover:bg-secondary/30"
                  }`}
                  onClick={() => onTabClick(tab.section, tab.subSection)}
                >
                  <span className="text-sm font-medium whitespace-nowrap">
                    {getSectionLabel(tab.section, tab.subSection)}
                  </span>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-4 w-4 p-0 hover:bg-destructive/20 rounded-sm opacity-60 hover:opacity-100"
                    onClick={(e) => {
                      e.stopPropagation()
                      onCloseTab(tab.id)
                    }}
                  >
                    <X className="h-3 w-3" />
                  </Button>
                </div>
              )
            })}
          </div>
        </div>
      )}

      <div className="flex-1 overflow-auto">
        {activeSection === "inicio" && <InicioView subSection={activeSubSection} onOpenCampaign={onOpenCampaign} />}
        {activeSection === "campanas" && <CampanasView subSection={activeSubSection} />}
        {activeSection === "analistas" && <AnalistasView subSection={activeSubSection} />}
        {activeSection === "configuracion" && <ConfiguracionView subSection={activeSubSection} />}
      </div>
    </main>
  )
}

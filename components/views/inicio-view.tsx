"use client"

import { Card } from "@/components/ui/card"
import { Zap, Package, Truck, Camera, Cable, Star, Users, Calendar, Phone, CheckCircle } from "lucide-react"

interface InicioViewProps {
  subSection: string
  onOpenCampaign?: (campaignId: string) => void
}

export function InicioView({ subSection, onOpenCampaign }: InicioViewProps) {
  const campaigns = [
    { id: "activaciones", label: "Activaciones", icon: Zap, color: "bg-blue-500" },
    { id: "aghaso", label: "Aghaso", icon: Package, color: "bg-purple-500" },
    { id: "delivery", label: "Delivery", icon: Truck, color: "bg-green-500" },
    { id: "foto-corporativo", label: "Foto Corporativo", icon: Camera, color: "bg-orange-500" },
    { id: "foto-alambrico", label: "Foto Alambrico", icon: Cable, color: "bg-cyan-500" },
    { id: "nps", label: "NPS", icon: Star, color: "bg-yellow-500" },
    { id: "multiskill", label: "MultiSkill", icon: Users, color: "bg-pink-500" },
    { id: "programacion-seg-fija", label: "Programación y Seg Fija", icon: Calendar, color: "bg-indigo-500" },
    { id: "soporte-venta-fija", label: "Soporte Venta Fija", icon: Phone, color: "bg-red-500" },
    { id: "validaciones", label: "Validaciones", icon: CheckCircle, color: "bg-teal-500" },
  ]

  const handleCampaignClick = (campaignId: string) => {
    if (onOpenCampaign) {
      onOpenCampaign(campaignId)
    }
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-foreground mb-1">Inicio</h2>
        <p className="text-sm text-muted-foreground">Selecciona una campaña para comenzar</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {campaigns.map((campaign) => {
          const Icon = campaign.icon
          return (
            <Card
              key={campaign.id}
              className="p-6 cursor-pointer hover:shadow-lg transition-all hover:scale-105 group"
              onClick={() => handleCampaignClick(campaign.id)}
            >
              <div className="flex flex-col items-center text-center gap-4">
                <div
                  className={`w-16 h-16 ${campaign.color} rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform`}
                >
                  <Icon className="w-8 h-8 text-white" />
                </div>
                <h3 className="text-sm font-semibold text-foreground leading-tight">{campaign.label}</h3>
              </div>
            </Card>
          )
        })}
      </div>

      <Card className="p-6 mt-8">
        <h3 className="text-lg font-semibold text-foreground mb-4">Resumen del Día</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div>
            <p className="text-sm text-muted-foreground mb-2">Total Analistas</p>
            <p className="text-2xl font-bold text-foreground">24</p>
            <p className="text-xs text-green-500 mt-1">Activos</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground mb-2">Gestiones Hoy</p>
            <p className="text-2xl font-bold text-foreground">156</p>
            <p className="text-xs text-green-500 mt-1">+12% vs ayer</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground mb-2">Tiempo Promedio</p>
            <p className="text-2xl font-bold text-foreground">8.5 min</p>
            <p className="text-xs text-muted-foreground mt-1">Por gestión</p>
          </div>
          <div>
            <p className="text-sm text-muted-foreground mb-2">Efectividad</p>
            <p className="text-2xl font-bold text-foreground">87%</p>
            <p className="text-xs text-green-500 mt-1">+3% vs ayer</p>
          </div>
        </div>
      </Card>
    </div>
  )
}

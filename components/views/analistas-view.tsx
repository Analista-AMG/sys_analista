"use client"

import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { User, Clock, CheckCircle, XCircle, Activity } from "lucide-react"
import { useState } from "react"

interface AnalistasViewProps {
  subSection: string
}

export function AnalistasView({ subSection }: AnalistasViewProps) {
  const [activeTab, setActiveTab] = useState("salesys")

  if (subSection === "lista") {
    return (
      <div className="p-6 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-foreground mb-1">Lista de Analistas</h2>
            <p className="text-sm text-muted-foreground">Gestión de analistas del sistema</p>
          </div>
          <Button>Agregar Analista</Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Card key={i} className="p-6">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
                  <User className="w-6 h-6 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-foreground">Analista {i}</h3>
                  <p className="text-sm text-muted-foreground">analista{i}@sys.com</p>
                  <div className="flex items-center gap-2 mt-3">
                    <Badge variant={i % 2 === 0 ? "default" : "secondary"}>
                      {i % 2 === 0 ? "Activo" : "Disponible"}
                    </Badge>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  if (subSection === "rendimiento") {
    return (
      <div className="p-6 space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground mb-1">Rendimiento</h2>
          <p className="text-sm text-muted-foreground">Métricas de rendimiento de analistas</p>
        </div>

        <div className="space-y-4">
          {[1, 2, 3, 4, 5].map((i) => (
            <Card key={i} className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">Analista {i}</h3>
                    <p className="text-sm text-muted-foreground">Campaña: Activaciones</p>
                  </div>
                </div>
                <div className="flex items-center gap-6">
                  <div className="text-center">
                    <p className="text-sm text-muted-foreground">Gestiones</p>
                    <p className="text-lg font-bold text-foreground">{20 + i * 5}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-muted-foreground">Efectividad</p>
                    <p className="text-lg font-bold text-foreground">{80 + i}%</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-muted-foreground">Tiempo Prom.</p>
                    <p className="text-lg font-bold text-foreground">{5 + i} min</p>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  if (subSection === "horarios") {
    return (
      <div className="p-6 space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground mb-1">Horarios</h2>
          <p className="text-sm text-muted-foreground">Gestión de horarios de analistas</p>
        </div>

        <Card className="p-6">
          <div className="space-y-4">
            {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                    <User className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-foreground">Analista {i}</h3>
                    <p className="text-sm text-muted-foreground">Turno: Mañana</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Clock className="w-4 h-4 text-muted-foreground" />
                  <span className="text-sm text-foreground">08:00 - 16:00</span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    )
  }

  if (subSection === "conexiones") {
    return (
      <div className="p-6 space-y-6">
        <div>
          <h2 className="text-2xl font-semibold text-foreground mb-1">Conexiones</h2>
          <p className="text-sm text-muted-foreground">Estado de conexiones a sistemas externos</p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="salesys">SaleSys</TabsTrigger>
            <TabsTrigger value="genesys">Genesys</TabsTrigger>
            <TabsTrigger value="ipcc">IPCC</TabsTrigger>
          </TabsList>

          <TabsContent value="salesys" className="space-y-4 mt-6">
            <Card className="p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-blue-500/10 rounded-lg flex items-center justify-center">
                    <Activity className="w-6 h-6 text-blue-500" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-foreground">SaleSys</h3>
                    <p className="text-sm text-muted-foreground">Sistema de gestión de ventas</p>
                  </div>
                </div>
                <Badge className="bg-green-500/10 text-green-600 border-green-500/20">
                  <CheckCircle className="w-3 h-3 mr-1" />
                  Conectado
                </Badge>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-secondary/50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-1">Estado del Servidor</p>
                  <p className="text-lg font-semibold text-foreground">Operativo</p>
                </div>
                <div className="p-4 bg-secondary/50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-1">Última Sincronización</p>
                  <p className="text-lg font-semibold text-foreground">Hace 2 min</p>
                </div>
                <div className="p-4 bg-secondary/50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-1">Usuarios Conectados</p>
                  <p className="text-lg font-semibold text-foreground">24</p>
                </div>
                <div className="p-4 bg-secondary/50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-1">Latencia</p>
                  <p className="text-lg font-semibold text-foreground">45 ms</p>
                </div>
              </div>
            </Card>
          </TabsContent>

          <TabsContent value="genesys" className="space-y-4 mt-6">
            <Card className="p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-purple-500/10 rounded-lg flex items-center justify-center">
                    <Activity className="w-6 h-6 text-purple-500" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-foreground">Genesys</h3>
                    <p className="text-sm text-muted-foreground">Plataforma de contact center</p>
                  </div>
                </div>
                <Badge className="bg-green-500/10 text-green-600 border-green-500/20">
                  <CheckCircle className="w-3 h-3 mr-1" />
                  Conectado
                </Badge>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-secondary/50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-1">Estado del Servidor</p>
                  <p className="text-lg font-semibold text-foreground">Operativo</p>
                </div>
                <div className="p-4 bg-secondary/50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-1">Última Sincronización</p>
                  <p className="text-lg font-semibold text-foreground">Hace 1 min</p>
                </div>
                <div className="p-4 bg-secondary/50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-1">Agentes Activos</p>
                  <p className="text-lg font-semibold text-foreground">18</p>
                </div>
                <div className="p-4 bg-secondary/50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-1">Llamadas en Cola</p>
                  <p className="text-lg font-semibold text-foreground">3</p>
                </div>
              </div>
            </Card>
          </TabsContent>

          <TabsContent value="ipcc" className="space-y-4 mt-6">
            <Card className="p-6">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-orange-500/10 rounded-lg flex items-center justify-center">
                    <Activity className="w-6 h-6 text-orange-500" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-foreground">IPCC</h3>
                    <p className="text-sm text-muted-foreground">Sistema de telefonía IP</p>
                  </div>
                </div>
                <Badge className="bg-yellow-500/10 text-yellow-600 border-yellow-500/20">
                  <XCircle className="w-3 h-3 mr-1" />
                  Reconectando
                </Badge>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-secondary/50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-1">Estado del Servidor</p>
                  <p className="text-lg font-semibold text-foreground">Reiniciando</p>
                </div>
                <div className="p-4 bg-secondary/50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-1">Última Sincronización</p>
                  <p className="text-lg font-semibold text-foreground">Hace 15 min</p>
                </div>
                <div className="p-4 bg-secondary/50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-1">Líneas Disponibles</p>
                  <p className="text-lg font-semibold text-foreground">12/15</p>
                </div>
                <div className="p-4 bg-secondary/50 rounded-lg">
                  <p className="text-sm text-muted-foreground mb-1">Intentos de Reconexión</p>
                  <p className="text-lg font-semibold text-foreground">2</p>
                </div>
              </div>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    )
  }

  return null
}

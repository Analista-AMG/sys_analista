"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"

interface ConfiguracionViewProps {
  subSection: string
}

export function ConfiguracionView({ subSection }: ConfiguracionViewProps) {
  const [activeTab, setActiveTab] = useState("empresa")

  if (subSection === "general") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="empresa"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Empresa
              </TabsTrigger>
              <TabsTrigger
                value="sistema"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Sistema
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="empresa" className="m-0 p-6 space-y-6 max-w-4xl">
              <div>
                <h2 className="text-3xl font-semibold text-balance">Configuración General</h2>
                <p className="text-muted-foreground mt-1">Ajusta las preferencias del sistema</p>
              </div>

              <Card className="p-6 bg-card border-border">
                <h3 className="text-lg font-semibold mb-4">Información de la Empresa</h3>
                <div className="space-y-4">
                  <div className="grid gap-2">
                    <Label htmlFor="company">Nombre de la Empresa</Label>
                    <Input id="company" defaultValue="CallCenter Pro" />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="email">Email de Contacto</Label>
                    <Input id="email" type="email" defaultValue="contacto@callcenter.com" />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="phone">Teléfono Principal</Label>
                    <Input id="phone" defaultValue="+34 900 123 456" />
                  </div>
                </div>
              </Card>

              <div className="flex justify-end gap-4">
                <Button variant="outline">Cancelar</Button>
                <Button>Guardar Cambios</Button>
              </div>
            </TabsContent>

            <TabsContent value="sistema" className="m-0 p-6 space-y-6 max-w-4xl">
              <div>
                <h2 className="text-3xl font-semibold text-balance">Configuración del Sistema</h2>
                <p className="text-muted-foreground mt-1">Parámetros técnicos</p>
              </div>

              <Card className="p-6 bg-card border-border">
                <p className="text-muted-foreground">Configuración del sistema...</p>
              </Card>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  if (subSection === "notificaciones") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="empresa"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Preferencias
              </TabsTrigger>
              <TabsTrigger
                value="canales"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Canales
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="empresa" className="m-0 p-6 space-y-6 max-w-4xl">
              <div>
                <h2 className="text-3xl font-semibold text-balance">Preferencias de Notificaciones</h2>
                <p className="text-muted-foreground mt-1">Configura tus preferencias de notificaciones</p>
              </div>

              <Card className="p-6 bg-card border-border">
                <h3 className="text-lg font-semibold mb-4">Notificaciones</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">Notificaciones de Llamadas</p>
                      <p className="text-sm text-muted-foreground">Recibe alertas de llamadas entrantes</p>
                    </div>
                    <Switch defaultChecked />
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">Reportes Diarios</p>
                      <p className="text-sm text-muted-foreground">Enviar resumen diario por email</p>
                    </div>
                    <Switch defaultChecked />
                  </div>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium">Alertas de Rendimiento</p>
                      <p className="text-sm text-muted-foreground">Notificar cuando el rendimiento baje</p>
                    </div>
                    <Switch />
                  </div>
                </div>
              </Card>

              <div className="flex justify-end gap-4">
                <Button variant="outline">Cancelar</Button>
                <Button>Guardar Cambios</Button>
              </div>
            </TabsContent>

            <TabsContent value="canales" className="m-0 p-6 space-y-6 max-w-4xl">
              <div>
                <h2 className="text-3xl font-semibold text-balance">Canales de Notificación</h2>
                <p className="text-muted-foreground mt-1">Configura los canales de comunicación</p>
              </div>

              <Card className="p-6 bg-card border-border">
                <p className="text-muted-foreground">Configuración de canales...</p>
              </Card>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  if (subSection === "horarios") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="empresa"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Operación
              </TabsTrigger>
              <TabsTrigger
                value="excepciones"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Excepciones
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="empresa" className="m-0 p-6 space-y-6 max-w-4xl">
              <div>
                <h2 className="text-3xl font-semibold text-balance">Horarios de Operación</h2>
                <p className="text-muted-foreground mt-1">Define los horarios de atención</p>
              </div>

              <Card className="p-6 bg-card border-border">
                <h3 className="text-lg font-semibold mb-4">Horario de Operación</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="start">Hora de Inicio</Label>
                    <Input id="start" type="time" defaultValue="09:00" />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="end">Hora de Cierre</Label>
                    <Input id="end" type="time" defaultValue="18:00" />
                  </div>
                </div>
              </Card>

              <div className="flex justify-end gap-4">
                <Button variant="outline">Cancelar</Button>
                <Button>Guardar Cambios</Button>
              </div>
            </TabsContent>

            <TabsContent value="excepciones" className="m-0 p-6 space-y-6 max-w-4xl">
              <div>
                <h2 className="text-3xl font-semibold text-balance">Excepciones de Horario</h2>
                <p className="text-muted-foreground mt-1">Días festivos y horarios especiales</p>
              </div>

              <Card className="p-6 bg-card border-border">
                <p className="text-muted-foreground">Gestión de excepciones...</p>
              </Card>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  return null
}

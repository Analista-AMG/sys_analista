"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search, Plus, Phone, Mail, MapPin } from "lucide-react"

interface ClientesViewProps {
  subSection: string
}

export function ClientesView({ subSection }: ClientesViewProps) {
  const [activeTab, setActiveTab] = useState("todos")

  const clientes = [
    {
      id: 1,
      nombre: "Juan Pérez",
      email: "juan@email.com",
      telefono: "+34 600 123 456",
      ciudad: "Madrid",
      llamadas: 12,
      ultimaLlamada: "2024-01-15",
    },
    {
      id: 2,
      nombre: "Ana Martínez",
      email: "ana@email.com",
      telefono: "+34 600 234 567",
      ciudad: "Barcelona",
      llamadas: 8,
      ultimaLlamada: "2024-01-14",
    },
    {
      id: 3,
      nombre: "Pedro Gómez",
      email: "pedro@email.com",
      telefono: "+34 600 345 678",
      ciudad: "Valencia",
      llamadas: 15,
      ultimaLlamada: "2024-01-16",
    },
    {
      id: 4,
      nombre: "Sofía Torres",
      email: "sofia@email.com",
      telefono: "+34 600 456 789",
      ciudad: "Sevilla",
      llamadas: 6,
      ultimaLlamada: "2024-01-13",
    },
    {
      id: 5,
      nombre: "Miguel Ruiz",
      email: "miguel@email.com",
      telefono: "+34 600 567 890",
      ciudad: "Bilbao",
      llamadas: 20,
      ultimaLlamada: "2024-01-16",
    },
  ]

  if (subSection === "lista") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="todos"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Todos
              </TabsTrigger>
              <TabsTrigger
                value="activos"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Activos
              </TabsTrigger>
              <TabsTrigger
                value="inactivos"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Inactivos
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="todos" className="m-0 p-6 space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Lista de Clientes</h2>
                  <p className="text-muted-foreground mt-1">Gestiona tu base de datos de clientes</p>
                </div>
                <Button className="gap-2">
                  <Plus className="w-4 h-4" />
                  Nuevo Cliente
                </Button>
              </div>

              <Card className="p-4 bg-card border-border">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="Buscar clientes por nombre, email o teléfono..."
                    className="pl-10 bg-background"
                  />
                </div>
              </Card>

              <Card className="bg-card border-border overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-secondary/50 border-b border-border">
                      <tr>
                        <th className="text-left p-4 text-sm font-medium text-muted-foreground">Cliente</th>
                        <th className="text-left p-4 text-sm font-medium text-muted-foreground">Contacto</th>
                        <th className="text-left p-4 text-sm font-medium text-muted-foreground">Ubicación</th>
                        <th className="text-left p-4 text-sm font-medium text-muted-foreground">Llamadas</th>
                        <th className="text-left p-4 text-sm font-medium text-muted-foreground">Última Llamada</th>
                        <th className="text-left p-4 text-sm font-medium text-muted-foreground">Acciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      {clientes.map((cliente) => (
                        <tr key={cliente.id} className="border-b border-border hover:bg-secondary/30 transition-colors">
                          <td className="p-4">
                            <div className="flex items-center gap-3">
                              <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                                <span className="text-sm font-semibold text-primary">
                                  {cliente.nombre
                                    .split(" ")
                                    .map((n) => n[0])
                                    .join("")}
                                </span>
                              </div>
                              <div>
                                <p className="font-medium">{cliente.nombre}</p>
                                <p className="text-xs text-muted-foreground">ID: {cliente.id}</p>
                              </div>
                            </div>
                          </td>
                          <td className="p-4">
                            <div className="space-y-1">
                              <div className="flex items-center gap-2 text-sm">
                                <Phone className="w-3 h-3 text-muted-foreground" />
                                {cliente.telefono}
                              </div>
                              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                                <Mail className="w-3 h-3" />
                                {cliente.email}
                              </div>
                            </div>
                          </td>
                          <td className="p-4">
                            <div className="flex items-center gap-2 text-sm">
                              <MapPin className="w-3 h-3 text-muted-foreground" />
                              {cliente.ciudad}
                            </div>
                          </td>
                          <td className="p-4">
                            <span className="text-sm font-medium">{cliente.llamadas}</span>
                          </td>
                          <td className="p-4">
                            <span className="text-sm text-muted-foreground">{cliente.ultimaLlamada}</span>
                          </td>
                          <td className="p-4">
                            <Button variant="ghost" size="sm" className="gap-2">
                              <Phone className="w-4 h-4" />
                              Llamar
                            </Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </Card>
            </TabsContent>

            <TabsContent value="activos" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Clientes Activos</h2>
                  <p className="text-muted-foreground mt-1">Clientes con actividad reciente</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Lista de clientes activos...</p>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="inactivos" className="m-0 p-6">
              <div className="space-y-6">
                <div>
                  <h2 className="text-3xl font-semibold text-balance">Clientes Inactivos</h2>
                  <p className="text-muted-foreground mt-1">Clientes sin actividad reciente</p>
                </div>
                <Card className="p-6 bg-card border-border">
                  <p className="text-muted-foreground">Lista de clientes inactivos...</p>
                </Card>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  if (subSection === "nuevo") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="todos"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Información Básica
              </TabsTrigger>
              <TabsTrigger
                value="contacto"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Contacto
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="todos" className="m-0 p-6 space-y-6 max-w-2xl">
              <div>
                <h2 className="text-3xl font-semibold text-balance">Nuevo Cliente</h2>
                <p className="text-muted-foreground mt-1">Agrega un nuevo cliente a la base de datos</p>
              </div>
              <Card className="p-6 bg-card border-border">
                <p className="text-muted-foreground">Formulario de información básica...</p>
              </Card>
            </TabsContent>

            <TabsContent value="contacto" className="m-0 p-6 space-y-6 max-w-2xl">
              <div>
                <h2 className="text-3xl font-semibold text-balance">Información de Contacto</h2>
                <p className="text-muted-foreground mt-1">Datos de contacto del cliente</p>
              </div>
              <Card className="p-6 bg-card border-border">
                <p className="text-muted-foreground">Formulario de contacto...</p>
              </Card>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  if (subSection === "importar") {
    return (
      <div className="h-full flex flex-col">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
          <div className="border-b border-border bg-card px-6">
            <TabsList className="h-12 bg-transparent border-0 p-0 gap-6">
              <TabsTrigger
                value="todos"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Cargar Archivo
              </TabsTrigger>
              <TabsTrigger
                value="mapeo"
                className="relative h-12 rounded-none border-0 bg-transparent px-0 pb-3 pt-3 font-medium text-muted-foreground shadow-none transition-none data-[state=active]:bg-transparent data-[state=active]:text-foreground data-[state=active]:shadow-none after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-transparent data-[state=active]:after:bg-primary"
              >
                Mapeo de Campos
              </TabsTrigger>
            </TabsList>
          </div>

          <div className="flex-1 overflow-auto">
            <TabsContent value="todos" className="m-0 p-6 space-y-6 max-w-2xl">
              <div>
                <h2 className="text-3xl font-semibold text-balance">Importar Clientes</h2>
                <p className="text-muted-foreground mt-1">Importa clientes desde un archivo CSV o Excel</p>
              </div>
              <Card className="p-6 bg-card border-border">
                <p className="text-muted-foreground">Herramienta de carga de archivos...</p>
              </Card>
            </TabsContent>

            <TabsContent value="mapeo" className="m-0 p-6 space-y-6 max-w-2xl">
              <div>
                <h2 className="text-3xl font-semibold text-balance">Mapeo de Campos</h2>
                <p className="text-muted-foreground mt-1">Relaciona las columnas del archivo con los campos</p>
              </div>
              <Card className="p-6 bg-card border-border">
                <p className="text-muted-foreground">Herramienta de mapeo...</p>
              </Card>
            </TabsContent>
          </div>
        </Tabs>
      </div>
    )
  }

  return null
}

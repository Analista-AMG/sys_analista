"use client"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"
import { useState, useEffect } from "react"
import { Calendar, Plus, Pencil, RefreshCw } from "lucide-react"

interface CampanasViewProps {
  subSection: string
}

interface Analista {
  fecha: string
  dni: string
  nombre_completo: string
  codigo_salesys: string
  codigo_genesys: string
  nombre_laraigo: string
  nombre_360: string
  codigo_navicat: string
  codigo_ipcc: string
  condicion: string
  cargo: string
  sub_cargo: string
  campana: string
  estado: string
  fecha_ingreso_campana: string
  hora_entrada: string
  hora_salida: string
  supervisor: string
  asistencia_detalle: string
  observacion: string
}

export function CampanasView({ subSection }: CampanasViewProps) {
  const [activeTab, setActiveTab] = useState("dia-actual")
  const [selectedDashboard, setSelectedDashboard] = useState("activaciones")
  const [nominaDate, setNominaDate] = useState("")

  const [nomina, setNomina] = useState<Analista[]>([
    {
      fecha: "2024-01-14",
      dni: "12345678",
      nombre_completo: "María García López",
      codigo_salesys: "SLS001",
      codigo_genesys: "GNS001",
      nombre_laraigo: "MGARCIA",
      nombre_360: "MGARCIA360",
      codigo_navicat: "NAV001",
      codigo_ipcc: "IPCC001",
      condicion: "Activo",
      cargo: "Analista",
      sub_cargo: "Analista Senior",
      campana: "Activaciones",
      estado: "Presente",
      fecha_ingreso_campana: "2023-06-15",
      hora_entrada: "08:00",
      hora_salida: "16:00",
      supervisor: "Juan Pérez",
      asistencia_detalle: "Completo",
      observacion: "Sin observaciones",
    },
    {
      fecha: "2024-01-14",
      dni: "87654321",
      nombre_completo: "Carlos López Martínez",
      codigo_salesys: "SLS002",
      codigo_genesys: "GNS002",
      nombre_laraigo: "CLOPEZ",
      nombre_360: "CLOPEZ360",
      codigo_navicat: "NAV002",
      codigo_ipcc: "IPCC002",
      condicion: "Activo",
      cargo: "Analista",
      sub_cargo: "Analista Junior",
      campana: "Activaciones",
      estado: "Presente",
      fecha_ingreso_campana: "2023-08-20",
      hora_entrada: "08:00",
      hora_salida: "16:00",
      supervisor: "Juan Pérez",
      asistencia_detalle: "Completo",
      observacion: "",
    },
    {
      fecha: "2024-01-14",
      dni: "23456789",
      nombre_completo: "Ana Rodríguez Silva",
      codigo_salesys: "SLS003",
      codigo_genesys: "GNS003",
      nombre_laraigo: "ARODRIGUEZ",
      nombre_360: "ARODRIGUEZ360",
      codigo_navicat: "NAV003",
      codigo_ipcc: "IPCC003",
      condicion: "Activo",
      cargo: "Analista",
      sub_cargo: "Analista Senior",
      campana: "Delivery",
      estado: "Presente",
      fecha_ingreso_campana: "2023-05-10",
      hora_entrada: "09:00",
      hora_salida: "17:00",
      supervisor: "María Torres",
      asistencia_detalle: "Completo",
      observacion: "Excelente desempeño",
    },
    {
      fecha: "2024-01-14",
      dni: "34567890",
      nombre_completo: "Luis Fernández Castro",
      codigo_salesys: "SLS004",
      codigo_genesys: "GNS004",
      nombre_laraigo: "LFERNANDEZ",
      nombre_360: "LFERNANDEZ360",
      codigo_navicat: "NAV004",
      codigo_ipcc: "IPCC004",
      condicion: "Activo",
      cargo: "Analista",
      sub_cargo: "Analista",
      campana: "NPS",
      estado: "Presente",
      fecha_ingreso_campana: "2023-09-01",
      hora_entrada: "08:00",
      hora_salida: "16:00",
      supervisor: "Juan Pérez",
      asistencia_detalle: "Completo",
      observacion: "",
    },
    {
      fecha: "2024-01-14",
      dni: "45678901",
      nombre_completo: "Patricia Morales Vega",
      codigo_salesys: "SLS005",
      codigo_genesys: "GNS005",
      nombre_laraigo: "PMORALES",
      nombre_360: "PMORALES360",
      codigo_navicat: "NAV005",
      codigo_ipcc: "IPCC005",
      condicion: "Activo",
      cargo: "Analista",
      sub_cargo: "Analista Junior",
      campana: "Activaciones",
      estado: "Tardanza",
      fecha_ingreso_campana: "2023-11-15",
      hora_entrada: "08:30",
      hora_salida: "16:30",
      supervisor: "Juan Pérez",
      asistencia_detalle: "Incompleto",
      observacion: "Llegó 30 minutos tarde",
    },
    {
      fecha: "2024-01-14",
      dni: "56789012",
      nombre_completo: "Roberto Sánchez Díaz",
      codigo_salesys: "SLS006",
      codigo_genesys: "GNS006",
      nombre_laraigo: "RSANCHEZ",
      nombre_360: "RSANCHEZ360",
      codigo_navicat: "NAV006",
      codigo_ipcc: "IPCC006",
      condicion: "Activo",
      cargo: "Analista",
      sub_cargo: "Analista Senior",
      campana: "MultiSkill",
      estado: "Presente",
      fecha_ingreso_campana: "2023-04-20",
      hora_entrada: "07:00",
      hora_salida: "15:00",
      supervisor: "María Torres",
      asistencia_detalle: "Completo",
      observacion: "Turno madrugada",
    },
    {
      fecha: "2024-01-14",
      dni: "67890123",
      nombre_completo: "Carmen Ruiz Herrera",
      codigo_salesys: "SLS007",
      codigo_genesys: "GNS007",
      nombre_laraigo: "CRUIZ",
      nombre_360: "CRUIZ360",
      codigo_navicat: "NAV007",
      codigo_ipcc: "IPCC007",
      condicion: "Activo",
      cargo: "Analista",
      sub_cargo: "Analista",
      campana: "Soporte Venta Fija",
      estado: "Presente",
      fecha_ingreso_campana: "2023-07-12",
      hora_entrada: "10:00",
      hora_salida: "18:00",
      supervisor: "Carlos Mendoza",
      asistencia_detalle: "Completo",
      observacion: "",
    },
    {
      fecha: "2024-01-14",
      dni: "78901234",
      nombre_completo: "Jorge Ramírez Ortiz",
      codigo_salesys: "SLS008",
      codigo_genesys: "GNS008",
      nombre_laraigo: "JRAMIREZ",
      nombre_360: "JRAMIREZ360",
      codigo_navicat: "NAV008",
      codigo_ipcc: "IPCC008",
      condicion: "Activo",
      cargo: "Analista",
      sub_cargo: "Analista Junior",
      campana: "Validaciones",
      estado: "Presente",
      fecha_ingreso_campana: "2023-10-05",
      hora_entrada: "08:00",
      hora_salida: "16:00",
      supervisor: "Juan Pérez",
      asistencia_detalle: "Completo",
      observacion: "En capacitación",
    },
    {
      fecha: "2024-01-14",
      dni: "89012345",
      nombre_completo: "Laura Jiménez Flores",
      codigo_salesys: "SLS009",
      codigo_genesys: "GNS009",
      nombre_laraigo: "LJIMENEZ",
      nombre_360: "LJIMENEZ360",
      codigo_navicat: "NAV009",
      codigo_ipcc: "IPCC009",
      condicion: "Activo",
      cargo: "Analista",
      sub_cargo: "Analista Senior",
      campana: "Foto Corporativo",
      estado: "Permiso",
      fecha_ingreso_campana: "2023-03-18",
      hora_entrada: "08:00",
      hora_salida: "16:00",
      supervisor: "María Torres",
      asistencia_detalle: "Parcial",
      observacion: "Permiso médico por la tarde",
    },
    {
      fecha: "2024-01-14",
      dni: "90123456",
      nombre_completo: "Diego Torres Mendoza",
      codigo_salesys: "SLS010",
      codigo_genesys: "GNS010",
      nombre_laraigo: "DTORRES",
      nombre_360: "DTORRES360",
      codigo_navicat: "NAV010",
      codigo_ipcc: "IPCC010",
      condicion: "Activo",
      cargo: "Analista",
      sub_cargo: "Analista",
      campana: "Aghaso",
      estado: "Presente",
      fecha_ingreso_campana: "2023-08-30",
      hora_entrada: "09:00",
      hora_salida: "17:00",
      supervisor: "Carlos Mendoza",
      asistencia_detalle: "Completo",
      observacion: "",
    },
  ])

  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [editingIndex, setEditingIndex] = useState<number | null>(null)

  const [formData, setFormData] = useState<Analista>({
    fecha: "",
    dni: "",
    nombre_completo: "",
    codigo_salesys: "",
    codigo_genesys: "",
    nombre_laraigo: "",
    nombre_360: "",
    codigo_navicat: "",
    codigo_ipcc: "",
    condicion: "Activo",
    cargo: "Analista",
    sub_cargo: "",
    campana: "",
    estado: "Presente",
    fecha_ingreso_campana: "",
    hora_entrada: "",
    hora_salida: "",
    supervisor: "",
    asistencia_detalle: "Completo",
    observacion: "",
  })

  useEffect(() => {
    // Set default date to yesterday
    const yesterday = new Date()
    yesterday.setDate(yesterday.getDate() - 1)
    const formattedDate = yesterday.toISOString().split("T")[0]
    setNominaDate(formattedDate)
  }, [])

  const handleActualizar = () => {
    console.log("[v0] Actualizando nómina para la fecha:", nominaDate)
    // Here you would typically fetch new data from the backend
  }

  const handleAddAnalista = () => {
    setNomina([...nomina, formData])
    setIsAddDialogOpen(false)
    setFormData({
      fecha: "",
      dni: "",
      nombre_completo: "",
      codigo_salesys: "",
      codigo_genesys: "",
      nombre_laraigo: "",
      nombre_360: "",
      codigo_navicat: "",
      codigo_ipcc: "",
      condicion: "Activo",
      cargo: "Analista",
      sub_cargo: "",
      campana: "",
      estado: "Presente",
      fecha_ingreso_campana: "",
      hora_entrada: "",
      hora_salida: "",
      supervisor: "",
      asistencia_detalle: "Completo",
      observacion: "",
    })
  }

  const handleEditAnalista = () => {
    if (editingIndex !== null) {
      const updatedNomina = [...nomina]
      updatedNomina[editingIndex] = formData
      setNomina(updatedNomina)
      setIsEditDialogOpen(false)
      setEditingIndex(null)
      setFormData({
        fecha: "",
        dni: "",
        nombre_completo: "",
        codigo_salesys: "",
        codigo_genesys: "",
        nombre_laraigo: "",
        nombre_360: "",
        codigo_navicat: "",
        codigo_ipcc: "",
        condicion: "Activo",
        cargo: "Analista",
        sub_cargo: "",
        campana: "",
        estado: "Presente",
        fecha_ingreso_campana: "",
        hora_entrada: "",
        hora_salida: "",
        supervisor: "",
        asistencia_detalle: "Completo",
        observacion: "",
      })
    }
  }

  const openEditDialog = (index: number) => {
    setEditingIndex(index)
    setFormData(nomina[index])
    setIsEditDialogOpen(true)
  }

  const renderCampanaContent = (campanaName: string) => {
    const getTitleByTab = (tab: string) => {
      switch (tab) {
        case "dia-actual":
          return `Día Actual de ${campanaName}`
        case "dashboard":
          return `Dashboard de ${campanaName}`
        case "nomina":
          return `Nómina de ${campanaName}`
        case "descargas":
          return `Descargas de ${campanaName}`
        default:
          return campanaName
      }
    }

    return (
      <div className="p-6 overflow-x-hidden">
        <Tabs defaultValue="dia-actual" className="w-full" onValueChange={setActiveTab}>
          <div className="flex justify-center mb-6">
            <TabsList className="w-[65%]">
              <TabsTrigger value="dia-actual" className="flex-1">
                Día Actual
              </TabsTrigger>
              <TabsTrigger value="dashboard" className="flex-1">
                Dashboard
              </TabsTrigger>
              <TabsTrigger value="nomina" className="flex-1">
                Nómina
              </TabsTrigger>
              <TabsTrigger value="descargas" className="flex-1">
                Descargas
              </TabsTrigger>
            </TabsList>
          </div>

          <TabsContent value="dia-actual" className="space-y-6">
            <div className="mb-6 text-center">
              <h2 className="text-2xl font-semibold text-foreground mb-1">{getTitleByTab("dia-actual")}</h2>
              <p className="text-sm text-muted-foreground">Gestiones del día en curso</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">Gestiones Hoy</p>
                <p className="text-2xl font-bold text-foreground mt-2">{Math.floor(Math.random() * 200) + 100}</p>
              </Card>
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">Efectividad</p>
                <p className="text-2xl font-bold text-foreground mt-2">{Math.floor(Math.random() * 20) + 80}%</p>
              </Card>
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">En Proceso</p>
                <p className="text-2xl font-bold text-foreground mt-2">{Math.floor(Math.random() * 30) + 10}</p>
              </Card>
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">Completadas</p>
                <p className="text-2xl font-bold text-foreground mt-2">{Math.floor(Math.random() * 150) + 80}</p>
              </Card>
            </div>

            <Card className="p-6">
              <h3 className="text-lg font-semibold text-foreground mb-4">Gestiones del Día</h3>
              <div className="space-y-3">
                {[1, 2, 3, 4, 5, 6].map((i) => (
                  <div key={i} className="flex items-center justify-between p-3 bg-secondary/50 rounded-lg">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-foreground">Cliente #{2000 + i}</p>
                      <p className="text-xs text-muted-foreground">
                        Hora: {8 + i}:30 AM - Analista: {i % 2 === 0 ? "María García" : "Carlos López"}
                      </p>
                    </div>
                    <Badge variant={i % 3 === 0 ? "default" : i % 3 === 1 ? "secondary" : "outline"}>
                      {i % 3 === 0 ? "Completado" : i % 3 === 1 ? "En Proceso" : "Pendiente"}
                    </Badge>
                  </div>
                ))}
              </div>
            </Card>
          </TabsContent>

          <TabsContent value="dashboard" className="space-y-6">
            <div className="mb-6 text-center">
              <h2 className="text-2xl font-semibold text-foreground mb-4">{getTitleByTab("dashboard")}</h2>

              <div className="mb-4 flex justify-center">
                <div className="w-full max-w-[300px]">
                  <label className="text-sm text-muted-foreground mb-2 block">Seleccionar Dashboard</label>
                  <Select value={selectedDashboard} onValueChange={setSelectedDashboard}>
                    <SelectTrigger>
                      <SelectValue placeholder="Selecciona un dashboard" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="general">Dashboard General</SelectItem>
                      <SelectItem value="analistas">Dashboard Analistas</SelectItem>
                      <SelectItem value="historico">Dashboard Histórico</SelectItem>
                      <SelectItem value="comparativo">Dashboard Comparativo</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </div>

            <Card className="p-0 overflow-hidden">
              <iframe
                src="https://app.powerbi.com/view?r=eyJrIjoiYjFjNDIzNzUtODhhMy00ZGYxLWI3NWEtODJiYTA0YTAzOTk0IiwidCI6IjVhZTRkNjc0LWU2ZGEtNDBjMS1iNTNjLWY3NDNhNTc0OWY1ZCIsImMiOjR9"
                className="w-full h-[800px] border-0"
                allowFullScreen
              />
            </Card>
          </TabsContent>

          <TabsContent value="nomina" className="space-y-6 overflow-hidden">
            <div className="mb-6 text-center">
              <h2 className="text-2xl font-semibold text-foreground mb-4">{getTitleByTab("nomina")}</h2>
            </div>

            <Card className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-foreground">Nómina de Analistas</h3>
                <Button onClick={() => setIsAddDialogOpen(true)} size="sm">
                  <Plus className="h-4 w-4 mr-2" />
                  Agregar
                </Button>
              </div>

              <div className="mb-6 flex items-end gap-3">
                <div className="flex-1 max-w-[300px]">
                  <label className="text-sm text-muted-foreground mb-2 block">Seleccionar Fecha</label>
                  <div className="relative">
                    <Input
                      type="date"
                      value={nominaDate}
                      onChange={(e) => setNominaDate(e.target.value)}
                      className="pr-10"
                    />
                    <Calendar className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
                  </div>
                </div>
                <Button onClick={handleActualizar} size="default">
                  <RefreshCw className="h-4 w-4 mr-2" />
                  Actualizar
                </Button>
              </div>

              <div className="w-full border rounded-lg overflow-hidden">
                {/* Header - Fixed, no horizontal scroll */}
                <div className="w-full overflow-hidden bg-background border-b border-border">
                  <div className="min-w-[2000px]">
                    <div className="flex border-b border-border">
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "100px" }}
                      >
                        Fecha
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "100px" }}
                      >
                        DNI
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "180px" }}
                      >
                        Nombre Completo
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "120px" }}
                      >
                        Código SaleSys
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "120px" }}
                      >
                        Código Genesys
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "120px" }}
                      >
                        Nombre Laraigo
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "120px" }}
                      >
                        Nombre 360
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "120px" }}
                      >
                        Código Navicat
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "120px" }}
                      >
                        Código IPCC
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "100px" }}
                      >
                        Condición
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "100px" }}
                      >
                        Cargo
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "120px" }}
                      >
                        Sub Cargo
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "120px" }}
                      >
                        Campaña
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "100px" }}
                      >
                        Estado
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "150px" }}
                      >
                        Fecha Ingreso Campaña
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "100px" }}
                      >
                        Hora Entrada
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "100px" }}
                      >
                        Hora Salida
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "120px" }}
                      >
                        Supervisor
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "140px" }}
                      >
                        Asistencia Detalle
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "200px" }}
                      >
                        Observación
                      </div>
                      <div
                        className="py-3 px-4 text-sm font-semibold text-foreground whitespace-nowrap"
                        style={{ width: "100px" }}
                      >
                        Acciones
                      </div>
                    </div>
                  </div>
                </div>

                {/* Body - Scrollable horizontally */}
                <div className="w-full max-h-[500px] overflow-x-auto overflow-y-auto">
                  <div className="min-w-[2000px]">
                    {nomina.map((analista, i) => (
                      <div key={i} className="flex border-b border-border hover:bg-secondary/50 transition-colors">
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "100px" }}
                        >
                          {analista.fecha}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "100px" }}
                        >
                          {analista.dni}
                        </div>
                        <div className="py-3 px-4 text-sm text-foreground whitespace-nowrap" style={{ width: "180px" }}>
                          {analista.nombre_completo}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "120px" }}
                        >
                          {analista.codigo_salesys}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "120px" }}
                        >
                          {analista.codigo_genesys}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "120px" }}
                        >
                          {analista.nombre_laraigo}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "120px" }}
                        >
                          {analista.nombre_360}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "120px" }}
                        >
                          {analista.codigo_navicat}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "120px" }}
                        >
                          {analista.codigo_ipcc}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "100px" }}
                        >
                          {analista.condicion}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "100px" }}
                        >
                          {analista.cargo}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "120px" }}
                        >
                          {analista.sub_cargo}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "120px" }}
                        >
                          {analista.campana}
                        </div>
                        <div className="py-3 px-4 whitespace-nowrap" style={{ width: "100px" }}>
                          <Badge variant={analista.estado === "Presente" ? "default" : "secondary"}>
                            {analista.estado}
                          </Badge>
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "150px" }}
                        >
                          {analista.fecha_ingreso_campana}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "100px" }}
                        >
                          {analista.hora_entrada}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "100px" }}
                        >
                          {analista.hora_salida}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "120px" }}
                        >
                          {analista.supervisor}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "140px" }}
                        >
                          {analista.asistencia_detalle}
                        </div>
                        <div
                          className="py-3 px-4 text-sm text-muted-foreground whitespace-nowrap"
                          style={{ width: "200px" }}
                        >
                          {analista.observacion || "-"}
                        </div>
                        <div className="py-3 px-4 whitespace-nowrap" style={{ width: "100px" }}>
                          <Button variant="ghost" size="sm" onClick={() => openEditDialog(i)} className="h-8 w-8 p-0">
                            <Pencil className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="mt-6 flex items-center justify-between">
                <p className="text-sm text-muted-foreground">
                  Mostrando nómina del{" "}
                  {new Date(nominaDate).toLocaleDateString("es-ES", {
                    weekday: "long",
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                  })}
                </p>
                <Button size="sm">Descargar Nómina</Button>
              </div>
            </Card>
          </TabsContent>

          <TabsContent value="descargas" className="space-y-6">
            <div className="mb-6 text-center">
              <h2 className="text-2xl font-semibold text-foreground mb-4">{getTitleByTab("descargas")}</h2>
            </div>

            <div className="p-6">
              <h3 className="text-lg font-semibold text-foreground mb-4">Reportes Disponibles</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-foreground">Reporte Diario</p>
                    <p className="text-xs text-muted-foreground">Gestiones del día actual</p>
                  </div>
                  <Button size="sm">Descargar Excel</Button>
                </div>
                <div className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-foreground">Reporte Semanal</p>
                    <p className="text-xs text-muted-foreground">Resumen de la última semana</p>
                  </div>
                  <Button size="sm">Descargar Excel</Button>
                </div>
                <div className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-foreground">Reporte Mensual</p>
                    <p className="text-xs text-muted-foreground">Estadísticas del mes</p>
                  </div>
                  <Button size="sm">Descargar Excel</Button>
                </div>
                <div className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-foreground">Reporte por Analista</p>
                    <p className="text-xs text-muted-foreground">Rendimiento individual</p>
                  </div>
                  <Button size="sm">Descargar Excel</Button>
                </div>
                <div className="flex items-center justify-between p-4 bg-secondary/50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-foreground">Base de Datos Completa</p>
                    <p className="text-xs text-muted-foreground">Todas las gestiones registradas</p>
                  </div>
                  <Button size="sm">Descargar Excel</Button>
                </div>
              </div>
            </div>
          </TabsContent>
        </Tabs>

        <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
          <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Agregar Analista</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="fecha">Fecha</Label>
                  <Input
                    id="fecha"
                    type="date"
                    value={formData.fecha}
                    onChange={(e) => setFormData({ ...formData, fecha: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="dni">DNI</Label>
                  <Input
                    id="dni"
                    value={formData.dni}
                    onChange={(e) => setFormData({ ...formData, dni: e.target.value })}
                    placeholder="12345678"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="nombre_completo">Nombre Completo</Label>
                <Input
                  id="nombre_completo"
                  value={formData.nombre_completo}
                  onChange={(e) => setFormData({ ...formData, nombre_completo: e.target.value })}
                  placeholder="Nombre completo"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="codigo_salesys">Código SaleSys</Label>
                  <Input
                    id="codigo_salesys"
                    value={formData.codigo_salesys}
                    onChange={(e) => setFormData({ ...formData, codigo_salesys: e.target.value })}
                    placeholder="SLS001"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="codigo_genesys">Código Genesys</Label>
                  <Input
                    id="codigo_genesys"
                    value={formData.codigo_genesys}
                    onChange={(e) => setFormData({ ...formData, codigo_genesys: e.target.value })}
                    placeholder="GNS001"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="nombre_laraigo">Nombre Laraigo</Label>
                  <Input
                    id="nombre_laraigo"
                    value={formData.nombre_laraigo}
                    onChange={(e) => setFormData({ ...formData, nombre_laraigo: e.target.value })}
                    placeholder="USUARIO"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="nombre_360">Nombre 360</Label>
                  <Input
                    id="nombre_360"
                    value={formData.nombre_360}
                    onChange={(e) => setFormData({ ...formData, nombre_360: e.target.value })}
                    placeholder="USUARIO360"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="codigo_navicat">Código Navicat</Label>
                  <Input
                    id="codigo_navicat"
                    value={formData.codigo_navicat}
                    onChange={(e) => setFormData({ ...formData, codigo_navicat: e.target.value })}
                    placeholder="NAV001"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="codigo_ipcc">Código IPCC</Label>
                  <Input
                    id="codigo_ipcc"
                    value={formData.codigo_ipcc}
                    onChange={(e) => setFormData({ ...formData, codigo_ipcc: e.target.value })}
                    placeholder="IPCC001"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="condicion">Condición</Label>
                  <Select
                    value={formData.condicion}
                    onValueChange={(value) => setFormData({ ...formData, condicion: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Activo">Activo</SelectItem>
                      <SelectItem value="Inactivo">Inactivo</SelectItem>
                      <SelectItem value="Suspendido">Suspendido</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="cargo">Cargo</Label>
                  <Input
                    id="cargo"
                    value={formData.cargo}
                    onChange={(e) => setFormData({ ...formData, cargo: e.target.value })}
                    placeholder="Analista"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="sub_cargo">Sub Cargo</Label>
                  <Input
                    id="sub_cargo"
                    value={formData.sub_cargo}
                    onChange={(e) => setFormData({ ...formData, sub_cargo: e.target.value })}
                    placeholder="Analista Senior"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="campana">Campaña</Label>
                  <Input
                    id="campana"
                    value={formData.campana}
                    onChange={(e) => setFormData({ ...formData, campana: e.target.value })}
                    placeholder="Activaciones"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="estado">Estado</Label>
                  <Select
                    value={formData.estado}
                    onValueChange={(value) => setFormData({ ...formData, estado: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Presente">Presente</SelectItem>
                      <SelectItem value="Ausente">Ausente</SelectItem>
                      <SelectItem value="Tardanza">Tardanza</SelectItem>
                      <SelectItem value="Permiso">Permiso</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="fecha_ingreso_campana">Fecha Ingreso Campaña</Label>
                  <Input
                    id="fecha_ingreso_campana"
                    type="date"
                    value={formData.fecha_ingreso_campana}
                    onChange={(e) => setFormData({ ...formData, fecha_ingreso_campana: e.target.value })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="hora_entrada">Hora Entrada</Label>
                  <Input
                    id="hora_entrada"
                    type="time"
                    value={formData.hora_entrada}
                    onChange={(e) => setFormData({ ...formData, hora_entrada: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="hora_salida">Hora Salida</Label>
                  <Input
                    id="hora_salida"
                    type="time"
                    value={formData.hora_salida}
                    onChange={(e) => setFormData({ ...formData, hora_salida: e.target.value })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="supervisor">Supervisor</Label>
                  <Input
                    id="supervisor"
                    value={formData.supervisor}
                    onChange={(e) => setFormData({ ...formData, supervisor: e.target.value })}
                    placeholder="Nombre del supervisor"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="asistencia_detalle">Asistencia Detalle</Label>
                  <Select
                    value={formData.asistencia_detalle}
                    onValueChange={(value) => setFormData({ ...formData, asistencia_detalle: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Completo">Completo</SelectItem>
                      <SelectItem value="Incompleto">Incompleto</SelectItem>
                      <SelectItem value="Parcial">Parcial</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="observacion">Observación</Label>
                <Input
                  id="observacion"
                  value={formData.observacion}
                  onChange={(e) => setFormData({ ...formData, observacion: e.target.value })}
                  placeholder="Observaciones adicionales"
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsAddDialogOpen(false)}>
                Cancelar
              </Button>
              <Button onClick={handleAddAnalista}>Agregar</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
          <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>Editar Analista</DialogTitle>
            </DialogHeader>
            <div className="space-y-4 py-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="edit-fecha">Fecha</Label>
                  <Input
                    id="edit-fecha"
                    type="date"
                    value={formData.fecha}
                    onChange={(e) => setFormData({ ...formData, fecha: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="edit-dni">DNI</Label>
                  <Input
                    id="edit-dni"
                    value={formData.dni}
                    onChange={(e) => setFormData({ ...formData, dni: e.target.value })}
                    placeholder="12345678"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="edit-nombre_completo">Nombre Completo</Label>
                <Input
                  id="edit-nombre_completo"
                  value={formData.nombre_completo}
                  onChange={(e) => setFormData({ ...formData, nombre_completo: e.target.value })}
                  placeholder="Nombre completo"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="edit-codigo_salesys">Código SaleSys</Label>
                  <Input
                    id="edit-codigo_salesys"
                    value={formData.codigo_salesys}
                    onChange={(e) => setFormData({ ...formData, codigo_salesys: e.target.value })}
                    placeholder="SLS001"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="edit-codigo_genesys">Código Genesys</Label>
                  <Input
                    id="edit-codigo_genesys"
                    value={formData.codigo_genesys}
                    onChange={(e) => setFormData({ ...formData, codigo_genesys: e.target.value })}
                    placeholder="GNS001"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="edit-nombre_laraigo">Nombre Laraigo</Label>
                  <Input
                    id="edit-nombre_laraigo"
                    value={formData.nombre_laraigo}
                    onChange={(e) => setFormData({ ...formData, nombre_laraigo: e.target.value })}
                    placeholder="USUARIO"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="edit-nombre_360">Nombre 360</Label>
                  <Input
                    id="edit-nombre_360"
                    value={formData.nombre_360}
                    onChange={(e) => setFormData({ ...formData, nombre_360: e.target.value })}
                    placeholder="USUARIO360"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="edit-codigo_navicat">Código Navicat</Label>
                  <Input
                    id="edit-codigo_navicat"
                    value={formData.codigo_navicat}
                    onChange={(e) => setFormData({ ...formData, codigo_navicat: e.target.value })}
                    placeholder="NAV001"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="edit-codigo_ipcc">Código IPCC</Label>
                  <Input
                    id="edit-codigo_ipcc"
                    value={formData.codigo_ipcc}
                    onChange={(e) => setFormData({ ...formData, codigo_ipcc: e.target.value })}
                    placeholder="IPCC001"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="edit-condicion">Condición</Label>
                  <Select
                    value={formData.condicion}
                    onValueChange={(value) => setFormData({ ...formData, condicion: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Activo">Activo</SelectItem>
                      <SelectItem value="Inactivo">Inactivo</SelectItem>
                      <SelectItem value="Suspendido">Suspendido</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="edit-cargo">Cargo</Label>
                  <Input
                    id="edit-cargo"
                    value={formData.cargo}
                    onChange={(e) => setFormData({ ...formData, cargo: e.target.value })}
                    placeholder="Analista"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="edit-sub_cargo">Sub Cargo</Label>
                  <Input
                    id="edit-sub_cargo"
                    value={formData.sub_cargo}
                    onChange={(e) => setFormData({ ...formData, sub_cargo: e.target.value })}
                    placeholder="Analista Senior"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="edit-campana">Campaña</Label>
                  <Input
                    id="edit-campana"
                    value={formData.campana}
                    onChange={(e) => setFormData({ ...formData, campana: e.target.value })}
                    placeholder="Activaciones"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="edit-estado">Estado</Label>
                  <Select
                    value={formData.estado}
                    onValueChange={(value) => setFormData({ ...formData, estado: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Presente">Presente</SelectItem>
                      <SelectItem value="Ausente">Ausente</SelectItem>
                      <SelectItem value="Tardanza">Tardanza</SelectItem>
                      <SelectItem value="Permiso">Permiso</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="edit-fecha_ingreso_campana">Fecha Ingreso Campaña</Label>
                  <Input
                    id="edit-fecha_ingreso_campana"
                    type="date"
                    value={formData.fecha_ingreso_campana}
                    onChange={(e) => setFormData({ ...formData, fecha_ingreso_campana: e.target.value })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="edit-hora_entrada">Hora Entrada</Label>
                  <Input
                    id="edit-hora_entrada"
                    type="time"
                    value={formData.hora_entrada}
                    onChange={(e) => setFormData({ ...formData, hora_entrada: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="edit-hora_salida">Hora Salida</Label>
                  <Input
                    id="edit-hora_salida"
                    type="time"
                    value={formData.hora_salida}
                    onChange={(e) => setFormData({ ...formData, hora_salida: e.target.value })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="edit-supervisor">Supervisor</Label>
                  <Input
                    id="edit-supervisor"
                    value={formData.supervisor}
                    onChange={(e) => setFormData({ ...formData, supervisor: e.target.value })}
                    placeholder="Nombre del supervisor"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="edit-asistencia_detalle">Asistencia Detalle</Label>
                  <Select
                    value={formData.asistencia_detalle}
                    onValueChange={(value) => setFormData({ ...formData, asistencia_detalle: value })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Completo">Completo</SelectItem>
                      <SelectItem value="Incompleto">Incompleto</SelectItem>
                      <SelectItem value="Parcial">Parcial</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="edit-observacion">Observación</Label>
                <Input
                  id="edit-observacion"
                  value={formData.observacion}
                  onChange={(e) => setFormData({ ...formData, observacion: e.target.value })}
                  placeholder="Observaciones adicionales"
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setIsEditDialogOpen(false)}>
                Cancelar
              </Button>
              <Button onClick={handleEditAnalista}>Guardar Cambios</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    )
  }

  if (subSection === "activaciones") return renderCampanaContent("Activaciones")
  if (subSection === "aghaso") return renderCampanaContent("Aghaso")
  if (subSection === "delivery") return renderCampanaContent("Delivery")
  if (subSection === "foto-corporativo") return renderCampanaContent("Foto Corporativo")
  if (subSection === "foto-alambrico") return renderCampanaContent("Foto Alambrico")
  if (subSection === "nps") return renderCampanaContent("NPS")
  if (subSection === "multiskill") return renderCampanaContent("MultiSkill")
  if (subSection === "programacion-seg-fija") return renderCampanaContent("Programación y Seg Fija")
  if (subSection === "soporte-venta-fija") return renderCampanaContent("Soporte Venta Fija")
  if (subSection === "validaciones") return renderCampanaContent("Validaciones")

  return null
}

"use client"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { useState, useEffect } from "react"
import { Calendar, RefreshCw, X, Eye, Pencil, Trash2 } from "lucide-react"

interface CampanasViewProps {
  subSection: string
}

interface PersonalData {
  id: string
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
  campaña: string
  estado: "Activo" | "Inactivo" | "Licencia"
  fecha_ingreso_campaña: string
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
  const [personal, setPersonal] = useState<PersonalData[]>([
    {
      id: "1",
      fecha: "2024-01-15",
      dni: "12345678",
      nombre_completo: "Juan Pérez García",
      codigo_salesys: "SAL001",
      codigo_genesys: "GEN001",
      nombre_laraigo: "JPEREZ",
      nombre_360: "JP001",
      codigo_navicat: "NAV001",
      codigo_ipcc: "IPCC001",
      condicion: "Permanente",
      cargo: "Analista",
      sub_cargo: "Analista Senior",
      campaña: "Activaciones",
      estado: "Activo",
      fecha_ingreso_campaña: "2023-01-15",
      hora_entrada: "08:00",
      hora_salida: "17:00",
      supervisor: "Carlos López",
      asistencia_detalle: "Presente",
      observacion: "Buen desempeño",
    },
    {
      id: "2",
      fecha: "2024-01-15",
      dni: "87654321",
      nombre_completo: "María García López",
      codigo_salesys: "SAL002",
      codigo_genesys: "GEN002",
      nombre_laraigo: "MGARCIA",
      nombre_360: "MG001",
      codigo_navicat: "NAV002",
      codigo_ipcc: "IPCC002",
      condicion: "Permanente",
      cargo: "Supervisor",
      sub_cargo: "Supervisor de Equipo",
      campaña: "Activaciones",
      estado: "Activo",
      fecha_ingreso_campaña: "2022-06-20",
      hora_entrada: "07:30",
      hora_salida: "16:30",
      supervisor: "Director",
      asistencia_detalle: "Presente",
      observacion: "Excelente liderazgo",
    },
    {
      id: "3",
      fecha: "2024-01-15",
      dni: "11223344",
      nombre_completo: "Pedro Rodríguez Martínez",
      codigo_salesys: "SAL003",
      codigo_genesys: "GEN003",
      nombre_laraigo: "PRODRIGUEZ",
      nombre_360: "PR001",
      codigo_navicat: "NAV003",
      codigo_ipcc: "IPCC003",
      condicion: "Temporal",
      cargo: "Analista",
      sub_cargo: "Analista Junior",
      campaña: "Activaciones",
      estado: "Licencia",
      fecha_ingreso_campaña: "2023-03-10",
      hora_entrada: "08:00",
      hora_salida: "17:00",
      supervisor: "Carlos López",
      asistencia_detalle: "Licencia",
      observacion: "En licencia médica",
    },
    {
      id: "4",
      fecha: "2024-01-15",
      dni: "55667788",
      nombre_completo: "Ana Martínez Sánchez",
      codigo_salesys: "SAL004",
      codigo_genesys: "GEN004",
      nombre_laraigo: "AMARTINEZ",
      nombre_360: "AM001",
      codigo_navicat: "NAV004",
      codigo_ipcc: "IPCC004",
      condicion: "Permanente",
      cargo: "Analista",
      sub_cargo: "Analista Senior",
      campaña: "Activaciones",
      estado: "Activo",
      fecha_ingreso_campaña: "2022-09-05",
      hora_entrada: "08:00",
      hora_salida: "17:00",
      supervisor: "María García López",
      asistencia_detalle: "Presente",
      observacion: "Excelente productividad",
    },
    {
      id: "5",
      fecha: "2024-01-15",
      dni: "99887766",
      nombre_completo: "Luis Fernández Díaz",
      codigo_salesys: "SAL005",
      codigo_genesys: "GEN005",
      nombre_laraigo: "LFERNANDEZ",
      nombre_360: "LF001",
      codigo_navicat: "NAV005",
      codigo_ipcc: "IPCC005",
      condicion: "Permanente",
      cargo: "Analista",
      sub_cargo: "Analista Pleno",
      campaña: "Activaciones",
      estado: "Activo",
      fecha_ingreso_campaña: "2023-02-14",
      hora_entrada: "08:00",
      hora_salida: "17:00",
      supervisor: "Carlos López",
      asistencia_detalle: "Presente",
      observacion: "Cumplimiento de metas",
    },
    {
      id: "6",
      fecha: "2024-01-15",
      dni: "44332211",
      nombre_completo: "Carmen Ruiz Gómez",
      codigo_salesys: "SAL006",
      codigo_genesys: "GEN006",
      nombre_laraigo: "CRUIZ",
      nombre_360: "CR001",
      codigo_navicat: "NAV006",
      codigo_ipcc: "IPCC006",
      condicion: "Temporal",
      cargo: "Analista",
      sub_cargo: "Analista Junior",
      campaña: "Activaciones",
      estado: "Activo",
      fecha_ingreso_campaña: "2023-11-20",
      hora_entrada: "08:00",
      hora_salida: "17:00",
      supervisor: "María García López",
      asistencia_detalle: "Presente",
      observacion: "En período de prueba",
    },
    {
      id: "7",
      fecha: "2024-01-15",
      dni: "77665544",
      nombre_completo: "Roberto Jiménez Flores",
      codigo_salesys: "SAL007",
      codigo_genesys: "GEN007",
      nombre_laraigo: "RJIMENEZ",
      nombre_360: "RJ001",
      codigo_navicat: "NAV007",
      codigo_ipcc: "IPCC007",
      condicion: "Permanente",
      cargo: "Coordinador",
      sub_cargo: "Coordinador de Calidad",
      campaña: "Activaciones",
      estado: "Activo",
      fecha_ingreso_campaña: "2022-04-10",
      hora_entrada: "07:30",
      hora_salida: "16:30",
      supervisor: "Director",
      asistencia_detalle: "Presente",
      observacion: "Responsable de auditorías",
    },
    {
      id: "8",
      fecha: "2024-01-15",
      dni: "33221100",
      nombre_completo: "Sofía Morales Castillo",
      codigo_salesys: "SAL008",
      codigo_genesys: "GEN008",
      nombre_laraigo: "SMORALES",
      nombre_360: "SM001",
      codigo_navicat: "NAV008",
      codigo_ipcc: "IPCC008",
      condicion: "Permanente",
      cargo: "Analista",
      sub_cargo: "Analista Senior",
      campaña: "Activaciones",
      estado: "Inactivo",
      fecha_ingreso_campaña: "2021-08-15",
      hora_entrada: "08:00",
      hora_salida: "17:00",
      supervisor: "Carlos López",
      asistencia_detalle: "Ausente",
      observacion: "Suspensión temporal",
    },
    {
      id: "9",
      fecha: "2024-01-15",
      dni: "66554433",
      nombre_completo: "Diego Vargas Romero",
      codigo_salesys: "SAL009",
      codigo_genesys: "GEN009",
      nombre_laraigo: "DVARGAS",
      nombre_360: "DV001",
      codigo_navicat: "NAV009",
      codigo_ipcc: "IPCC009",
      condicion: "Temporal",
      cargo: "Analista",
      sub_cargo: "Analista Pleno",
      campaña: "Activaciones",
      estado: "Activo",
      fecha_ingreso_campaña: "2023-07-01",
      hora_entrada: "08:00",
      hora_salida: "17:00",
      supervisor: "María García López",
      asistencia_detalle: "Presente",
      observacion: "Contrato por proyecto",
    },
    {
      id: "10",
      fecha: "2024-01-15",
      dni: "22110099",
      nombre_completo: "Valentina Soto Navarro",
      codigo_salesys: "SAL010",
      codigo_genesys: "GEN010",
      nombre_laraigo: "VSOTO",
      nombre_360: "VS001",
      codigo_navicat: "NAV010",
      codigo_ipcc: "IPCC010",
      condicion: "Permanente",
      cargo: "Analista",
      sub_cargo: "Analista Junior",
      campaña: "Activaciones",
      estado: "Activo",
      fecha_ingreso_campaña: "2023-10-03",
      hora_entrada: "08:00",
      hora_salida: "17:00",
      supervisor: "Carlos López",
      asistencia_detalle: "Presente",
      observacion: "Nuevo ingreso",
    },
    {
      id: "11",
      fecha: "2024-01-15",
      dni: "88990011",
      nombre_completo: "Javier Herrera Mendoza",
      codigo_salesys: "SAL011",
      codigo_genesys: "GEN011",
      nombre_laraigo: "JHERRERA",
      nombre_360: "JH001",
      codigo_navicat: "NAV011",
      codigo_ipcc: "IPCC011",
      condicion: "Permanente",
      cargo: "Analista",
      sub_cargo: "Analista Senior",
      campaña: "Activaciones",
      estado: "Activo",
      fecha_ingreso_campaña: "2022-12-12",
      hora_entrada: "08:00",
      hora_salida: "17:00",
      supervisor: "María García López",
      asistencia_detalle: "Presente",
      observacion: "Especialista en ventas",
    },
    {
      id: "12",
      fecha: "2024-01-15",
      dni: "11009988",
      nombre_completo: "Gabriela Ortiz Reyes",
      codigo_salesys: "SAL012",
      codigo_genesys: "GEN012",
      nombre_laraigo: "GORTIZ",
      nombre_360: "GO001",
      codigo_navicat: "NAV012",
      codigo_ipcc: "IPCC012",
      condicion: "Temporal",
      cargo: "Analista",
      sub_cargo: "Analista Pleno",
      campaña: "Activaciones",
      estado: "Licencia",
      fecha_ingreso_campaña: "2023-05-22",
      hora_entrada: "08:00",
      hora_salida: "17:00",
      supervisor: "Carlos López",
      asistencia_detalle: "Licencia",
      observacion: "Licencia de maternidad",
    },
    {
      id: "13",
      fecha: "2024-01-15",
      dni: "99001122",
      nombre_completo: "Marcos Delgado Silva",
      codigo_salesys: "SAL013",
      codigo_genesys: "GEN013",
      nombre_laraigo: "MDELGADO",
      nombre_360: "MD001",
      codigo_navicat: "NAV013",
      codigo_ipcc: "IPCC013",
      condicion: "Permanente",
      cargo: "Analista",
      sub_cargo: "Analista Junior",
      campaña: "Activaciones",
      estado: "Activo",
      fecha_ingreso_campaña: "2023-09-18",
      hora_entrada: "08:00",
      hora_salida: "17:00",
      supervisor: "María García López",
      asistencia_detalle: "Presente",
      observacion: "Buen potencial",
    },
  ])
  const [editingId, setEditingId] = useState<string | null>(null)
  const [showAddModal, setShowAddModal] = useState(false)
  const [showEditModal, setShowEditModal] = useState(false)
  const [showViewModal, setShowViewModal] = useState(false)
  const [viewingPerson, setViewingPerson] = useState<PersonalData | null>(null)
  const [formData, setFormData] = useState<PersonalData>({
    id: "",
    fecha: "",
    dni: "",
    nombre_completo: "",
    codigo_salesys: "",
    codigo_genesys: "",
    nombre_laraigo: "",
    nombre_360: "",
    codigo_navicat: "",
    codigo_ipcc: "",
    condicion: "",
    cargo: "",
    sub_cargo: "",
    campaña: "",
    estado: "Activo",
    fecha_ingreso_campaña: "",
    hora_entrada: "",
    hora_salida: "",
    supervisor: "",
    asistencia_detalle: "",
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
  }

  const handleAddPersonal = () => {
    setFormData({
      id: Date.now().toString(),
      fecha: new Date().toISOString().split("T")[0],
      dni: "",
      nombre_completo: "",
      codigo_salesys: "",
      codigo_genesys: "",
      nombre_laraigo: "",
      nombre_360: "",
      codigo_navicat: "",
      codigo_ipcc: "",
      condicion: "",
      cargo: "",
      sub_cargo: "",
      campaña: "",
      estado: "Activo",
      fecha_ingreso_campaña: "",
      hora_entrada: "",
      hora_salida: "",
      supervisor: "",
      asistencia_detalle: "",
      observacion: "",
    })
    setShowAddModal(true)
  }

  const handleEditPersonal = (person: PersonalData) => {
    setFormData(person)
    setEditingId(person.id)
    setShowEditModal(true)
  }

  const handleViewPersonal = (person: PersonalData) => {
    setViewingPerson(person)
    setShowViewModal(true)
  }

  const handleSavePersonal = () => {
    if (editingId) {
      setPersonal(personal.map((p) => (p.id === editingId ? formData : p)))
      setShowEditModal(false)
    } else {
      setPersonal([...personal, formData])
      setShowAddModal(false)
    }
    setFormData({
      id: "",
      fecha: "",
      dni: "",
      nombre_completo: "",
      codigo_salesys: "",
      codigo_genesys: "",
      nombre_laraigo: "",
      nombre_360: "",
      codigo_navicat: "",
      codigo_ipcc: "",
      condicion: "",
      cargo: "",
      sub_cargo: "",
      campaña: "",
      estado: "Activo",
      fecha_ingreso_campaña: "",
      hora_entrada: "",
      hora_salida: "",
      supervisor: "",
      asistencia_detalle: "",
      observacion: "",
    })
  }

  const handleDeletePersonal = (id: string) => {
    setPersonal(personal.filter((p) => p.id !== id))
  }

  const handleDownload = () => {
    console.log("[v0] Descargando nómina de personal")
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
      <div className="p-6 overflow-auto h-full">
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
              <div className="mb-6 flex items-end gap-3 justify-center">
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
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">Total Personal</p>
                <p className="text-2xl font-bold text-foreground mt-2">{personal.length}</p>
              </Card>
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">Activos</p>
                <p className="text-2xl font-bold text-foreground mt-2">
                  {personal.filter((p) => p.estado === "Activo").length}
                </p>
              </Card>
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">Inactivos</p>
                <p className="text-2xl font-bold text-foreground mt-2">
                  {personal.filter((p) => p.estado === "Inactivo").length}
                </p>
              </Card>
              <Card className="p-4">
                <p className="text-sm text-muted-foreground">En Licencia</p>
                <p className="text-2xl font-bold text-foreground mt-2">
                  {personal.filter((p) => p.estado === "Licencia").length}
                </p>
              </Card>
            </div>

            <Card className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-foreground">Personal</h3>
                <Button onClick={handleAddPersonal} size="sm">
                  Agregar Personal
                </Button>
              </div>

              <div className="overflow-auto border rounded-lg max-h-[600px]">
                <table className="w-full text-sm">
                  <thead className="bg-secondary/50 border-b sticky top-0">
                    <tr>
                      <th className="px-4 py-2 text-left font-semibold">Nombre</th>
                      <th className="px-4 py-2 text-left font-semibold">DNI</th>
                      <th className="px-4 py-2 text-left font-semibold">Cargo</th>
                      <th className="px-4 py-2 text-left font-semibold">Estado</th>
                      <th className="px-4 py-2 text-left font-semibold">Fecha Ingreso</th>
                      <th className="px-4 py-2 text-left font-semibold">Supervisor</th>
                      <th className="px-4 py-2 text-center font-semibold">Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {personal.map((person) => (
                      <tr key={person.id} className="border-b hover:bg-secondary/30">
                        <td className="px-4 py-2">{person.nombre_completo}</td>
                        <td className="px-4 py-2">{person.dni}</td>
                        <td className="px-4 py-2">{person.cargo}</td>
                        <td className="px-4 py-2">
                          <Badge
                            variant={
                              person.estado === "Activo"
                                ? "default"
                                : person.estado === "Inactivo"
                                  ? "secondary"
                                  : "outline"
                            }
                          >
                            {person.estado}
                          </Badge>
                        </td>
                        <td className="px-4 py-2">{person.fecha_ingreso_campaña}</td>
                        <td className="px-4 py-2">{person.supervisor}</td>
                        <td className="px-4 py-2 text-center space-x-2">
                          <button
                            onClick={() => handleViewPersonal(person)}
                            className="inline-flex items-center justify-center h-8 w-8 rounded hover:bg-secondary/50 transition-colors"
                            title="Visualizar"
                          >
                            <Eye className="h-4 w-4 text-foreground" />
                          </button>
                          <button
                            onClick={() => handleEditPersonal(person)}
                            className="inline-flex items-center justify-center h-8 w-8 rounded hover:bg-secondary/50 transition-colors"
                            title="Editar"
                          >
                            <Pencil className="h-4 w-4 text-foreground" />
                          </button>
                          <button
                            onClick={() => handleDeletePersonal(person.id)}
                            className="inline-flex items-center justify-center h-8 w-8 rounded hover:bg-destructive/20 transition-colors"
                            title="Eliminar"
                          >
                            <Trash2 className="h-4 w-4 text-destructive" />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="mt-4 flex justify-end">
                <Button onClick={handleDownload} size="default">
                  Descargar Nómina
                </Button>
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

        {showEditModal && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-semibold text-foreground">Editar Personal</h2>
                  <Button onClick={() => setShowEditModal(false)} variant="ghost" size="sm" className="h-8 w-8 p-0">
                    <X className="h-4 w-4" />
                  </Button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Fecha</label>
                    <Input
                      type="date"
                      value={formData.fecha}
                      onChange={(e) => setFormData({ ...formData, fecha: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">DNI</label>
                    <Input value={formData.dni} onChange={(e) => setFormData({ ...formData, dni: e.target.value })} />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Nombre Completo</label>
                    <Input
                      value={formData.nombre_completo}
                      onChange={(e) => setFormData({ ...formData, nombre_completo: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Código SaleSys</label>
                    <Input
                      value={formData.codigo_salesys}
                      onChange={(e) => setFormData({ ...formData, codigo_salesys: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Código Genesys</label>
                    <Input
                      value={formData.codigo_genesys}
                      onChange={(e) => setFormData({ ...formData, codigo_genesys: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Nombre Laraigo</label>
                    <Input
                      value={formData.nombre_laraigo}
                      onChange={(e) => setFormData({ ...formData, nombre_laraigo: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Nombre 360</label>
                    <Input
                      value={formData.nombre_360}
                      onChange={(e) => setFormData({ ...formData, nombre_360: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Código Navicat</label>
                    <Input
                      value={formData.codigo_navicat}
                      onChange={(e) => setFormData({ ...formData, codigo_navicat: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Código IPCC</label>
                    <Input
                      value={formData.codigo_ipcc}
                      onChange={(e) => setFormData({ ...formData, codigo_ipcc: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Condición</label>
                    <Select
                      value={formData.condicion}
                      onValueChange={(value) => setFormData({ ...formData, condicion: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Permanente">Permanente</SelectItem>
                        <SelectItem value="Temporal">Temporal</SelectItem>
                        <SelectItem value="Contratista">Contratista</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Cargo</label>
                    <Select
                      value={formData.cargo}
                      onValueChange={(value) => setFormData({ ...formData, cargo: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Analista">Analista</SelectItem>
                        <SelectItem value="Supervisor">Supervisor</SelectItem>
                        <SelectItem value="Coordinador">Coordinador</SelectItem>
                        <SelectItem value="Gerente">Gerente</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Sub Cargo</label>
                    <Select
                      value={formData.sub_cargo}
                      onValueChange={(value) => setFormData({ ...formData, sub_cargo: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Analista Junior">Analista Junior</SelectItem>
                        <SelectItem value="Analista Pleno">Analista Pleno</SelectItem>
                        <SelectItem value="Analista Senior">Analista Senior</SelectItem>
                        <SelectItem value="Supervisor de Equipo">Supervisor de Equipo</SelectItem>
                        <SelectItem value="Coordinador de Calidad">Coordinador de Calidad</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Campaña</label>
                    <Select
                      value={formData.campaña}
                      onValueChange={(value) => setFormData({ ...formData, campaña: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Activaciones">Activaciones</SelectItem>
                        <SelectItem value="Aghaso">Aghaso</SelectItem>
                        <SelectItem value="Delivery">Delivery</SelectItem>
                        <SelectItem value="Foto Corporativo">Foto Corporativo</SelectItem>
                        <SelectItem value="Foto Alambrico">Foto Alambrico</SelectItem>
                        <SelectItem value="NPS">NPS</SelectItem>
                        <SelectItem value="MultiSkill">MultiSkill</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Estado</label>
                    <Select
                      value={formData.estado}
                      onValueChange={(value) =>
                        setFormData({ ...formData, estado: value as "Activo" | "Inactivo" | "Licencia" })
                      }
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Activo">Activo</SelectItem>
                        <SelectItem value="Inactivo">Inactivo</SelectItem>
                        <SelectItem value="Licencia">Licencia</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Fecha Ingreso Campaña</label>
                    <Input
                      type="date"
                      value={formData.fecha_ingreso_campaña}
                      onChange={(e) => setFormData({ ...formData, fecha_ingreso_campaña: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Hora Entrada</label>
                    <Input
                      type="time"
                      value={formData.hora_entrada}
                      onChange={(e) => setFormData({ ...formData, hora_entrada: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Hora Salida</label>
                    <Input
                      type="time"
                      value={formData.hora_salida}
                      onChange={(e) => setFormData({ ...formData, hora_salida: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Supervisor</label>
                    <Input
                      value={formData.supervisor}
                      onChange={(e) => setFormData({ ...formData, supervisor: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Asistencia Detalle</label>
                    <Input
                      value={formData.asistencia_detalle}
                      onChange={(e) => setFormData({ ...formData, asistencia_detalle: e.target.value })}
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="text-sm text-muted-foreground mb-1 block">Observación</label>
                    <Input
                      value={formData.observacion}
                      onChange={(e) => setFormData({ ...formData, observacion: e.target.value })}
                    />
                  </div>
                </div>

                <div className="mt-6 flex justify-end gap-2">
                  <Button onClick={() => setShowEditModal(false)} variant="outline">
                    Cancelar
                  </Button>
                  <Button onClick={handleSavePersonal}>Guardar Cambios</Button>
                </div>
              </div>
            </Card>
          </div>
        )}

        {showAddModal && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-semibold text-foreground">Agregar Personal</h2>
                  <Button onClick={() => setShowAddModal(false)} variant="ghost" size="sm" className="h-8 w-8 p-0">
                    <X className="h-4 w-4" />
                  </Button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Fecha</label>
                    <Input
                      type="date"
                      value={formData.fecha}
                      onChange={(e) => setFormData({ ...formData, fecha: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">DNI</label>
                    <Input value={formData.dni} onChange={(e) => setFormData({ ...formData, dni: e.target.value })} />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Nombre Completo</label>
                    <Input
                      value={formData.nombre_completo}
                      onChange={(e) => setFormData({ ...formData, nombre_completo: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Código SaleSys</label>
                    <Input
                      value={formData.codigo_salesys}
                      onChange={(e) => setFormData({ ...formData, codigo_salesys: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Código Genesys</label>
                    <Input
                      value={formData.codigo_genesys}
                      onChange={(e) => setFormData({ ...formData, codigo_genesys: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Nombre Laraigo</label>
                    <Input
                      value={formData.nombre_laraigo}
                      onChange={(e) => setFormData({ ...formData, nombre_laraigo: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Nombre 360</label>
                    <Input
                      value={formData.nombre_360}
                      onChange={(e) => setFormData({ ...formData, nombre_360: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Código Navicat</label>
                    <Input
                      value={formData.codigo_navicat}
                      onChange={(e) => setFormData({ ...formData, codigo_navicat: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Código IPCC</label>
                    <Input
                      value={formData.codigo_ipcc}
                      onChange={(e) => setFormData({ ...formData, codigo_ipcc: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Condición</label>
                    <Select
                      value={formData.condicion}
                      onValueChange={(value) => setFormData({ ...formData, condicion: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Permanente">Permanente</SelectItem>
                        <SelectItem value="Temporal">Temporal</SelectItem>
                        <SelectItem value="Contratista">Contratista</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Cargo</label>
                    <Select
                      value={formData.cargo}
                      onValueChange={(value) => setFormData({ ...formData, cargo: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Analista">Analista</SelectItem>
                        <SelectItem value="Supervisor">Supervisor</SelectItem>
                        <SelectItem value="Coordinador">Coordinador</SelectItem>
                        <SelectItem value="Gerente">Gerente</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Sub Cargo</label>
                    <Select
                      value={formData.sub_cargo}
                      onValueChange={(value) => setFormData({ ...formData, sub_cargo: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Analista Junior">Analista Junior</SelectItem>
                        <SelectItem value="Analista Pleno">Analista Pleno</SelectItem>
                        <SelectItem value="Analista Senior">Analista Senior</SelectItem>
                        <SelectItem value="Supervisor de Equipo">Supervisor de Equipo</SelectItem>
                        <SelectItem value="Coordinador de Calidad">Coordinador de Calidad</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Campaña</label>
                    <Select
                      value={formData.campaña}
                      onValueChange={(value) => setFormData({ ...formData, campaña: value })}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Activaciones">Activaciones</SelectItem>
                        <SelectItem value="Aghaso">Aghaso</SelectItem>
                        <SelectItem value="Delivery">Delivery</SelectItem>
                        <SelectItem value="Foto Corporativo">Foto Corporativo</SelectItem>
                        <SelectItem value="Foto Alambrico">Foto Alambrico</SelectItem>
                        <SelectItem value="NPS">NPS</SelectItem>
                        <SelectItem value="MultiSkill">MultiSkill</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Estado</label>
                    <Select
                      value={formData.estado}
                      onValueChange={(value) =>
                        setFormData({ ...formData, estado: value as "Activo" | "Inactivo" | "Licencia" })
                      }
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Activo">Activo</SelectItem>
                        <SelectItem value="Inactivo">Inactivo</SelectItem>
                        <SelectItem value="Licencia">Licencia</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Fecha Ingreso Campaña</label>
                    <Input
                      type="date"
                      value={formData.fecha_ingreso_campaña}
                      onChange={(e) => setFormData({ ...formData, fecha_ingreso_campaña: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Hora Entrada</label>
                    <Input
                      type="time"
                      value={formData.hora_entrada}
                      onChange={(e) => setFormData({ ...formData, hora_entrada: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Hora Salida</label>
                    <Input
                      type="time"
                      value={formData.hora_salida}
                      onChange={(e) => setFormData({ ...formData, hora_salida: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Supervisor</label>
                    <Input
                      value={formData.supervisor}
                      onChange={(e) => setFormData({ ...formData, supervisor: e.target.value })}
                    />
                  </div>
                  <div>
                    <label className="text-sm text-muted-foreground mb-1 block">Asistencia Detalle</label>
                    <Input
                      value={formData.asistencia_detalle}
                      onChange={(e) => setFormData({ ...formData, asistencia_detalle: e.target.value })}
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="text-sm text-muted-foreground mb-1 block">Observación</label>
                    <Input
                      value={formData.observacion}
                      onChange={(e) => setFormData({ ...formData, observacion: e.target.value })}
                    />
                  </div>
                </div>

                <div className="mt-6 flex justify-end gap-2">
                  <Button onClick={() => setShowAddModal(false)} variant="outline">
                    Cancelar
                  </Button>
                  <Button onClick={handleSavePersonal}>Guardar Cambios</Button>
                </div>
              </div>
            </Card>
          </div>
        )}

        {showViewModal && viewingPerson && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex justify-between items-center mb-6">
                  <h2 className="text-2xl font-semibold text-foreground">Detalles del Personal</h2>
                  <Button onClick={() => setShowViewModal(false)} variant="ghost" size="sm" className="h-8 w-8 p-0">
                    <X className="h-4 w-4" />
                  </Button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-muted-foreground">Fecha</p>
                    <p className="text-foreground font-medium">{viewingPerson.fecha}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">DNI</p>
                    <p className="text-foreground font-medium">{viewingPerson.dni}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Nombre Completo</p>
                    <p className="text-foreground font-medium">{viewingPerson.nombre_completo}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Código SaleSys</p>
                    <p className="text-foreground font-medium">{viewingPerson.codigo_salesys}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Código Genesys</p>
                    <p className="text-foreground font-medium">{viewingPerson.codigo_genesys}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Nombre Laraigo</p>
                    <p className="text-foreground font-medium">{viewingPerson.nombre_laraigo}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Nombre 360</p>
                    <p className="text-foreground font-medium">{viewingPerson.nombre_360}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Código Navicat</p>
                    <p className="text-foreground font-medium">{viewingPerson.codigo_navicat}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Código IPCC</p>
                    <p className="text-foreground font-medium">{viewingPerson.codigo_ipcc}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Condición</p>
                    <p className="text-foreground font-medium">{viewingPerson.condicion}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Cargo</p>
                    <p className="text-foreground font-medium">{viewingPerson.cargo}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Sub Cargo</p>
                    <p className="text-foreground font-medium">{viewingPerson.sub_cargo}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Campaña</p>
                    <p className="text-foreground font-medium">{viewingPerson.campaña}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Estado</p>
                    <Badge
                      variant={
                        viewingPerson.estado === "Activo"
                          ? "default"
                          : viewingPerson.estado === "Inactivo"
                            ? "secondary"
                            : "outline"
                      }
                    >
                      {viewingPerson.estado}
                    </Badge>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Fecha Ingreso Campaña</p>
                    <p className="text-foreground font-medium">{viewingPerson.fecha_ingreso_campaña}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Hora Entrada</p>
                    <p className="text-foreground font-medium">{viewingPerson.hora_entrada}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Hora Salida</p>
                    <p className="text-foreground font-medium">{viewingPerson.hora_salida}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Supervisor</p>
                    <p className="text-foreground font-medium">{viewingPerson.supervisor}</p>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Asistencia Detalle</p>
                    <p className="text-foreground font-medium">{viewingPerson.asistencia_detalle}</p>
                  </div>
                  <div className="md:col-span-2">
                    <p className="text-sm text-muted-foreground">Observación</p>
                    <p className="text-foreground font-medium">{viewingPerson.observacion}</p>
                  </div>
                </div>

                <div className="mt-6 flex justify-end gap-2">
                  <Button onClick={() => setShowViewModal(false)} variant="outline">
                    Cerrar
                  </Button>
                </div>
              </div>
            </Card>
          </div>
        )}
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

"use client"

import {
  Home,
  Megaphone,
  Users,
  Settings,
  ChevronDown,
  ChevronRight,
  Phone,
  LogOut,
  KeyRound,
  Sun,
  Moon,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { useState } from "react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { useTheme } from "@/components/theme-provider"

interface SidebarProps {
  activeSection: string | null
  activeSubSection: string | null
  onNavigate: (section: string, subSection: string) => void
}

const menuItems = [
  {
    id: "inicio",
    label: "Inicio",
    icon: Home,
    subItems: [],
  },
  {
    id: "campanas",
    label: "Campañas",
    icon: Megaphone,
    subItems: [
      { id: "activaciones", label: "Activaciones" },
      { id: "aghaso", label: "Aghaso" },
      { id: "delivery", label: "Delivery" },
      { id: "foto-corporativo", label: "Foto Corporativo" },
      { id: "foto-alambrico", label: "Foto Alambrico" },
    ],
  },
  {
    id: "analistas",
    label: "Analistas",
    icon: Users,
    subItems: [
      { id: "conexiones", label: "Conexiones" },
      { id: "campanas", label: "Campañas" },
      { id: "scraping", label: "Scraping" },
    ],
  },
  {
    id: "configuracion",
    label: "Configuración",
    icon: Settings,
    subItems: [
      { id: "general", label: "General" },
      { id: "usuarios", label: "Usuarios" },
      { id: "integraciones", label: "Integraciones" },
    ],
  },
]

export function Sidebar({ activeSection, activeSubSection, onNavigate }: SidebarProps) {
  const [expandedSections, setExpandedSections] = useState<string[]>([])
  const { theme, setTheme } = useTheme()

  const toggleSection = (sectionId: string) => {
    setExpandedSections((prev) =>
      prev.includes(sectionId) ? prev.filter((id) => id !== sectionId) : [...prev, sectionId],
    )
  }

  return (
    <aside className="w-64 bg-sidebar border-r border-sidebar-border flex flex-col">
      <div className="p-6 border-b border-sidebar-border">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
            <Phone className="w-5 h-5 text-primary-foreground" />
          </div>
          <div className="flex-1">
            <h1 className="text-lg font-semibold text-sidebar-foreground">Sys-Analistas</h1>
            <p className="text-xs text-muted-foreground">Sistema de Gestión</p>
          </div>
          <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="p-2 rounded-lg hover:bg-sidebar-accent/30 transition-colors"
            aria-label="Toggle theme"
          >
            {theme === "dark" ? (
              <Sun className="w-4 h-4 text-sidebar-foreground" />
            ) : (
              <Moon className="w-4 h-4 text-sidebar-foreground" />
            )}
          </button>
        </div>
      </div>

      <nav className="flex-1 p-4 overflow-y-auto">
        <div className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon
            const isExpanded = expandedSections.includes(item.id)
            const isSectionActive = activeSection === item.id

            return (
              <div key={item.id}>
                <button
                  onClick={() => toggleSection(item.id)}
                  className={cn(
                    "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                    isSectionActive
                      ? "bg-sidebar-accent/50 text-sidebar-accent-foreground"
                      : "text-sidebar-foreground hover:bg-sidebar-accent/30",
                  )}
                >
                  <Icon className="w-4 h-4" />
                  <span className="flex-1 text-left">{item.label}</span>
                  {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                </button>

                {isExpanded && item.subItems.length > 0 && (
                  <div className="ml-7 mt-1 space-y-1">
                    {item.subItems.map((subItem) => {
                      const isSubActive = activeSection === item.id && activeSubSection === subItem.id

                      return (
                        <button
                          key={subItem.id}
                          onClick={() => onNavigate(item.id, subItem.id)}
                          className={cn(
                            "w-full text-left px-3 py-2 rounded-md text-sm transition-colors",
                            isSubActive
                              ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium"
                              : "text-muted-foreground hover:text-sidebar-foreground hover:bg-sidebar-accent/30",
                          )}
                        >
                          {subItem.label}
                        </button>
                      )
                    })}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </nav>

      <div className="p-4 border-t border-sidebar-border">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <button className="w-full flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-sidebar-accent/30 transition-colors">
              <div className="w-8 h-8 bg-muted rounded-full flex items-center justify-center">
                <span className="text-xs font-semibold">AD</span>
              </div>
              <div className="flex-1 min-w-0 text-left">
                <p className="text-sm font-medium text-sidebar-foreground truncate">Admin User</p>
                <p className="text-xs text-muted-foreground truncate">admin@sys-analistas.com</p>
              </div>
              <ChevronDown className="w-4 h-4 text-muted-foreground" />
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuItem>
              <KeyRound className="w-4 h-4 mr-2" />
              Cambiar contraseña
            </DropdownMenuItem>
            <DropdownMenuItem className="text-red-600">
              <LogOut className="w-4 h-4 mr-2" />
              Cerrar sesión
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </aside>
  )
}

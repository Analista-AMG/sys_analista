# Módulo de Scraping - Analistas

## 📋 Objetivo Principal

Sistema de gestión y ejecución de scraping automatizado para extracción de datos de múltiples plataformas.

---

## 🎯 Funcionalidades Requeridas

### 1. Configuración de Scraping
- **Rango de fechas**: Fecha inicio y fecha fin
  - Restricción: Máximo 30 días hacia atrás
  - Validación: Fecha final debe ser mayor o igual a fecha inicial
- **Selección de plataformas**: Múltiples plataformas simultáneas
  - Salesys (con sub-opciones)
  - Laraigo (con sub-opciones)
  - Navicat (con sub-opciones)
  - 360 (con sub-opciones)
  - Más plataformas en el futuro
- **Sub-opciones por plataforma**: Cada plataforma tiene diferentes tipos de reportes/acciones
- **Programación de ejecución**:
  - Ahora (inmediato)
  - 5 minutos
  - 10 minutos
  - 15 minutos
  - 30 minutos
  - 60 minutos

### 2. Ejecución en Tiempo Real
- **Barra de progreso visual**: Mostrar avance del scraping
- **Botón cancelar**: Detener ejecución en cualquier momento
- **Solo visible si hay scraping activo**

### 3. Historial de Scrapings
- **Últimos 10 registros**: Tabla con historial reciente
- **Información mostrada**:
  - Fecha y hora de ejecución
  - Plataformas utilizadas
  - Archivos generados
  - Estado (Completado / Error / En Proceso)
  - Rastro de ejecución

---

## 🏗️ Arquitectura de Componentes

### Estructura de Archivos

```
/components/analistas/scraping/
├── README.md                          (este archivo)
├── types.ts                           (Interfaces TypeScript)
├── scraping-panel.tsx                 (Contenedor principal - Opción A)
├── scraping-config-form.tsx           (Formulario de configuración)
├── scraping-execution.tsx             (Barra progreso + cancelar)
└── scraping-history-table.tsx         (Tabla de historial)
```

### Responsabilidades por Archivo

#### `types.ts`
- Interfaces de plataformas
- Tipos de reportes/sub-opciones
- Interface de ScrapingJob
- Estados de ejecución
- Tipos de historial

#### `scraping-panel.tsx`
- **Contenedor principal** que organiza todo
- Implementa **Opción A** (todo en una vista):
  ```
  ┌─────────────────────────────────────┐
  │  CONFIGURACIÓN DE SCRAPING          │
  │  (scraping-config-form)             │
  ├─────────────────────────────────────┤
  │  SCRAPING EN EJECUCIÓN (condicional)│
  │  (scraping-execution)               │
  ├─────────────────────────────────────┤
  │  HISTORIAL (últimos 10)             │
  │  (scraping-history-table)           │
  └─────────────────────────────────────┘
  ```
- Maneja estado global del scraping
- Coordina comunicación entre componentes

#### `scraping-config-form.tsx`
- Campos de fecha inicio y fin
- Selector de plataformas (múltiple)
- Sub-opciones dinámicas por plataforma seleccionada
- Selector de programación
- Botón "Ejecutar Scraping"
- Validaciones de formulario

#### `scraping-execution.tsx`
- Solo se renderiza si hay scraping activo
- Muestra progreso en tiempo real
- Permite cancelar ejecución
- Indicadores visuales del estado actual

#### `scraping-history-table.tsx`
- Tabla responsive con últimos 10 scrapings
- Información detallada de cada ejecución
- Estados visuales con badges (success/warning/pending)
- Posible acción para re-ejecutar o ver detalles

---

## 🔗 Integración con Vista Principal

### Modificación en `analistas-view.tsx`
```tsx
import { ScrapingPanel } from '@/components/analistas/scraping/scraping-panel'

export function AnalistasView({ subSection }: AnalistasViewProps) {
  // ... código existente ...

  if (subSection === "scraping") {
    return <ScrapingPanel />
  }

  // ... resto del código ...
}
```

**Cambio mínimo**: Solo importar y renderizar el componente principal.

---

## 🔄 Recursos Reutilizados del Proyecto General

Este módulo **NO es independiente**, está integrado en la aplicación principal y reutiliza componentes compartidos.

### 1️⃣ Componentes UI de `/components/ui/`

```tsx
// Formularios
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

// Contenedores
import { Card } from "@/components/ui/card"

// Feedback
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"

// Tablas
import { Table } from "@/components/ui/table"
```

### 2️⃣ Estilos Globales de `/app/globals.css`

```css
/* Variables CSS que usaremos */
--primary: oklch(0.62 0.21 35)           /* Naranja #F54927 */
--success: oklch(0.77 0.15 165)          /* Verde #34D399 */
--warning: oklch(0.78 0.15 75)           /* Amarillo #FBBF24 */
--pending: oklch(0.68 0.015 250)         /* Gris azulado #94A3B8 */
--pending-foreground: oklch(0.98 0 0)    /* Texto blanco */
--background, --foreground, --border, --card, etc.
```

### 3️⃣ Sistema de Temas de `/components/theme-provider.tsx`

```tsx
import { useTheme } from "@/components/theme-provider"
// El módulo respeta automáticamente el modo claro/oscuro
```

### 4️⃣ Utilidades de `/lib/utils.ts`

```tsx
import { cn } from "@/lib/utils"
// Función para combinar clases CSS con Tailwind
```

### 5️⃣ Hooks Personalizados de `/hooks/`

```tsx
import { useToast } from "@/hooks/use-toast"
// Para notificaciones de éxito/error
```

### 6️⃣ Layout y Estructura

```
call-center-layout.tsx
    ↓
main-content.tsx
    ↓
analistas-view.tsx
    ↓
scraping-panel.tsx (nuestro módulo)
```

El módulo hereda:
- Sidebar de navegación
- Header con tema
- Estilos globales
- Sistema de routing

### 7️⃣ Configuración de Next.js

```tsx
// next.config.mjs - Configuración del proyecto
// tsconfig.json - Aliases @/ paths
// tailwind.config - Clases y temas personalizados
```

### 8️⃣ Tipado TypeScript

```tsx
// Convenciones de nomenclatura del proyecto
// Interfaces base si existen
// Patrones de código establecidos
```

### ❌ Lo que NO reutilizamos:

- Lógica de negocio de otras vistas (campañas, agentes, etc.)
- Estados de otros componentes
- Datos mock específicos de otras secciones
- Formularios de otras funcionalidades

### ✅ Ventajas de esta Integración:

1. **Consistencia visual**: Mismo look & feel que el resto de la app
2. **No duplicar código**: Reutilizamos componentes ya testeados
3. **Mantenimiento fácil**: Un cambio en UI afecta todo el sistema
4. **Temas automáticos**: Dark/Light mode sin configuración extra
5. **TypeScript compartido**: Mismos tipos y validaciones

---

## 🎨 Diseño Visual

### Paleta de Colores (ya configurada)
- **Completado**: Verde coral `#34D399` (success)
- **En Proceso**: Amarillo ámbar `#FBBF24` (warning)
- **Pendiente**: Gris azulado `#94A3B8` (pending)
- **Principal**: Naranja `#F54927` (primary)

### Componentes UI Utilizados
- Card (contenedores)
- Button (acciones)
- Input (fechas)
- Select (plataformas, programación)
- Checkbox (sub-opciones múltiples)
- Badge (estados)
- Progress (barra de progreso)
- Table (historial)
- Label (etiquetas)

---

## ⚙️ Backend (Python)

**Importante**: El scraping ya está implementado en Python con clases abstractas.
- El frontend solo debe enviar los parámetros al backend
- El backend maneja la ejecución en cadena
- Los archivos se guardan en su ubicación correspondiente
- Otra parte de la web maneja la carga de datos

**El frontend NO ejecuta el scraping**, solo lo configura y monitorea.

---

## 📝 Notas Importantes

1. **Ejecución en cadena**: El sistema puede ejecutar múltiples scrapings secuencialmente
   - Ejemplo: Salesys (3/5 opciones) + Laraigo (2/4 opciones)

2. **Validaciones críticas**:
   - Fecha final >= Fecha inicial (error directo si no cumple)
   - Máximo 30 días hacia atrás desde hoy

3. **Archivos generados**: Los scrapings dejan archivos en el servidor
   - El historial debe marcar qué archivos se generaron
   - Rastreo de hora de ejecución

4. **Diseño modular**: Fácil agregar nuevas plataformas en el futuro

---

## 🚀 Estado del Proyecto

- [ ] Crear estructura de carpetas
- [ ] Definir interfaces en `types.ts`
- [ ] Implementar `scraping-config-form.tsx`
- [ ] Implementar `scraping-execution.tsx`
- [ ] Implementar `scraping-history-table.tsx`
- [ ] Implementar `scraping-panel.tsx`
- [ ] Modificar `analistas-view.tsx`
- [ ] Pruebas de integración
- [ ] Conectar con backend Python

---

**Última actualización**: 2025-10-16
**Desarrollador**: Sistema Call Center - Módulo Analistas

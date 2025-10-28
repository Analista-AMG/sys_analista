# Estructura del Proyecto - Sistema Call Center

## 📋 Resumen General
Este es un proyecto de call center desarrollado con **Next.js 14+**, **React**, **TypeScript** y **shadcn/ui**. Incluye también scripts en Python para backend/procesamiento.

---

## 🗂️ Estructura de Directorios

### 📁 `/app` - Directorio principal de Next.js (App Router)
Utiliza el nuevo sistema de enrutamiento de Next.js 13+.

- **`layout.tsx`** - Layout raíz de la aplicación
  - Define la estructura HTML base
  - Configura providers globales (temas, contextos)
  - Importa fuentes y metadatos

- **`page.tsx`** - Página principal (ruta `/`)
  - Punto de entrada de la aplicación
  - Probablemente renderiza el dashboard o vista de inicio

- **`globals.css`** - Estilos globales de la aplicación
  - Variables CSS personalizadas
  - Configuración de Tailwind
  - Estilos base y resets

---

### 📁 `/components` - Componentes de React

#### **`call-center-layout.tsx`**
Layout específico del sistema de call center con:
- Navegación principal
- Áreas de contenido
- Posiblemente header/footer

#### **`main-content.tsx`**
Componente que gestiona el contenido principal:
- Renderización condicional de vistas
- Manejo de estado de navegación

#### **`sidebar.tsx`**
Barra lateral de navegación con:
- Menú de opciones
- Enlaces a diferentes secciones
- Posible información de usuario

#### **`theme-provider.tsx`**
Proveedor de contexto para temas:
- Gestión de modo claro/oscuro
- Configuración de colores
- Persistencia de preferencias

---

### 📁 `/components/ui` - Componentes de UI (shadcn/ui)
Biblioteca de componentes reutilizables basados en Radix UI y Tailwind CSS.

**Componentes de Navegación:**
- `navigation-menu.tsx` - Menú de navegación
- `breadcrumb.tsx` - Migas de pan para navegación
- `menubar.tsx` - Barra de menú
- `sidebar.tsx` - Componente sidebar reutilizable
- `command.tsx` - Paleta de comandos (Cmd+K)
- `tabs.tsx` - Sistema de pestañas

**Componentes de Formulario:**
- `form.tsx` - Wrapper de formularios con validación
- `input.tsx` - Campo de entrada de texto
- `textarea.tsx` - Área de texto
- `select.tsx` - Selector desplegable
- `checkbox.tsx` - Casilla de verificación
- `radio-group.tsx` - Grupo de botones radio
- `switch.tsx` - Interruptor toggle
- `slider.tsx` - Control deslizante
- `calendar.tsx` - Selector de fecha
- `input-otp.tsx` - Input para códigos OTP
- `input-group.tsx` - Agrupación de inputs
- `label.tsx` - Etiquetas de formulario
- `field.tsx` - Campo de formulario completo

**Componentes de Retroalimentación:**
- `alert.tsx` - Alertas informativas
- `alert-dialog.tsx` - Diálogos de alerta modales
- `toast.tsx` - Notificaciones temporales
- `toaster.tsx` - Contenedor de toasts
- `use-toast.ts` - Hook para gestionar toasts
- `progress.tsx` - Barra de progreso
- `spinner.tsx` - Indicador de carga
- `skeleton.tsx` - Placeholder de carga

**Componentes de Overlay:**
- `dialog.tsx` - Diálogos modales
- `sheet.tsx` - Panel lateral deslizable
- `drawer.tsx` - Cajón deslizable
- `popover.tsx` - Ventana emergente
- `hover-card.tsx` - Tarjeta al pasar el mouse
- `tooltip.tsx` - Información al hover
- `dropdown-menu.tsx` - Menú desplegable
- `context-menu.tsx` - Menú contextual

**Componentes de Visualización:**
- `card.tsx` - Tarjetas contenedoras
- `table.tsx` - Tablas de datos
- `chart.tsx` - Gráficos y visualizaciones
- `badge.tsx` - Etiquetas/badges
- `avatar.tsx` - Imagen de avatar
- `empty.tsx` - Estado vacío
- `item.tsx` - Elemento de lista genérico

**Componentes de Layout:**
- `separator.tsx` - Línea separadora
- `scroll-area.tsx` - Área con scroll personalizado
- `resizable.tsx` - Paneles redimensionables
- `aspect-ratio.tsx` - Contenedor con ratio fijo
- `collapsible.tsx` - Contenido colapsable
- `accordion.tsx` - Acordeón expandible
- `carousel.tsx` - Carrusel de contenido

**Componentes de Interacción:**
- `button.tsx` - Botón estándar
- `button-group.tsx` - Grupo de botones
- `toggle.tsx` - Botón de alternancia
- `toggle-group.tsx` - Grupo de toggles
- `pagination.tsx` - Paginación de datos
- `kbd.tsx` - Representación de teclas

**Hooks y Utilidades:**
- `use-mobile.tsx` - Detección de dispositivos móviles
- `use-toast.ts` - Gestión de notificaciones

---

### 📁 `/components/views` - Vistas de la aplicación
Componentes de página completa para cada sección del call center.

- **`inicio-view.tsx`** - Vista de inicio/bienvenida
  - Dashboard general
  - Resumen de actividades

- **`dashboard-view.tsx`** - Dashboard principal
  - Métricas en tiempo real
  - Gráficos y estadísticas
  - KPIs del call center

- **`agentes-view.tsx`** - Gestión de agentes
  - Lista de agentes
  - Estados (disponible, ocupado, descanso)
  - Métricas por agente

- **`analistas-view.tsx`** - Gestión de analistas
  - Supervisores/analistas del sistema
  - Permisos y roles
  - Asignaciones

- **`llamadas-view.tsx`** - Registro de llamadas
  - Historial de llamadas
  - Estado (en curso, completadas, perdidas)
  - Grabaciones y notas

- **`clientes-view.tsx`** - Base de datos de clientes
  - Información de contacto
  - Historial de interacciones
  - Segmentación

- **`campanas-view.tsx`** - Gestión de campañas
  - Campañas activas/inactivas
  - Objetivos y métricas
  - Configuración de campañas

- **`reportes-view.tsx`** - Sistema de reportes
  - Generación de informes
  - Análisis de datos
  - Exportación de reportes

- **`configuracion-view.tsx`** - Configuración del sistema
  - Parámetros generales
  - Integraciones
  - Preferencias de usuario

---

### 📁 `/hooks` - Custom React Hooks
Lógica reutilizable para componentes.

- **`use-mobile.ts`** - Hook para detectar dispositivos móviles
  - Media queries
  - Responsive behavior

- **`use-toast.ts`** - Hook para gestionar notificaciones
  - Mostrar/ocultar toasts
  - Cola de notificaciones

---

### 📁 `/lib` - Utilidades y funciones auxiliares

- **`utils.ts`** - Funciones de utilidad
  - Helpers generales
  - Función `cn()` para clases de Tailwind
  - Formateo de datos
  - Validaciones

---

### 📁 `/scripts` - Scripts de Python
Backend o procesamiento de datos.

- **`app.py`** - Aplicación Python principal
  - Posible API Flask/FastAPI
  - Procesamiento de datos
  - Integración con sistemas externos

- **`requirements.txt`** - Dependencias de Python
  - Lista de paquetes necesarios
  - Versiones específicas

- **`README.md`** - Documentación de scripts
  - Instrucciones de uso
  - Configuración del entorno Python

---

### 📁 `/styles` - Estilos adicionales

- **`globals.css`** - Estilos globales alternativos
  - Podría ser duplicado de app/globals.css
  - O estilos específicos para componentes legacy

---

### 📁 `/public` - Archivos estáticos
- Imágenes
- Iconos
- Fuentes
- Assets públicos

---

### 📁 `/marco_papa` - Documentación o recursos
- **`asd.txt`** - Archivo de texto (contenido desconocido)
- **`marco_papa_2.txt`** (raíz) - Posible documentación o notas

---

### 📁 `/.claude` - Configuración de Claude Code
Configuración para el asistente de IA Claude Code.

---

## 📄 Archivos de Configuración Raíz

### **`package.json`**
- Dependencias del proyecto
- Scripts de desarrollo/build
- Metadata del proyecto

### **`package-lock.json`**
- Versiones exactas de dependencias
- Árbol de dependencias bloqueado

### **`pnpm-lock.yaml`**
- Lock file de pnpm (gestor de paquetes alternativo)

### **`tsconfig.json`**
- Configuración de TypeScript
- Paths aliases
- Opciones del compilador

### **`next.config.mjs`**
- Configuración de Next.js
- Webpack customization
- Variables de entorno
- Redirects y rewrites

### **`postcss.config.mjs`**
- Configuración de PostCSS
- Plugins (Tailwind, Autoprefixer)

### **`components.json`**
- Configuración de shadcn/ui
- Paths de componentes
- Temas y estilos

### **`.gitignore`**
- Archivos ignorados por Git
- node_modules, .next, etc.

### **`README.md`**
- Documentación del proyecto
- Instrucciones de instalación
- Guía de uso

---

## 🏗️ Stack Tecnológico Identificado

**Frontend:**
- Next.js 14+ (App Router)
- React 18+
- TypeScript
- Tailwind CSS
- shadcn/ui (Radix UI)
- Sonner (Toasts)

**Backend/Scripts:**
- Python (Flask/FastAPI probable)

**Desarrollo:**
- Git (control de versiones)
- pnpm/npm (gestión de paquetes)
- ESLint/Prettier (probables)

---

## 🎯 Propósito del Proyecto

Sistema de gestión de call center con:
- Dashboard de métricas en tiempo real
- Gestión de agentes y analistas
- Registro y seguimiento de llamadas
- Base de datos de clientes
- Gestión de campañas
- Sistema de reportes
- Configuración personalizable
- Interfaz responsive y moderna

---

## 📝 Notas

- El proyecto usa el **App Router** de Next.js (no Pages Router)
- Todos los componentes UI están basados en **shadcn/ui** (altamente personalizables)
- Hay scripts Python separados que probablemente manejan procesamiento backend
- Sistema modular con vistas separadas para cada funcionalidad
- Implementación completa de sistema de diseño con temas

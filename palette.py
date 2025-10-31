# ---------------- Paletas de Temas Mejoradas ----------------

# Paleta para el Modo Claro (Teal Moderno Refinado)
LIGHT_PALETTE = {
    # Fondo General: Gris muy claro con toque cálido
    "bg": "#F8FAFC", 
    # Texto Principal: Gris pizarra muy oscuro para máximo contraste
    "fg": "#0F172A", 
    # Texto Muted/Secundario: Gris medio equilibrado
    "muted": "#64748B", 
    # Borde de Elementos: Gris claro suave
    "border": "#CBD5E1", 
    
    # Primario (Acción Principal): Teal vibrante y profesional
    "primary": "#0D9488", 
    # Primario Hover: Teal más oscuro con mayor saturación
    "primary_hover": "#0F766E", 
    
    # Acento/Progreso: Teal medio brillante
    "accent": "#14B8A6", 
    # Danger/Error: Rojo saturado pero no agresivo
    "danger": "#DC2626", 
    
    # Superficie (Fondo de Tarjeta/Entry): Blanco puro
    "surface": "#FFFFFF", 
    # Fondo de Trough (Barra de Progreso): Gris muy claro
    "trough": "#E2E8F0",
}

# Paleta para el Modo Oscuro (Contraste Optimizado)
DARK_PALETTE = {
    # Fondo General: Gris azulado oscuro profundo
    "bg": "#0F172A", 
    # Texto Principal: Casi blanco con leve tinte azul
    "fg": "#F1F5F9", 
    # Texto Muted/Secundario: Gris claro equilibrado
    "muted": "#94A3B8", 
    # Borde de Elementos: Gris medio-oscuro con contraste suficiente
    "border": "#475569", 
    
    # Primario (Acción Principal): Teal brillante para alta visibilidad
    "primary": "#14B8A6", 
    # Primario Hover: Teal más claro para feedback visual claro
    "primary_hover": "#2DD4BF", 
    
    # Acento/Progreso: Cyan brillante para máximo contraste
    "accent": "#22D3EE", 
    # Danger/Error: Rojo coral suave para modo oscuro
    "danger": "#F87171", 
    
    # Superficie (Fondo de Tarjeta/Entry): Gris oscuro elevado
    "surface": "#1E293B", 
    # Fondo de Trough (Barra de Progreso): Gris oscuro con contraste
    "trough": "#334155",
}

# Mapa de todas las paletas para facilitar la selección de temas
THEME_PALETTES = {
    "light": LIGHT_PALETTE,
    "dark": DARK_PALETTE
}

# PALETTE por defecto (alias de LIGHT_PALETTE) para compatibilidad
PALETTE = LIGHT_PALETTE

# Mejoras implementadas:
# 1. Mayor contraste en ambos temas para mejor legibilidad
# 2. Colores primarios más vibrantes y distintivos
# 3. Bordes más visibles en modo oscuro
# 4. Superficie con mejor separación del fondo en modo oscuro
# 5. Colores de acento más brillantes para elementos interactivos
# 6. Paleta teal/cyan consistente y moderna en ambos temas
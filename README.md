# Sistema Inteligente de Rutas MIO de Cali

## Descripción
Sistema inteligente basado en conocimiento que utiliza el algoritmo A* y reglas lógicas para encontrar la mejor ruta en el sistema de transporte masivo MIO de Cali.

## Características
- **Base de conocimiento**: 30+ estaciones, 4 rutas (T31, E21, P27D, P41)
- **Algoritmo A***: Búsqueda heurística con distancia euclidiana
- **Reglas lógicas**: Penalización por transbordos, ajuste por congestión horaria
- **API REST**: Endpoints para consultar estaciones y rutas
- **Interfaz moderna**: Frontend responsive con visualización de resultados

### 1. Requisitos previos
- Python 3.8 o superior
- Pip (gestor de paquetes)
 
## Como ejecutar
1. Clonar el repositorio de https://github.com/DayannaCoral19/sistema-mio-cali.git
2. Abrir cd sistema-mio-cali
3. Instalar dependencias pip install -r requirements.txt
4. Ejecutar servidor python backend/app.py
5. Abrir en el navegador http://localhost:5000

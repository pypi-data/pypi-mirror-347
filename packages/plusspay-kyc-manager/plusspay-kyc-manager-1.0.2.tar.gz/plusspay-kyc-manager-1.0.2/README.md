# Plusspay KYC Manager

Librería de Plusspay© para la gestión de procesos KYC (Know Your Customer) a través de diferentes proveedores.

## Descripción

Plusspay KYC Manager es una librería que proporciona una interfaz unificada para interactuar con diferentes proveedores de servicios KYC. Actualmente soporta los siguientes proveedores:

- DIDIT: Servicio de verificación de identidad con soporte para OCR, NFC y reconocimiento facial.

## Instalación

La librería se instala automáticamente como parte del proyecto Plusspay. No requiere instalación adicional.

## Configuración

### Variables de Entorno

La librería requiere las siguientes variables de entorno para funcionar:

#### Variables Comunes
- `KYC_PROVIDER`: Proveedor de KYC a utilizar. Valores válidos: "DIDIT", "METAMASK"
- `KYC_CALLBACK_URL`: URL de callback para retornar al usuario a un lugar seguro una vez completado su proceso de verificación.

#### Variables Específicas para DIDIT
- `DIDIT_API_FEATURES`: Características de la API a utilizar. Ejemplo: "OCR + NFC + FACE"
- `DIDIT_CLIENT_ID`: ID de cliente proporcionado por DIDIT
- `DIDIT_CLIENT_SECRET`: Secret de cliente proporcionado por DIDIT

### Ejemplo de Configuración

```bash
# Variables comunes
export KYC_PROVIDER="DIDIT"
export KYC_CALLBACK_URL="https://tu-dominio.com/kyc/callback"

# Variables específicas para DIDIT
export DIDIT_API_FEATURES="OCR + NFC + FACE"
export DIDIT_CLIENT_ID="tu-client-id"
export DIDIT_CLIENT_SECRET="tu-client-secret"
```

## Uso

### Inicialización

```python
from apps.plusspay_kyc_manager.core import PlusspayKYCManager

# Crear instancia del manager
kyc_manager = PlusspayKYCManager()

# Configurar y validar el entorno y las variables
kyc_manager.set_environment()
```

### Obtener Información de la Librería

```python
# Obtener información completa de la librería
info = kyc_manager.get_full_info()
print(info)
```

### Crear una Sesión KYC

```python
# Crear una nueva sesión KYC
session = kyc_manager.create_session("usuario@ejemplo.com")

# La sesión contiene:
# - session_id: ID único de la sesión
# - session_url: URL para que el usuario complete el proceso KYC
# - status: Estado actual de la sesión
# - kyc_verify_types: Tipos de verificación configurados
# - vendor_data: Datos del usuario
```

### Obtener Datos de una Sesión

```python
# Obtener los datos de una sesión existente
session_data = kyc_manager.get_session_data("session-id")

# Los datos incluyen:
# - Información básica de la sesión
# - Datos del documento de identidad
# - Información personal del usuario
# - Estado de verificación
# - Ubicación del usuario
```

## Estructura de Datos

### Datos de Sesión

```python
{
    "provider": "DIDIT",
    "session_id": "id-unico",
    "session_url": "https://url-de-verificacion",
    "status": "Not Started|In Progress|Approved|Rejected",
    "kyc_verify_types": "OCR + NFC + FACE",
    "vendor_data": "usuario@ejemplo.com",
    "document_type": "ID|Passport",
    "document_number": "123456789",
    "first_name": "Nombre",
    "last_name": "Apellido",
    "full_name": "Nombre Completo",
    "date_of_birth": "YYYY-MM-DD",
    "gender": "M|F",
    "nationality": "País",
    "address": "Dirección",
    "ip_country": "País",
    "ip_country_code": "Código País"
}
```

## Manejo de Errores

La librería lanza las siguientes excepciones:

- `EnvironmentError`: Cuando hay problemas con la configuración del entorno
- `HTTPException`: Cuando hay errores en las llamadas a la API del proveedor

### Ejemplo de Manejo de Errores

```python
try:
    kyc_manager.set_environment()
except EnvironmentError as e:
    print(f"Error de configuración: {str(e)}")
except HTTPException as e:
    print(f"Error de API: {str(e)}")
```

## Licencia

MIT License - Ver archivo LICENSE para más detalles. 

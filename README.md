# 🌾 AgroSmart - Sistema de Gestión Agrícola

Sistema completo de gestión de cultivos con:
- ✅ Autenticación con verificación OTP por email
- ✅ Dashboard de clima en tiempo real con mapa interactivo
- ✅ Gestión multi-usuario de cultivos
- ✅ Panel administrativo para usuarios root
- ✅ Recomendaciones de riego inteligentes

## 📋 Requisitos

- Python 3.10+
- Django 5.1+
- Pip (gestor de paquetes de Python)
- Cuenta de Gmail con acceso a aplicaciones

## 🚀 Instalación Rápida

### 1. Clonar o descargar el proyecto

```bash
cd "e:\Proyecto Programación III\agrosmart"
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

Si no existe `requirements.txt`, instala manualmente:

```bash
pip install django
pip install django-environ
pip install requests
pip install python-dotenv
```

### 3. Configurar variables de entorno

Edita el archivo `.env` en la raíz del proyecto:
python manage.py runserver
```env
DEBUG=True
SECRET_KEY=tu_llave_secreta_de_django
WEATHER_API_KEY=tu_clave_de_weatherapi
DEFAULT_CITY=San Miguel
DEFAULT_COUNTRY=SV

# Gmail Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
```

### 4. Configurar Gmail (IMPORTANTE)

#### Opción A: Usar Contraseña de Aplicación (Recomendado)

1. Ve a https://myaccount.google.com
2. Haz clic en "Seguridad" → "Verificación en 2 pasos" (actívalo)
3. Ve a https://myaccount.google.com/apppasswords
4. Selecciona "Correo" y "Windows" (o tu sistema operativo)
5. Haz clic en "Generar"
6. Google te mostrará una contraseña de 16 caracteres
7. Copia esa contraseña (con espacios) y pégala en .env como `EMAIL_HOST_PASSWORD`

#### Opción B: Usar Aplicaciones Menos Seguras (No recomendado)

1. Ve a https://myaccount.google.com/lesssecureapps
2. Activa "Permitir aplicaciones menos seguras"
3. Usa tu contraseña normal de Gmail en .env

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear usuario root

```bash
python manage.py create_root_user
```

Esto crea:
- Email: `root@gmail.com`
- Contraseña: `Antho-XD07`

### 7. Probar email (Opcional)

```bash
python test_email.py
```

Deberías ver: ✅ EMAIL ENVIADO EXITOSAMENTE

### 8. Iniciar servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: http://127.0.0.1:8000

## 🔑 Cuentas Predefinidas

| Email | Contraseña | Rol |
|-------|-----------|-----|
| root@gmail.com | Antho-XD07 | Administrador (ve todos los cultivos) |

## 📱 Flujo de Uso

### Registro de Nuevo Usuario

1. Ve a http://127.0.0.1:8000/registro/
2. Ingresa tu email
3. Recibe un código OTP de 6 dígitos en tu correo
4. Verifica el código
5. Crea una contraseña
6. ¡Listo! Ahora puedes iniciar sesión

### Crear Cultivo

1. Inicia sesión
2. Haz clic en "Cultivos" → "Nuevo Cultivo"
3. Ingresa nombre, descripción, país
4. Haz clic en el mapa para marcar la ubicación (opcional)
5. Guarda

### Ver Dashboard

1. Haz clic en "Dashboard"
2. Verás:
   - 🗺️ Mapa interactivo con tus cultivos (pines verdes)
   - 📊 Datos de clima en tiempo real
   - 💡 Recomendaciones de riego
   - 🌦️ Capas de temperatura, nubes, precipitación

### Cambiar Entre Cultivos

1. En el mapa, haz **doble clic** en un pin verde (tu cultivo)
2. El dashboard se actualizará con datos de ese cultivo

### Panel Administrativo (Solo root)

1. Inicia sesión como root@gmail.com
2. Haz clic en "Admin Panel" (en rojo en la navegación)
3. Desde aquí puedes:
   - Ver todos los usuarios
   - Ver cultivos de cada usuario
   - Eliminar usuarios (y sus cultivos)

## 🗺️ Características del Mapa

- **Pines Verdes**: Tus cultivos (puedes hacer doble clic para cambiar)
- **Pines Grises**: Cultivos de otros usuarios (información)
- **Capas Meteorológicas**: Toggle de temperatura, nubes, precipitación
- **Zoom Dinámico**: Se centra en tu cultivo seleccionado

## 🔒 Seguridad

- Cada usuario solo ve sus propios cultivos
- Usuario root puede ver y gestionar todos los cultivos
- Autenticación por email con OTP
- Contraseñas hasheadas con PBKDF2
- CSRF protection en todos los formularios
- SQL injection prevention (ORM de Django)

## 🐛 Solucionar Problemas

### "Error al enviar el email"

**Causa**: EMAIL_HOST_USER o EMAIL_HOST_PASSWORD no configurados correctamente

**Solución**:
1. Ve a http://127.0.0.1:8000/configurar-gmail/ para instrucciones
2. Verifica que .env tenga las credenciales correctas
3. Ejecuta `python test_email.py` para probar
4. Reinicia el servidor Django (Ctrl+C, luego `python manage.py runserver`)

### "No puedo iniciar sesión"

**Causa**: Email no fue verificado durante el registro

**Solución**:
1. Completa el proceso de verificación por OTP
2. Si perdiste el código, haz clic en "Solicitar nuevo código"

### "La contraseña no es correcta"

**Causa**: Diferencia entre mayúsculas/minúsculas

**Solución**:
- Verifica que escribas correctamente la contraseña
- Mayúsculas y minúsculas importan
- Si olvidaste, regístrate de nuevo

## 📊 Base de Datos

El proyecto usa SQLite (archivo `agrosmart.db`). Los datos se guardan en:

- **Usuarios**: CustomUser
- **Verificaciones OTP**: EmailVerification
- **Cultivos**: Crop (con ForeignKey a CustomUser)
- **Clima**: WeatherRecord (histórico)

## 🔄 APIs Externas

- **OpenWeatherMap**: Datos meteorológicos (mapas)
- **WeatherAPI**: Datos de clima por ubicación
- **Gmail SMTP**: Envío de códigos OTP

## 📁 Estructura del Proyecto

```
agrosmart/
├── manage.py                    # Comando principal de Django
├── .env                         # Variables de entorno
├── agrosmart/
│   ├── settings.py             # Configuración
│   ├── urls.py                 # URLs principales
│   └── wsgi.py                 # WSGI para producción
├── monitor/
│   ├── models.py               # CustomUser, Crop, etc.
│   ├── views.py                # Vistas de cultivos
│   ├── views_auth.py           # Vistas de autenticación
│   ├── views_admin.py          # Vistas administrativas
│   ├── forms.py                # Formularios
│   ├── urls.py                 # URLs de la app
│   ├── services/
│   │   ├── weather.py          # Consultas de clima
│   │   └── recommender.py      # Recomendaciones de riego
│   └── management/commands/
│       └── create_root_user.py # Comando para crear root
├── templates/
│   ├── base.html               # Template base
│   ├── auth/                   # Templates de autenticación
│   ├── admin/                  # Templates administrativos
│   └── crops/                  # Templates de cultivos
├── static/
│   ├── css/                    # Estilos
│   └── js/                     # JavaScript
└── requirements.txt            # Dependencias
```

## 🎯 Roadmap Futuro

- [ ] Agregar más modelos de cultivos predefinidos
- [ ] Gráficos históricos de clima
- [ ] Notificaciones por SMS
- [ ] Exportación a PDF
- [ ] API REST pública
- [ ] App móvil

## 📝 Licencia

Este proyecto es de código abierto para fines educativos.

## 👨‍💻 Autor

Proyecto desarrollado como parte de Programación III.

---

**¿Necesitas ayuda?** Revisa la página de configuración en http://127.0.0.1:8000/configurar-gmail/

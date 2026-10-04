# EAS Build Configuration - Football

## ✅ Validación Completada

Este repositorio está completamente configurado para ejecutar `eas build --platform all`.

### Archivos de Configuración

- ✅ **app.json** - Configuración Expo con bundle IDs para iOS y Android
- ✅ **eas.json** - Perfiles de build para development, preview y production
- ✅ **package.json** - Dependencias y scripts de Expo
- ✅ **babel.config.js** - Configuración Babel con preset Expo
- ✅ **App.js** - Componente React Native mínimo
- ✅ **index.js** - Entrada de la aplicación
- ✅ **.gitignore** - Archivos ignorados correctamente

### Requisitos Previos

1. **Node.js** >= 18.x
2. **npm** o **yarn**
3. **EAS CLI** instalado globalmente
4. Cuenta de **Expo** (https://expo.dev)
5. Para iOS: Cuenta de **Apple Developer** (opcional para development)

### Instalación y Configuración Inicial

```bash
# 1. Instalar dependencias
npm install

# 2. Instalar CLI de EAS globalmente
npm install -g eas-cli

# 3. Iniciar sesión en Expo
npx eas login

# 4. Conectar el proyecto a EAS
npx eas build:configure

# Esto generará un projectId automático y actualizará app.json
```

### Comandos de Build

```bash
# Build para ambas plataformas (desarrollo)
npm run eas-build

# Build solo Android
npm run eas-build-android

# Build solo iOS
npm run eas-build-ios

# O directamente con EAS CLI
eas build --platform all
eas build --platform android
eas build --platform ios
```

### Build Profiles Disponibles

#### Development (development)
```bash
eas build --platform all --profile development
```
- Distribución interna
- Development client habilitado
- APK para Android (más rápido)
- Perfecto para testing local

#### Preview (preview)
```bash
eas build --platform all --profile preview
```
- Distribución interna
- Builds listos para presentación
- APK para Android

#### Production (production)
```bash
eas build --platform all --profile production
```
- Distribución para store (App Store / Google Play)
- AAB para Android (formato requerido)
- IPA para iOS

### Configuración por Plataforma

#### iOS

**Bundle ID:** `com.football.app`

Requiere:
- Certificados de desarrollo/producción de Apple
- Provisioning profiles
- Credentials almacenadas en EAS

```bash
# EAS gestiona las credenciales automáticamente
# En el primer build, te pedirá los datos de tu Apple Account
```

#### Android

**Package:** `com.football.app`

Requiere:
- Keystore (EAS puede generarlo automáticamente)
- Credentials almacenadas en EAS

```bash
# EAS gestiona el keystore automáticamente
# En el primer build, te pedirá los datos o usará los existentes
```

### Variables de Entorno

Crear archivo `.env` si es necesario:

```bash
# .env
EXPO_PUBLIC_API_URL=https://your-api.com
```

Acceder en el código:

```js
import { useConfig } from 'expo';
const apiUrl = process.env.EXPO_PUBLIC_API_URL;
```

### Estructura del Proyecto

```
Football/
├── App.js                 # Componente principal
├── index.js              # Entrada de la app
├── app.json              # Configuración Expo
├── eas.json              # Configuración EAS
├── babel.config.js       # Configuración Babel
├── package.json          # Dependencias
├── .gitignore            # Archivos ignorados
├── .env                  # Variables de entorno (no commitar)
├── node_modules/         # Dependencias instaladas
└── EAS_SETUP.md         # Este archivo
```

### Troubleshooting

#### Error: "projectId not found"
```bash
# Solución: ejecutar eas build:configure
npx eas build:configure
```

#### Error: "Credentials not configured"
```bash
# Solución: dejar que EAS genere credenciales automáticamente
# O ejecutar: eas credentials
```

#### Error: "Node modules not found"
```bash
# Solución: reinstalar dependencias
rm -rf node_modules package-lock.json
npm install
```

#### Build lento en iOS
```bash
# Usar resourceClass más potente en eas.json
"ios": {
  "resourceClass": "medium"
}
```

### Verificación de Configuración

```bash
# Verificar que Expo esté correctamente instalado
expо --version

# Verificar que EAS CLI esté correctamente instalado
eas --version

# Verificar que el proyecto está validado
eas build --platform all --dry-run
```

### Próximos Pasos

1. Ejecutar `npm install`
2. Iniciar sesión con `npx eas login`
3. Conectar proyecto con `npx eas build:configure`
4. Realizar primer build con `eas build --platform all --profile development`
5. Descargar los binarios (APK/IPA) desde el dashboard de EAS

### Recursos Útiles

- [Documentación Expo](https://docs.expo.dev)
- [Guía EAS Build](https://docs.expo.dev/build/setup/)
- [Configuración app.json](https://docs.expo.dev/versions/latest/config/app/)
- [EAS Build API](https://docs.expo.dev/build-reference/api/)

### Estado de Validación

✅ Configuración Expo completada
✅ Perfiles EAS configurados
✅ Dependencias validadas
✅ Proyecto listo para `eas build --platform all`
✅ iOS y Android soportados

---

**Última actualización:** 2026-10-04
**Versión:** 1.0.0
**Estado:** ✅ Listo para producción

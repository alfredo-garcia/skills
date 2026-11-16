# Montar el knowledge base y sincronizarlo con Google Drive

Guía para una persona que empieza de cero. El knowledge base es una carpeta normal de archivos (Markdown, YAML, JSON). Claude trabaja sobre los archivos locales, y Google Drive mantiene una copia en la nube y en tus otros dispositivos.

## 1. Lo que necesitas

- La app de Claude (escritorio, con Cowork) o Claude Code.
- Una cuenta de Google con Google Drive.
- Opcional: un bot de Telegram propio, para recibir avisos y mandar cosas desde el móvil (sección 6).

## 2. Instalar el marketplace

- **Claude escritorio o Cowork**: Customize → Plugins → *Add marketplace* → `alfredo-garcia/skills`. Después instala `knowledge-base-suite` y, si los quieres, `health-advisor`, `finance-advisor` y `legal-advisor-es-co`.
- **Claude Code**: `/plugin marketplace add alfredo-garcia/skills` y luego `/plugin install knowledge-base-suite@skills` (y los demás).

Las skills no llevan datos de nadie. Todo lo tuyo se guarda en tu carpeta.

## 3. Crear la carpeta sincronizada

Elige la opción de tu sistema. Lo importante es que **los archivos estén de verdad en el disco**, no solo en la nube: Cowork y Claude Code leen y escriben archivos locales.

### A. Mac o Windows: Google Drive para escritorio (recomendada)

1. Instala [Google Drive para escritorio](https://www.google.com/drive/download/) e inicia sesión.
2. Abre Preferencias (⚙️) → **Google Drive** y elige **Duplicar archivos** (*Mirror files*). Así cada archivo existe en local y en la nube.
   - Si prefieres **Transmitir archivos** (*Stream files*), entonces, tras crear la carpeta (paso 3), haz clic derecho sobre ella → *Disponible sin conexión*. Si no lo haces, Claude ve archivos que aún no se han descargado.
3. Dentro de **Mi unidad**, crea una carpeta llamada `knowledge-base`. La encontrarás en:
   - Mac: `~/Library/CloudStorage/GoogleDrive-<tu-correo>/Mi unidad/knowledge-base`. Con «Duplicar», también puede estar en `~/Google Drive/Mi unidad/knowledge-base`.
   - Windows: `G:\Mi unidad\knowledge-base` (si transmites) o `C:\Users\<tú>\Mi unidad\knowledge-base` (si duplicas).
4. En Cowork, conecta esa carpeta como carpeta de trabajo.

La sincronización es automática y suele tardar unos segundos.

### B. Linux: rclone bisync con cron

Google no tiene cliente oficial para Linux, así que se usa `rclone`:

```bash
sudo apt install rclone
rclone config            # nuevo remoto "gdrive", tipo "drive", acceso completo
mkdir -p ~/knowledge-base   # o la carpeta que elijas
rclone mkdir gdrive:knowledge-base
rclone bisync ~/knowledge-base gdrive:knowledge-base --resync   # solo la primera vez
```

Script `~/bin/kb-sync.sh` (dale permisos con `chmod +x`):

```bash
#!/bin/bash
/usr/bin/rclone bisync "$HOME/knowledge-base" gdrive:knowledge-base \
  --create-empty-src-dirs --resilient --recover --max-lock 2m --conflict-resolve newer "$@"
```

Para que se ejecute cada 5 minutos, añade esta línea con `crontab -e`:

```
*/5 * * * * $HOME/bin/kb-sync.sh >> $HOME/.cache/rclone-kb.log 2>&1
```

**Client ID propio (recomendado)**: el client ID compartido de rclone para Google Drive deja de funcionar durante 2026. Crea el tuyo en Google Cloud Console (proyecto → habilitar Google Drive API → credenciales OAuth tipo «Aplicación de escritorio») y pégalo en `rclone config` (`client_id` y `client_secret` del remoto `gdrive`, y vuelve a autorizar). Guía oficial: https://rclone.org/drive/#making-your-own-client-id

En `_profile.yaml`, pon `sync.method: rclone-bisync` y `sync.command: ~/bin/kb-sync.sh`. Las skills lanzan la sincronización siempre con ese script, nunca con `rclone bisync` directamente. Si `bisync` se queda bloqueado tras un error, ejecuta una vez `~/bin/kb-sync.sh --resync`.

### Conflictos

Si el mismo archivo se edita en dos sitios antes de sincronizar, Drive o rclone guardan dos copias (`archivo (1).md`, `archivo.conflict1`…). Pídele a Claude «revisa conflictos de sincronización del knowledge base»: comparará las dos copias, conservará el contenido de ambas y borrará la copia sobrante cuando le confirmes. Las skills releen cada archivo antes de escribirlo (escritura optimista), así que estos conflictos son poco frecuentes.

## 4. Primer arranque

En una sesión con la carpeta conectada, escribe: **«monta mi knowledge base»**. (También vale empezar directamente con cualquier skill: si no encuentra un knowledge base, te pregunta qué carpeta usar, y si no tiene tu perfil, te avisa y lo crea contigo). La skill `personal-knowledge-base` te hará unas pocas preguntas (nombre, cómo quieres que te traten, zona horaria, ciudad y países, si quieres Telegram) y creará lo siguiente:

```
knowledge-base/
  _profile.yaml       tus datos básicos (solo aquí, nunca dentro de las skills)
  _domains.json       registro de grupos y dominios
  _inbox/             bandeja global
  _links/
```

No hace falta crear nada más a mano. **Cada skill monta su propio grupo la primera vez que la usas**:

| Primera vez que… | La skill crea |
| --- | --- |
| guardas una receta o dices «compré nata» | `food/` (recetas, ingredientes, despensa, valoraciones, plan de comidas) |
| guardas un plan o pides «¿qué hacemos el finde?» | `plans/`, y te pregunta qué ciudades buscar |
| cuentas un entrenamiento o pides una rutina | `fitness/`, y te pregunta tus objetivos y limitaciones |
| hablas de salud | `health/`, y construye tu ficha contigo |
| hablas de inversiones | `finance/` y tu perfil de inversor |
| haces una consulta legal o un trámite | `legal/` y tu perfil legal |

## 5. Tareas programadas (Cowork)

Las tareas solo se ejecutan con el ordenador encendido y la app de Claude abierta. Sugerencias:

- Cada 15–30 min: «Revisa el inbox global del knowledge base (y Telegram si está activo), enrútalo y procesa lo que llegue a cada dominio».
- Una vez por semana: «Haz la búsqueda semanal de planes y mándame el resumen».

## 6. Telegram (opcional)

1. En Telegram, habla con **@BotFather** → `/newbot` y guarda el token. Escríbele cualquier cosa a tu bot para abrir el chat.
2. Configura un servidor **Telegram MCP** que admita una cuenta de tipo bot (con el token) y dale a esa cuenta un nombre, por ejemplo `bot`. Las skills solo usan esa cuenta, nunca tu cuenta personal.
3. Averigua tu id de usuario de Telegram (por ejemplo, leyendo con la cuenta del bot el mensaje que le mandaste: el `sender_id` es tu id).
4. En `_profile.yaml`, rellena `telegram.enabled: true`, `mcp_account`, `bot_username`, `bot_id` y `chat_id` (tu id).

Sin Telegram todo funciona igual: los avisos y las confirmaciones se quedan en la sesión de Claude.

## 7. Varias personas

Cada persona tiene **su propio knowledge base**, con su `_profile.yaml`, su carpeta de Drive y su bot. Si alguna vez queréis compartir un grupo (por ejemplo, las recetas de casa), basta con compartir esa carpeta en Drive y listar al otro usuario en `household`. Los archivos por usuario (`reviews/<usuario>.yaml`, `program/<usuario>.yaml`…) evitan que os piséis los datos.

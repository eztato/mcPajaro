# mcPajaro - Minecraft Arclight 1.20.1 Template

Molde limpio para servidor Docker con Arclight (Forge por defecto), orientado a host de 12 GB de RAM total y listo para usar con ItemsAdder.

Este repo no incluye jars, zips ni datos del mundo para mantenerlo liviano y reusable.

## Incluye

- Arclight `1.20.1` (`ARCLIGHT_TYPE=FORGE` por defecto).
- Descarga automatica de dependencias base: ProtocolLib, PlaceholderAPI, LuckPerms, TAB, Chunky.
- Pregeneracion Chunky manual por etapas (mas estable para modded pesado).
- Backup diario con `mc-backup`.
- Estructura para mods, plugins y config externa.

## Estructura

- `docker-compose.yml`: stack principal.
- `docker-compose.local.yml`: perfil de pruebas con menos RAM.
- `.env.example`: variables recomendadas.
- `mods/`: coloca mods Forge aqui.
- `plugin/`: coloca jars de plugins aqui.
- `plugin/config/`: configs para copiar a `data/plugins` al arrancar.
- `plugin/packs-source/`: zips de packs fuente (opcional, no versionados).
- `data/`: datos del servidor.
- `backups/`: backups generados.

## Inicio rapido

```bash
cp .env.example .env
```

Edita `RCON_PASSWORD` en `.env` y levanta:

```bash
docker compose up -d
docker logs -f bugcraft-12gb
```

El flujo ahora incluye una etapa automatica previa (`mc-mods-sync`) que descarga mods de servidor en `mods/` antes de iniciar Minecraft.

Si tu `CF_API_KEY` contiene `$`, escapala en `.env` como `$$` para evitar interpolacion de Docker Compose.

## Requisitos previos

- Docker Engine instalado y activo.
- Docker Compose plugin (`docker compose`) disponible.
- Acceso a internet saliente para descargar mods (Modrinth/CurseForge/CDN).
- Puerto `25565` libre en el host.
- `.env` creado y con `RCON_PASSWORD` definido.
- `CF_API_KEY` definido si quieres usar API de CurseForge (si contiene `$`, escaparlo como `$$`).
- `ARCLIGHT_RELEASE=Trials/1.0.6` para fijar el release compatible de Arclight 1.20.1.
- `WHITELIST` configurada con nicks permitidos (recomendado para servidor publico).

## Flujo automatico de arranque

Cuando ejecutas `docker compose up -d`:

1. Arranca `mc-mods-sync` y sincroniza mods/dependencias en `mods/`.
2. Si la sincronizacion termina bien, inicia `bugcraft`.
3. Puedes revisar el resultado en `mods/.sync-report.json`.

## Comandos utiles

Levantar todo el stack (sync + server):

```bash
docker compose up -d
```

Sincronizar mods manualmente (sin iniciar Minecraft):

```bash
docker compose run --rm mc-mods-sync
```

Ver logs del sincronizador:

```bash
docker compose logs -f mc-mods-sync
```

Ver logs del server:

```bash
docker logs -f bugcraft-12gb
```

Ver estado de contenedores:

```bash
docker compose ps
```

Reiniciar solo Minecraft:

```bash
docker compose restart bugcraft
```

Ver reporte de sincronizacion de mods:

```bash
cat mods/.sync-report.json
```

Ejemplo de pregeneracion manual (estabilidad primero):

```bash
docker exec -it bugcraft-12gb rcon-cli "chunky world world"
docker exec -it bugcraft-12gb rcon-cli "chunky radius 4000"
docker exec -it bugcraft-12gb rcon-cli "chunky start"
```

## Troubleshooting rapido

- Si falta algun mod, corre `docker compose run --rm mc-mods-sync` y revisa `mods/.sync-report.json`.
- Si quieres que el arranque falle cuando falte un mod, usa `MODS_SYNC_STRICT=true` en `.env`.
- Estado actual conocido para `1.20.1 Forge`: `Infernal Expansion` puede quedar pendiente por falta de build compatible.
- Si ves `The "..." variable is not set`, revisa `CF_API_KEY` y escapa cada `$` como `$$` en `.env`.
- Si falla Arclight con `Failed to locate Arclight jar`, confirma `ARCLIGHT_RELEASE=Trials/1.0.6`.
- Si entra gente no deseada, revisa que `WHITELIST` tenga tus nicks y reinicia el stack.

## Perfil recomendado (host 12 GB RAM total)

- `MC_INIT_MEMORY=4G`
- `MC_MAX_MEMORY=9G`
- `MC_MAX_PLAYERS=12`
- `MC_MOTD=BugCraft`
- `ONLINE_MODE=FALSE`
- `ENFORCE_SECURE_PROFILE=FALSE`
- `WHITELIST=tuNick,amigo1,amigo2`
- `MAX_TICK_TIME=-1` (mientras pregeneras)
- `VIEW_DISTANCE=7`
- `SIMULATION_DISTANCE=5`

Con `ONLINE_MODE=FALSE` el servidor acepta jugadores sin cuenta premium. En este modo no hay autenticacion oficial de Mojang y cualquier usuario puede usar cualquier nickname.
Para reducir bots y accesos no autorizados, usa whitelist siempre.

## Perfil local liviano

```bash
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d
```

## Pregeneracion Chunky

- Overworld: `CHUNKY_RADIUS_OVERWORLD=40000`
- Nether: `CHUNKY_RADIUS_NETHER=24000`
- End: `CHUNKY_RADIUS_END=18000`

Comportamiento automatico:

- primer jugador entra: `chunky pause`
- ultimo jugador sale: `chunky continue`

Recomendado: correr pregen manual por etapas (4k -> 8k -> 12k...) y un mundo a la vez para evitar watchdog/crash.

## ItemsAdder y contenido

Este molde esta pensado para ItemsAdder-only.

Consulta `docs/PLUGINS_AND_MODS.md` para la lista sugerida de jars y notas de compatibilidad.

Para el ultimo estado de instalacion automatizada de mods de servidor revisa:

- `docs/MODS_SERVER_MANIFEST.md`
- `docs/mods-manifest.json`

En runtime el detalle queda en `mods/.sync-report.json`.

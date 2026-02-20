# Plugins y Mods (plantilla)

Este repositorio no sube binarios (`.jar/.zip`).

## Plugins recomendados (ItemsAdder-only)

Colocalos en `plugin/`:

- `ItemsAdder`
- `ModelEngine`
- `UltimateShop`
- `AxTrade` (si usas sus configs)
- `HappyHUD` (si usas sus configs)

Dependencias base se descargan con `SPIGET_RESOURCES` en el compose:

- ProtocolLib
- PlaceholderAPI
- LuckPerms
- TAB
- Chunky

## Configs

Coloca configuraciones en `plugin/config/`.

Al arrancar, `itzg/minecraft-server` copia ese contenido a `/data/plugins` por `COPY_CONFIG_DEST=/data/plugins`.

## Mods Forge (servidor)

Coloca tus mods en `mods/`.

No mezclar mods Forge y NeoForge en la misma carpeta. Si cambias `ARCLIGHT_TYPE=NEOFORGE`, usa un set de mods compatible.

Este proyecto esta fijado en `Minecraft 1.20.1` con `ARCLIGHT_TYPE=FORGE`.

### Lista de mods instalada automaticamente

- Estado detallado: `docs/MODS_SERVER_MANIFEST.md`
- Formato maquina: `docs/mods-manifest.json`

Al ejecutar `docker compose up`, el servicio `mc-mods-sync` descarga mods y dependencias a `mods/` antes de iniciar `bugcraft`.

Variables utiles en `.env`:

- `CF_API_KEY`: token para API de CurseForge (opcional, con fallback automatico).
- `MODS_SYNC_STRICT`: si `true`, falla el arranque si falta algun mod.
- `WHITELIST`: lista de nicks permitidos para bloquear bots/accesos no deseados.

Incluye solo mods de lado `Ambos` (server), mas dependencias requeridas detectadas.

### Mods cliente (no instalar en servidor)

No colocar mods marcados como "Solo Cliente" dentro de `mods/` del servidor.

## Nota de licencias

No subas jars o zips premium al repo.

Guarda solo configuraciones, listas de dependencias y documentacion.

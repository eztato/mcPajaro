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

## Mods Forge

Coloca tus mods en `mods/`.

No mezclar mods Forge y NeoForge en la misma carpeta. Si cambias `ARCLIGHT_TYPE=NEOFORGE`, usa un set de mods compatible.

## Nota de licencias

No subas jars o zips premium al repo.

Guarda solo configuraciones, listas de dependencias y documentacion.

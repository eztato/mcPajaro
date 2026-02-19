# mcPajaro - Minecraft Arclight 1.20.1 Template

Molde limpio para servidor Docker con Arclight (Forge por defecto), orientado a 10+ jugadores y listo para usar con ItemsAdder.

Este repo no incluye jars, zips ni datos del mundo para mantenerlo liviano y reusable.

## Incluye

- Arclight `1.20.1` (`ARCLIGHT_TYPE=FORGE` por defecto).
- Descarga automatica de dependencias base: ProtocolLib, PlaceholderAPI, LuckPerms, TAB, Chunky.
- Pregeneracion Chunky agresiva y automatica (`40k / 24k / 18k`).
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
docker logs -f mc-evolution-16gb
```

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

## ItemsAdder y contenido

Este molde esta pensado para ItemsAdder-only.

Consulta `docs/PLUGINS_AND_MODS.md` para la lista sugerida de jars y notas de compatibilidad.

#!/usr/bin/env python3

import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone


MC_VERSION = os.getenv("MC_VERSION", "1.20.1")
MOD_LOADER = os.getenv("MOD_LOADER", "forge").lower()
CF_API_KEY = os.getenv("CF_API_KEY", "").strip()
MODS_DIR = os.getenv("MODS_DIR", "/mods")
STRICT_MODE = os.getenv("MODS_SYNC_STRICT", "false").lower() in {"1", "true", "yes"}


SEED_MODS = [
    {"name": "Alex's Caves", "modrinth": "alexs-caves", "curse": "alexs-caves"},
    {"name": "Tectonic", "modrinth": "tectonic", "curse": "tectonic"},
    {"name": "Terralith", "modrinth": "terralith", "curse": "terralith"},
    {"name": "Citadel", "modrinth": "citadel", "curse": "citadel"},
    {"name": "Chunky", "modrinth": "chunky", "curse": "chunky-pregenerator"},
    {"name": "FerriteCore", "modrinth": "ferrite-core", "curse": "ferritecore"},
    {"name": "Serene Seasons", "modrinth": "serene-seasons", "curse": "serene-seasons"},
    {"name": "Nature's Compass", "modrinth": "natures-compass", "curse": "natures-compass"},
    {"name": "Structure Compass", "modrinth": "structure-compass", "curse": "structure-compass"},
    {"name": "Mekanism", "modrinth": "mekanism", "curse": "mekanism"},
    {"name": "Industrial Foregoing", "modrinth": "industrial-foregoing", "curse": "industrial-foregoing"},
    {"name": "Sophisticated Backpacks", "modrinth": "sophisticated-backpacks", "curse": "sophisticated-backpacks"},
    {"name": "Artifacts", "modrinth": "artifacts", "curse": "artifacts"},
    {"name": "SecurityCraft", "modrinth": "security-craft", "curse": "securitycraft"},
    {"name": "L_Ender's Cataclysm", "modrinth": "l_enders-cataclysm", "curse": "l-enders-cataclysm"},
    {"name": "Aquamirae", "modrinth": "aquamirae", "curse": "ob-aquamirae"},
    {"name": "JEI", "modrinth": "jei", "curse": "jei"},
    {"name": "The Hordes", "modrinth": "the-hordes", "curse": "the-hordes"},
    {"name": "Zombie Awareness", "modrinth": "zombie-awareness", "curse": "zombie-awareness"},
    {"name": "Better Zombie AI", "modrinth": None, "curse": "better-zombie-ai"},
    {"name": "Born in Chaos", "modrinth": "borninchaos", "curse": "born-in-chaos"},
    {"name": "Extra Golems", "modrinth": None, "curse": "extra-golems"},
    {"name": "Draconic Evolution", "modrinth": "draconic-evolution", "curse": "draconic-evolution"},
    {"name": "FallingTree", "modrinth": "fallingtree", "curse": "falling-tree"},
    {"name": "Mekanism Tools", "modrinth": "mekanism-tools", "curse": "mekanism-tools"},
    {"name": "Harvest with Ease", "modrinth": "harvest-with-ease", "curse": "harvest-with-ease"},
    {"name": "Jade", "modrinth": "jade", "curse": "jade"},
    {"name": "Cupboard", "modrinth": None, "curse": "cupboard"},
    {"name": "Corail Tombstone", "modrinth": None, "curse": "corail-tombstone"},
    {"name": "BetterNether", "modrinth": "betternether-forge", "curse": "betternether"},
    {"name": "Infernal Expansion", "modrinth": None, "curse": "infernal-expansion"},
    {"name": "Biomes O' Plenty", "modrinth": "biomes-o-plenty", "curse": "biomes-o-plenty"},
    {"name": "ChoiceTheorem's Overhauled Village", "modrinth": "ct-overhaul-village", "curse": "choicetheorems-overhauled-village"},
    {"name": "YUNG's Better Dungeons", "modrinth": "yungs-better-dungeons", "curse": "yungs-better-dungeons"},
    {"name": "YUNG's Better Mineshafts", "modrinth": "yungs-better-mineshafts", "curse": "yungs-better-mineshafts"},
    {"name": "Waystones", "modrinth": "waystones", "curse": "waystones"},
    {"name": "Enlightend", "modrinth": "enlightend", "curse": "enlightend"},
    {"name": "TerraBlender", "modrinth": "terrablender", "curse": "terrablender"},
    {"name": "Ice and Fire: Dragons", "modrinth": "ice-and-fire-dragons", "curse": "ice-and-fire-dragons"},
    {"name": "Titanium", "modrinth": "titanium", "curse": "titanium"},
    {"name": "Sophisticated Core", "modrinth": "sophisticated-core", "curse": "sophisticated-core"},
    {"name": "Curios API", "modrinth": "curios", "curse": "curios"},
    {"name": "Brandon's Core", "modrinth": "brandons-core", "curse": "brandons-core"},
    {"name": "CodeChicken Lib", "modrinth": "codechicken-lib", "curse": "codechicken-lib-1-8"},
    {"name": "BCLib", "modrinth": "bclib-forge", "curse": "bclib"},
    {"name": "YUNG's API", "modrinth": "yungs-api", "curse": "yungs-api"},
    {"name": "Balm", "modrinth": "balm", "curse": "balm"},
]


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def log(msg):
    print(msg, flush=True)


def req_json(url, headers=None, params=None):
    full_url = url
    if params:
        full_url = f"{url}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(full_url, headers=headers or {})
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def download_file(url, target_path):
    request = urllib.request.Request(url, headers={"User-Agent": "mcPajaro-mod-sync/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        data = response.read()
    with open(target_path, "wb") as f:
        f.write(data)


def safe_filename(name):
    return re.sub(r"[^A-Za-z0-9._-]", "_", name)


def normalize_key(name):
    base = name.lower()
    base = re.sub(r"[^a-z0-9]+", "", base)
    return base


def ensure_mods_dir(path):
    os.makedirs(path, exist_ok=True)


def clear_existing_jars(path):
    for entry in os.listdir(path):
        if entry.lower().endswith(".jar"):
            os.remove(os.path.join(path, entry))


def modrinth_versions(slug):
    return req_json(
        f"https://api.modrinth.com/v2/project/{slug}/version",
        headers={"User-Agent": "mcPajaro-mod-sync/1.0"},
        params={
            "loaders": json.dumps([MOD_LOADER]),
            "game_versions": json.dumps([MC_VERSION]),
        },
    )


def modrinth_project(project_id_or_slug):
    return req_json(
        f"https://api.modrinth.com/v2/project/{project_id_or_slug}",
        headers={"User-Agent": "mcPajaro-mod-sync/1.0"},
    )


def pick_modrinth_file(version):
    files = version.get("files", [])
    if not files:
        return None
    for f in files:
        if f.get("primary"):
            return f
    return files[0]


def cf_api_search(slug):
    if not CF_API_KEY:
        return None
    return req_json(
        "https://api.curseforge.com/v1/mods/search",
        headers={"x-api-key": CF_API_KEY, "Accept": "application/json"},
        params={"gameId": 432, "slug": slug, "pageSize": 1},
    )


def cf_api_files(mod_id):
    if not CF_API_KEY:
        return None
    return req_json(
        f"https://api.curseforge.com/v1/mods/{mod_id}/files",
        headers={"x-api-key": CF_API_KEY, "Accept": "application/json"},
        params={"pageSize": 50},
    )


def pick_cf_file(files):
    candidates = []
    for f in files:
        versions = [str(v) for v in f.get("gameVersions", [])]
        lower_versions = {v.lower() for v in versions}
        if MC_VERSION not in versions:
            continue
        if "forge" not in lower_versions:
            continue
        score = 2 if "neoforge" not in lower_versions else 1
        candidates.append((score, f.get("fileDate", ""), f))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][2]


def cfwidget_project(slug):
    return req_json(
        f"https://api.cfwidget.com/minecraft/mc-mods/{slug}",
        headers={"User-Agent": "mcPajaro-mod-sync/1.0"},
    )


def pick_cfwidget_file(files):
    candidates = []
    for f in files:
        versions = [str(v) for v in f.get("versions", [])]
        lower_versions = {v.lower() for v in versions}
        if MC_VERSION not in versions:
            continue
        if "forge" not in lower_versions:
            continue
        server_bonus = 1 if "server" in lower_versions else 0
        candidates.append((server_bonus, f.get("uploaded_at", ""), f))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][2]


def cfwidget_download_url(file_id, filename):
    part_a = file_id // 1000
    part_b = file_id % 1000
    return f"https://mediafilez.forgecdn.net/files/{part_a}/{part_b}/{filename}"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def dedupe_jars(path):
    by_hash = {}
    removed = []
    for entry in sorted(os.listdir(path)):
        if not entry.lower().endswith(".jar"):
            continue
        full = os.path.join(path, entry)
        digest = sha256_file(full)
        if digest in by_hash:
            os.remove(full)
            removed.append(entry)
        else:
            by_hash[digest] = entry
    return removed


def main():
    ensure_mods_dir(MODS_DIR)
    clear_existing_jars(MODS_DIR)

    installed = {}
    pending = []
    queue = list(SEED_MODS)
    seen = set()

    while queue:
        item = queue.pop(0)
        name = item.get("name") or item.get("modrinth") or item.get("curse")
        key = normalize_key(name)
        if key in installed:
            continue

        identity = (item.get("name"), item.get("modrinth"), item.get("curse"))
        if identity in seen:
            continue
        seen.add(identity)

        installed_item = None

        modrinth_slug = item.get("modrinth")
        if modrinth_slug:
            try:
                versions = modrinth_versions(modrinth_slug)
                if versions:
                    version = versions[0]
                    f = pick_modrinth_file(version)
                    if f:
                        filename = safe_filename(f.get("filename", f"{modrinth_slug}.jar"))
                        target = os.path.join(MODS_DIR, filename)
                        download_file(f["url"], target)
                        installed_item = {
                            "name": name,
                            "source": "modrinth",
                            "slug": modrinth_slug,
                            "file": filename,
                            "version": version.get("version_number"),
                        }

                        for dep in version.get("dependencies", []):
                            if dep.get("dependency_type") != "required":
                                continue
                            project_id = dep.get("project_id")
                            if not project_id:
                                continue
                            try:
                                project_meta = modrinth_project(project_id)
                            except Exception:
                                continue
                            dep_slug = project_meta.get("slug")
                            dep_name = project_meta.get("title") or dep_slug
                            if dep_slug:
                                queue.append({"name": dep_name, "modrinth": dep_slug, "curse": None})
            except Exception:
                pass

        if not installed_item and item.get("curse"):
            curse_slug = item["curse"]
            try:
                api_search = cf_api_search(curse_slug)
                api_mods = (api_search or {}).get("data", [])
                if api_mods:
                    mod_id = api_mods[0].get("id")
                    if mod_id:
                        api_files = cf_api_files(mod_id)
                        cf_file = pick_cf_file((api_files or {}).get("data", []))
                        if cf_file:
                            download_url = cf_file.get("downloadUrl")
                            if not download_url:
                                download_url = cfwidget_download_url(int(cf_file["id"]), cf_file["fileName"])
                            filename = safe_filename(cf_file.get("fileName", f"{curse_slug}.jar"))
                            target = os.path.join(MODS_DIR, filename)
                            download_file(download_url, target)
                            installed_item = {
                                "name": name,
                                "source": "curseforge-api",
                                "slug": curse_slug,
                                "file": filename,
                                "version": cf_file.get("displayName"),
                            }
            except Exception:
                pass

            if not installed_item:
                try:
                    cfw = cfwidget_project(curse_slug)
                    cfw_file = pick_cfwidget_file(cfw.get("files", []))
                    if cfw_file:
                        file_id = int(cfw_file["id"])
                        filename = safe_filename(cfw_file["name"])
                        target = os.path.join(MODS_DIR, filename)
                        download_url = cfwidget_download_url(file_id, cfw_file["name"])
                        download_file(download_url, target)
                        installed_item = {
                            "name": name,
                            "source": "cfwidget",
                            "slug": curse_slug,
                            "file": filename,
                            "version": cfw_file.get("display"),
                        }
                except Exception:
                    pass

        if installed_item:
            installed[key] = installed_item
            log(f"[ok] {name} -> {installed_item['file']} ({installed_item['source']})")
        else:
            pending.append({"name": name, "modrinth": item.get("modrinth"), "curse": item.get("curse")})
            log(f"[pending] {name}")

    removed_dupes = dedupe_jars(MODS_DIR)

    report = {
        "generated_at": now_iso(),
        "mc_version": MC_VERSION,
        "mod_loader": MOD_LOADER,
        "strict_mode": STRICT_MODE,
        "installed_count": len(installed),
        "pending_count": len(pending),
        "installed": sorted(installed.values(), key=lambda x: x["name"].lower()),
        "pending": sorted(pending, key=lambda x: x["name"].lower()),
        "dedup_removed": removed_dupes,
    }

    report_path = os.path.join(MODS_DIR, ".sync-report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    log(f"\nSync completado: {report['installed_count']} instalados, {report['pending_count']} pendientes")
    if pending and STRICT_MODE:
        log("Modo estricto activado: hay mods pendientes.")
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except urllib.error.HTTPError as exc:
        log(f"HTTP error: {exc.code} {exc.reason}")
        sys.exit(1)
    except Exception as exc:
        log(f"Error: {exc}")
        sys.exit(1)

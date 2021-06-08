import os
import sys
import pkg_resources
import subprocess
import signal


def current_platform() -> str:
    import platform
    os = platform.system().lower()
    machine = platform.machine().lower()

    # Consistent naming
    if machine == 'x86_64':
        machine = 'amd64'
    if os == 'darwin':
        os = 'mac'

    return "{}_{}".format(os, machine)

SUPPORTED_TYPES = ('application/zip', 'application/gzip')
TARGET_LICENSE  = 'caddy.LICENSE'
TARGET_BINARY   = 'caddy.target.exe'
RELEASES_JSON   = 'https://api.github.com/repos/caddyserver/caddy/releases?per_page=3'

def latest_version(platform) -> (str, str, str):
    import requests
    releases_json: list = requests.get(RELEASES_JSON).json()

    if len(releases_json) == 0:
        raise ValueError('Cannot fetch GitHub Releases, got len(body) == 0.')

    rel: dict = releases_json[0]
    release_name: str = rel['name']

    asset = [x for x in rel['assets'] \
             if platform in x['name'] and x['content_type'] in SUPPORTED_TYPES]

    if len(asset) == 0:
        raise ValueError('Cannot find matching artefact with {} and type {}'.format(platform, SUPPORTED_TYPES))

    asset = asset[0]
    asset_url:  str = asset['browser_download_url']
    asset_type: str = asset['content_type']

    return release_name, asset_url, asset_type


def main():
    target_path = pkg_resources.resource_filename('sponggy', TARGET_BINARY)

    update = False
    if len(sys.argv) == 2 and sys.argv[1] in ('update', 'upgrade', 'install'):
        update = True
    if update or os.path.getsize(target_path) == 0:
        from .download_release import download
        platform = current_platform()
        version, url, content_type = latest_version(platform)
        print('Downloading {} from {}'.format(version, url))
        download(url, target_path, content_type)
        sys.stdout.write('[!] Installed {}.'.format(version, ))
        if len(sys.argv) > 1 and not update:
            sys.stdout.write(' Calling `sponggy {}`\n\n'.format(' '.join(sys.argv[1:])))
            sys.stdout.flush()
        else:
            sys.stdout.write(' To start the server, use `sponggy run`\n')
            sys.exit(0)

    p = subprocess.Popen([target_path, *sys.argv[1:]], stdin=sys.stdin, stderr=sys.stderr, stdout=sys.stdout)
    def handle(sig, frame):
        try:
            p.send_signal(sig)
        except: pass
    signal.signal(signal.SIGINT, handle)
    sys.exit(p.wait())

if __name__ == '__main__':
    main()

import requests
import tqdm
import zipfile
import tarfile
import io
import os
import pkg_resources

def download(url, target_file, content_type='application/zip', show_progress=True):
    zip_raw = io.BytesIO()
    req = requests.get(url, stream=True)
    progress_options = dict(
        bar_format='{percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}, {rate_fmt}{postfix}]',
        unit="B",
        total=int(req.headers['Content-Length']),
        unit_scale=True,
        unit_divisor=1024,
        disable=not show_progress
    )

    with tqdm.tqdm(**progress_options) as pbar:
        for chunk in req.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                pbar.update(len(chunk))
                zip_raw.write(chunk)

    zip_raw.seek(0, 0)

    if content_type == 'application/gzip':
        tf = tarfile.open(fileobj=zip_raw, mode='r:gz')
        exec_candidates = [x for x in tf.getnames() if 'caddy' in x]
        method = 'gzip'
        write_caddy_license(tf, method)
    elif content_type == 'application/zip':
        zf = zipfile.ZipFile(zip_raw)
        exec_candidates = [x for x in zf.namelist() if 'caddy' in x]
        method ='zip'
        write_caddy_license(zf, method)
    else:
        raise ValueError('Unknown archive format')
    if len(exec_candidates) != 1:
        raise ValueError("Cannot find a caddy executable")
    exec_name = exec_candidates[0]

    if method == 'zip':
        exec_data = zf.open(exec_name, mode='r')
    elif method == 'gzip':
        exec_data = tf.extractfile(exec_name)

    with open(target_file, "wb") as disk_file:
        disk_file.write(exec_data.read())
        if hasattr(os, 'fchmod'):
            mode = os.fstat(disk_file.fileno()).st_mode
            mode |= 0o111
            os.fchmod(disk_file.fileno(), mode & 0o7777)

def write_caddy_license(archive, method):
    try:
        if method == 'zip':
            license = archive.open('LICENSE', mode='r').read()
        elif method == 'gzip':
            license = archive.extractfile('LICENSE').read()
    except:
        return False
    target_path = pkg_resources.resource_filename('sponggy', 'caddy.LICENSE')
    with open(target_path, 'wb') as f:
        f.write(license)
    return True
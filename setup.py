def main():
    import pkg_resources
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
                                      for i in installed_packages])
    if not any("requests" in s for s in installed_packages_list):
        install_and_import('requests')
    if not any("tqdm" in s for s in installed_packages_list):
        install_and_import('tqdm')
    if not any("beautifulsoup4" in s for s in installed_packages_list):
        install_and_import('beautifulsoup4')

    import requests
    import os
    import zipfile
    from tqdm import tqdm

    url1 = "https://library.ldraw.org/library/updates/complete.zip"
    url2 = "https://github.com/TobyLobster/ImportLDraw/releases/download/v1.2.0/importldraw1.2.0.zip"

    print("Downloading complete.zip...")
    r = requests.get(url1, allow_redirects=True)
    open('complete.zip', 'wb').write(r.content)

    print("Downloading importldraw.zip...")
    r = requests.get(url2, allow_redirects=True)
    open('importldraw.zip', 'wb').write(r.content)

    print("Unzipping complete.zip...")
    complete_zip_path = os.path.abspath("complete.zip")
    with zipfile.ZipFile(complete_zip_path, 'r') as zip_ref:
        for member in tqdm(zip_ref.infolist(), desc='Extracting '):
            try:
                zip_ref.extract(member, os.path.abspath("complete"))
            except zipfile.error as e:
                pass


def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


if __name__ == "__main__":
    main()

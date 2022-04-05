import uproot

def file_tester(file_path):
    try:
        uproot.open(file_path).close()
    except Exception:
        print(f'An exception occurred trying to open: {file_path}')

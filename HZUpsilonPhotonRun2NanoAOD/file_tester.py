import uproot

def file_tester(file_path):
    print(f'Testing "uproot.open" file: {file_path}')
    try:
        uproot.open(file_path)
    except:
        print(f'An exception occurred trying to open: {file_path}')

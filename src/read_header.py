from pathlib import Path
data_folder = Path(__file__).parent.parent / "data"
hdr_file = data_folder / "megt90n000fb.hdr"

with open(hdr_file,"r") as file:
    header = file.read()

print(header)
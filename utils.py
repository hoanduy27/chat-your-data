import os 
import io
import tempfile 
def make_temp_file(fs, name):
    temp_dir = tempfile.TemporaryDirectory()

    temp_file = os.path.join(temp_dir.name, name)

    return temp_dir, temp_file 
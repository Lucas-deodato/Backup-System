import gzip
import multiprocessing
from pathlib import Path

def compress_file(input_path, output_path, queue):
    input_file = Path(input_path)
    output_file = Path(output_path)
    """Simple gzip compression."""
    with open(input_file, "rb") as f_in:
        with gzip.open(output_file, "wb") as f_out:
            f_out.writelines(f_in)
            
    input_file.unlink()
    queue.put(output_file)


def process_file(file_path):
    """Performs compression in parallel."""
    queue = multiprocessing.Queue()
    output_file = str(file_path) + ".gz"
    p = multiprocessing.Process(target=compress_file, args=(file_path, output_file, queue))
    p.start()
    result = queue.get()
    p.join()
    return result
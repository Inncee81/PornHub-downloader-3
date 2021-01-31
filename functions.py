from tqdm import tqdm
import requests


def get_num_ending(num, cases):
    """Склоняет существительное,в зависимости от числительного,
    стоящего перед ним.
    """
    num = num % 100
    if 11 <= num <= 19:
        return cases[2]
    else:
        i = num % 10
        if i == 1:
            return cases[0]
        elif 2 <= i <= 4:
            return cases[1]
        else:
            return cases[2]


def download(url, filename):
    # Streaming, so we can iterate over the response.
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        return False
    else:
        return True

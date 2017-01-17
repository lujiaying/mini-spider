import os

def load(seedfile_path, seed_urls):
    """
    Args:
        seedfile_path: string
        seed_urls: list of string
    Returns:
        success_flag: 0 success, others fail
    """
    if not os.path.exists(seedfile_path):
        return -1

    with open(seedfile_path) as fopen:
        for line in fopen:
            url = line.strip()
            seed_urls.append(url)

    return 0

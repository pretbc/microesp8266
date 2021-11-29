from yaml import load, Loader
from controller.settings import gen_bin_yml


def get_config(setup_name: str = None, file_path=gen_bin_yml):
    if setup_name:
        return {**load_config_file(file_path)[setup_name]}
    to_load = ['boot_versions', 'bins', 'spi_speeds', 'spi_modes', 'spi_sizes']
    return {k: v for k, v in load_config_file(file_path).items() if k in to_load}


def load_config_file(local_file):
    with open(local_file, 'r') as f:
        return load(f, Loader=Loader)

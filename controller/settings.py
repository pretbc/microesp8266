import os

# ENVI
sdk_root = os.environ.get('NON_OS_SDK_PATH')

# SDK PATHS
sdk_bin = os.path.join(sdk_root, 'bin')
sdk_upgrade = os.path.join(sdk_bin, 'upgrade')

# PYTHON FILE PATHS
gen_bin_yml = os.path.join('controller', 'config', 'genbin.yml')

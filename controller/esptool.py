import os
import shutil
import subprocess as sp

from controller.errors import EspToolError
from controller.settings import sdk_root, sdk_bin, sdk_upgrade
from controller.logger import MyLogger

logger = MyLogger(__name__, level='INFO')


class EspTool:

    def __init__(self, working_dir: str = sdk_root):
        self.working_dir = working_dir

    def run(self):
        os.chdir(self.working_dir)
        logger.info(f'Set working dir: {self.working_dir}')
        cmd = [
            f'esptool.py',
            f'write_flash',
            f'--flash_size',
            f'4MB', f'0x0',
            f'{sdk_bin}/boot_v1.7.bin', f'0x01000',
            f'{sdk_upgrade}/user1.4096.new.6', f'0x3fc000',
            f'{sdk_bin}/blank.bin', f'0xfc000',
            f'{sdk_bin}/esp_init_data_default_v08.bin', f'0x3fe00',
            f'blank.bin', f'0x3fb000',
            f'{sdk_bin}/blank.bin'

        ]
        logger.info('Run esptool process:')
        logger.info(f'Start to execute cmd: ' + ' '.join(cmd))
        proc = sp.Popen(cmd, stderr=sp.PIPE, stdout=sp.PIPE)
        out, err = proc.communicate()
        if err:
            raise EspToolError(f'Error while exe cmd: ' + ' '.join(cmd) + f'\nError msg: {err}')
        logger.info(out)

import os
import shutil
import subprocess as sp

from controller.errors import CompilerPreProcessError, CompilerCommandExecuteError
from controller.genbin import Configuration
from controller.settings import sdk_root, sdk_upgrade, sdk_user
from controller.logger import MyLogger

logger = MyLogger(__name__, level='INFO')


class Compiler:
    def __init__(self, working_dir: str = sdk_root):
        self.working_dir = working_dir
        self.configured = Configuration()

    @staticmethod
    def _purge_upgrade_dir():
        logger.info(f'Start to purge files in: {sdk_upgrade}')
        for filename in os.listdir(sdk_upgrade):
            file_path = os.path.join(sdk_upgrade, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def _process(self):
        os.chdir(self.working_dir)
        logger.info(f'Set working dir: {self.working_dir}')
        cmd_touch = [
            f'touch',
            f'{sdk_user}/user_main.c'
        ]
        cmd_make = [
            f'make',
            f'COMPILE=gcc',
            f'BOOT={self.configured.boot.value}',
            f'APP={self.configured.app.value}'
            f'SPI_SPEED={self.configured.speed.value}'
            f'SPI_MODE={self.configured.mode.value}'
            f'SPI_SIZE_MAP={self.configured.size.value}'
        ]
        logger.info('Run compiler process:')
        for cmd in [cmd_touch, cmd_make]:
            logger.info(f'Start to execute cmd: ' + ' '.join(cmd))
            proc = sp.Popen(cmd, stderr=sp.PIPE, stdout=sp.PIPE)
            out, err = proc.communicate()
            if err:
                raise CompilerCommandExecuteError(f'Error while exe cmd: ' + ' '.join(cmd) + f'\nError msg: {err}')
            logger.info(out)

    def _pre_preprocess(self):
        boot = self.configured.boot
        app = self.configured.app
        logger.debug(f'boot value/name: {boot.value} | {boot.name}')
        logger.debug(f'app value/name: {app.value} | {app.name}')
        if boot.value == 'none' and app.value != 0:
            raise CompilerPreProcessError(
                f'Boot mode: {boot.name}, cannot be compiled with app equal: {app.name}')

    def run(self, boot_input: int = None, bin_input: int = None, speed_input: int = None, mode_input: int = None,
            size_input: int = None, load_config: str = None):
        self._purge_upgrade_dir()
        if load_config:
            logger.info(f'Loading custom config: {load_config}')
            self.configured.load_custom_config(load_config)
        if load_config is None:
            logger.info(f'Parsing given data config')
            self.configured.parse_args(boot_input, bin_input, speed_input, mode_input, size_input)
        self._pre_preprocess()
        self._process()

import abc

from dataclasses import dataclass, field
from typing import List, Dict, Any

from controller.errors import GenBinOptionError
from controller.config.load_genbin_config import get_config
from controller.logger import MyLogger

logger = MyLogger(__name__, level='INFO')


@dataclass
class GenBin(abc.ABC):
    set_value: int = None
    _default: int = 0
    _value: Dict = field(init=False)

    def __post_init__(self):
        self._config: Dict = get_config()
        options = self._options()
        logger.debug(f'Possible options: {options}')
        if self.set_value is None:
            self.set_value = self._default
        try:
            option = options[self.set_value]
        except IndexError:
            GenBinOptionError(f'Given option: {self.set_value} not found. '
                              f'Possible options:\n' + '\n'.join([f'{i}={k}' for i, k in enumerate(options)]))
        else:
            logger.debug(f'Parsed option: {option}')
            self._value = [v for v in option.values()][0]

    @abc.abstractmethod
    def _options(self) -> List:
        pass

    @property
    def get_value(self):
        return self._value

    @property
    def return_config(self):
        return self._config


@dataclass
class BootVersion(GenBin):
    _default: int = 2

    def _options(self) -> List:
        return self._config['boot_versions']


@dataclass
class Bin(GenBin):

    def _options(self) -> List:
        return self._config['bins']


@dataclass
class SpiSpeed(GenBin):
    _default: int = 2

    def _options(self) -> List:
        return self._config['spi_speeds']


@dataclass
class SpiMode(GenBin):

    def _options(self) -> List:
        return self._config['spi_modes']


@dataclass
class SpiSize(GenBin):

    def _options(self) -> List:
        return self._config['spi_sizes']


@dataclass
class Params:
    param_dict: Dict
    name: Any = field(init=False)
    value: Any = field(init=False)

    def __post_init__(self):
        self.name = self.param_dict['name']
        self.value = self.param_dict['value']


@dataclass
class Configuration:
    boot: Params = None
    app: Params = None
    speed: Params = None
    mode: Params = None
    size: Params = None

    def load_custom_config(self, config_name):
        custom = get_config(config_name)
        self.boot = Params(custom['boot'])
        self.app = Params(custom['app'])
        self.speed = Params(custom['speed'])
        self.mode = Params(custom['mode'])
        self.size = Params(custom['size'])

    def parse_args(self, boot_input: int = None, bin_input: int = None, speed_input: int = None,
                   mode_input: int = None, size_input: int = None):
        self.boot = Params(BootVersion(boot_input).get_value)
        self.app = Params(Bin(bin_input).get_value)
        self.speed = Params(SpiSpeed(speed_input).get_value)
        self.mode = Params(SpiMode(mode_input).get_value)
        self.size = Params(SpiSize(size_input).get_value)



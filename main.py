import argparse

from controller.compiler import Compiler
from controller.esptool import EspTool
from controller.logger import MyLogger

logger = MyLogger(__name__, level='INFO')

my_parser = argparse.ArgumentParser()
my_parser.add_argument('--boot', type=int, default=2,
                       help='choose boot version(0=boot_v1.1, 1=boot_v1.2+, 2=none)')
my_parser.add_argument('--bin', type=int, default=0,
                       help='choose bin generate(0=eagle.flash.bin+eagle.irom0text.bin, 1=user1.bin, 2=user2.bin)')
my_parser.add_argument('--speed, -b', type=int, default=2,
                       help='choose spi speed(0=20MHz, 1=26.7MHz, 2=40MHz, 3=80MHz)')
my_parser.add_argument('--mode, -b', type=int, default=0,
                       help='choose spi mode(0=QIO, 1=QOUT, 2=DIO, 3=DOUT)')
my_parser.add_argument('--size, -b', type=int, default=0, help="choose spi size and map:\n"
                                                               "0= 51KB( 256KB+ 256KB)\n"
                                                               "1=1024KB( 512KB+ 512KB)\n"
                                                               "2=2048KB( 512KB+ 512KB)\n"
                                                               "3=4096KB( 512KB+ 512KB)\n"
                                                               "4=2048KB(1024KB+1024KB)\n"
                                                               "5=4096KB(1024KB+1024KB)\n"
                                                               "6=4096KB(2048KB+2048KB) not support ,"
                                                               "just for compatible with nodeMCU board\n"
                                                               "7=8192KB(1024KB+1024KB)\n"
                                                               "8=16384KB(1024KB+1024KB)\n")
my_parser.add_argument('--custom_config, -b', type=str, default=None, help='custom configuration name')

if __name__ == '__main__':
    args = my_parser.parse_args()
    logger.info('Start compiler')
    cpr = Compiler()
    cpr.run(
        boot_input=args.boot,
        bin_input=args.bin,
        speed_input=args.speed,
        mode_input=args.mode,
        size_input=args.size,
        load_config=args.custom_config
    )
    logger.info('Start python esptool')
    esp = EspTool()
    esp.run()
    logger.info('All done. See you next time !!!')

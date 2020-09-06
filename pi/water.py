import logging
from datetime import datetime
from time import sleep

import click
from rpi_rf import RFDevice

LOGGER = logging.getLogger(__name__)

@click.command()
@click.argument('on_code', type=int, nargs=1)
@click.argument('off_code', type=int, nargs=1)
@click.option('--pin', '-p', type=int, default=21)
@click.option('--repeat', '-r', type=int, default=10)
@click.option('--time', '-o', type=float, default=10)
def main(on_code: int, off_code: int, pin: int, repeat: int, time: float):
    rf_device = RFDevice(pin)
    rf_device.enable_tx()
    rf_device.tx_repeat = repeat
    LOGGER.info(f'RF device ready')

    LOGGER.info(f'Transmitting code: {on_code}')
    rf_device.tx_code(on_code, 1, 100, 24)

    start = datetime.now()
    while (elapsed := (datetime.now() - start).total_seconds()) <= time:
        print(f'\rWaiting...{elapsed:.1f} s', '')
        sleep(.1)

    LOGGER.info(f'Transmitting code: {off_code}')
    rf_device.tx_code(off_code, 1, 100, 24)

    rf_device.cleanup()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)
    main()


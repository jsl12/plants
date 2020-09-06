import logging

import click
from rpi_rf import RFDevice

LOGGER = logging.getLogger(__name__)

@click.command()
@click.argument('code', type=int, nargs=1)
@click.option('--pin', '-p', type=int, default=21)
# @click.option('--wait', '-w', type=float, default=5.0)
@click.option('--repeat', '-r', type=int, default=10)
@click.option('--start_length', '-start', type=int, default=100)
@click.option('--end_length', '-end', type=int, default=300)
def main(code: int, pin: int, repeat: int, start_length: int, end_length: int):
    rf_device = RFDevice(pin)
    rf_device.enable_tx()
    rf_device.tx_repeat = repeat
    LOGGER.info(f'RF device ready')
    for i in range(start_length, end_length):
        LOGGER.info(f'Sending {code} with pulse-length={i}, {repeat} times, protocol 1')
        rf_device.tx_code(code, 1, i, 24)
        input("Press Enter to continue...")
    rf_device.cleanup()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s',)
    main()

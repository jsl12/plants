import logging
import time

import click
from constants import OUTLET_2_ON, OUTLET_2_OFF
from rpi_rf import RFDevice

LOGGER = logging.getLogger(__name__)

@click.command()
@click.argument('pause', type=float, nargs=1, default=2.0)
@click.option('--type', '-t', type=str, default='off')
@click.option('--gpio', '-g', type=int, default=21)
@click.option('--repeat', '-r', type=int, default=10)
def main(pause: float, type: str, gpio: int, repeat: int):
    rf_device = RFDevice(gpio)
    rf_device.enable_tx()
    rf_device.tx_repeat = repeat
    try:
        if type == 'on':
            code1, code2 = OUTLET_2_ON, OUTLET_2_OFF
        elif type == 'off':
            code1, code2 = OUTLET_2_OFF, OUTLET_2_ON
        else:
            raise ValueError(f'Invalid type: {type}')

        LOGGER.info(f'Sending code {code1}')
        rf_device.tx_code(code1, 1, 100, 24)
        LOGGER.info(f'Waiting for {pause:.1f}s...')
        time.sleep(pause)
        LOGGER.info(f'Sending code {code2}')
        rf_device.tx_code(code2, 1, 100, 24)

    except Exception as e:
        LOGGER.exception(e)
    finally:
        LOGGER.info(f'Cleaning up GPIO')
        rf_device.cleanup()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
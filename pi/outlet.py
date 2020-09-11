import logging
import time

import click
from rpi_rf import RFDevice

LOGGER = logging.getLogger(__name__)

OUTLETS = [
    {
        'on': 1381683,
        'off': 1381692
    },
    {
        'on': 1381827,
        'off': 1381836
    },
    {
        'on': 1382147,
        'off': 1382156
    },
]

@click.command()
@click.option('--outlet', '-o', type=int)
@click.option('--type', '-t', type=str, default='off')
@click.option('--gpio', '-g', type=int, default=21)
@click.option('--repeat', '-r', type=int, default=10)
@click.option('--pause', '-p', type=float, nargs=1, default=None)
def main(outlet: int, type: str, gpio: int, repeat: int, pause: float):
    assert type in ['on', 'off']
    rf_device = RFDevice(gpio)
    rf_device.enable_tx()
    rf_device.tx_repeat = repeat
    try:
        LOGGER.info(f'Turning outlet {outlet} {type}')
        rf_device.tx_code(OUTLETS[outlet][type], 1, 100, 24)

        if pause is not None:
            if type == 'on':
                type = 'off'
            elif type == 'off':
                type = 'on'

            LOGGER.info(f'Waiting for {pause:.1f}s...')
            time.sleep(pause)

            LOGGER.info(f'Turning outlet {outlet} {type}')
            rf_device.tx_code(OUTLETS[outlet][type], 1, 100, 24)

    except Exception as e:
        LOGGER.exception(e)
    finally:
        LOGGER.info(f'Cleaning up GPIO')
        rf_device.cleanup()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s')
    main()
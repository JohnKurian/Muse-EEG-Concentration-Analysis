# import asyncio
# from bleak import BleakScanner

# async def run():
#     devices = await BleakScanner.discover()
#     for d in devices:
#         print(d)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())

from muselsl import stream, list_muses, record

muses = list_muses(backend="bleak")
stream(muses[0]['address'], ppg_enabled=True, acc_enabled=True, gyro_enabled=True, backend="bleak", timeout=100)
import loguru
from tqdm import tqdm

loguru.logger.remove()
loguru.logger.add(lambda msg: tqdm.write(msg, end=""))

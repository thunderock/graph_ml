from graph_ml.utils.logger import logger
from os import path


def test_output_file():
    logger.info("Test info message")
    logger.error("Test error message")
    logger.debug("Test debug message")
    # check output file graph_ml.log exists
    assert path.exists("graph_ml.log")
    # check output file is not empty
    assert path.getsize("graph_ml.log") > 0

from graph_ml.utils.logger import logger


def test_logger():
    logger.info("Test info message")
    logger.error("Test error message")
    logger.debug("Test debug message")
    assert True

import logging
import sys

def configurar_logger(nivel: str = "INFO") -> logging.Logger:
    """Configura um logger seguro e estruturado."""
    logger = logging.getLogger("p0_classificador")
    
    # Evita duplicar handlers se a função for chamada mais de uma vez
    if logger.hasHandlers():
        logger.handlers.clear()
        
    logger.setLevel(nivel)
    
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger
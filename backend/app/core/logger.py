# core/logger.py

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger("delivery_app")



# USE CASE 
                                   
# from app.core.logger import logger                
                                                  
# logger.info("Order created successfully")         
# logger.error("Payment failed")                    
# logger.warning("Invalid token attempt")           
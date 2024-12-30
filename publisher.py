import logging
import redis

CHANNEL = "test"
REDIS_HOST = "redis"

r = redis.Redis(host="redis")

def publish(message):
    while True:  # note: limit this to x attempts, not a good idea to try indefinitely
        global r
        try:            
            rcvd = r.publish(CHANNEL, message)
            if rcvd >0:
                break
        except redis.ConnectionError as e:
            logging.error(e)
            logging.error("Will attempt to retry")
        except Exception as e:
            logging.error(e)
            logging.error("Other exception")
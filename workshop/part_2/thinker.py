import asyncio
import logging
import pickle

import redis

from aiohttp import web

from thoughts import thoughts

# Logger configuration
logger = logging.getLogger(__name__)

# Setup access logging
aiohttp_logger = logging.getLogger('aiohttp.access')
aiohttp_logger.addHandler(logging.StreamHandler())
aiohttp_logger.setLevel(logging.DEBUG)

# Configure Redis
# This will report a span with the default settings
redis_client = redis.StrictRedis(host='redis', port=6379)
patch(redis=True)


async def think(subject):
    cached_thought = redis_client.get(subject)
    if cached_thought:
        return pickle.loads(cached_thought)

    await asyncio.sleep(0.5)

    thought = thoughts[subject]
    redis_client.set(subject, pickle.dumps(thought))

    return thought


async def handle(request):
    response = {}
    
    for subject in request.query.getall('subject', []):
        try:
            thought = await think(subject)
            response[subject] = {
                'error': False,
                'quote': thought.quote,
                'author': thought.author,
            }
        except KeyError:
            response[subject] = {
                'error': True,
                'reason': 'This subject is too complicated to be resumed in one sentence.'
            }

    return web.json_response(response)


app = web.Application()
app.router.add_get('/', handle)

web.run_app(app, port=8000)
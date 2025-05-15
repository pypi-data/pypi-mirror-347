from redis import Redis
from pydantic_state.config import state_manager_settings


redis_client = Redis.from_url(state_manager_settings.STATE_MANAGER_REDIS_URL)

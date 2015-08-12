from models import get_session
import default_config as config
db = get_session(config.DB_URL)

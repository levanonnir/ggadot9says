from scorpbot import ScorpBot
from subscriber import create_subscriber, handle_message
from connector import connect_to_redis_server
from globals import INBOUND_CHANNEL, COLORS
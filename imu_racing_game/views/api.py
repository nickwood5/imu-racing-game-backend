from ninja import NinjaAPI
from imu_racing_game.views.debug.router import debug_router

api = NinjaAPI()

api.add_router("/debug", debug_router)

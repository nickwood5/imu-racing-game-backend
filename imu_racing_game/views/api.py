from ninja import NinjaAPI
from imu_racing_game.views.debug.router import debug_router
from imu_racing_game.views.imu_game.router import imu_game_router

api = NinjaAPI(urls_namespace="imu_racing_game")

api.add_router("/debug", debug_router)
api.add_router("/imu_game", imu_game_router)

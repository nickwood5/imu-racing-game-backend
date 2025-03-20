import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from channels.layers import get_channel_layer

# Global mapping from game ID to player data
game_id_to_player_id_to_data = {}
game_loop_task = None


class IMUGameUploadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        global game_loop_task, game_id_to_player_id_to_data

        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.player_id = self.scope["url_route"]["kwargs"]["player_id"]

        await self.accept()
        await self.send(
            text_data=json.dumps({"message": "Connected to IMU Game Upload Consumer"})
        )

        if self.game_id not in game_id_to_player_id_to_data:
            game_id_to_player_id_to_data[self.game_id] = {}

        game_id_to_player_id_to_data[self.game_id][self.player_id] = {"x": 0, "y": 0}

        if game_loop_task is None or game_loop_task.done():
            print("Creating task")
            game_loop_task = asyncio.create_task(game_loop(self.game_id))
        else:
            print("Task already running")

    async def disconnect(self, close_code):
        global game_id_to_player_id_to_data

        if self.game_id in game_id_to_player_id_to_data:
            if self.player_id in game_id_to_player_id_to_data[self.game_id]:
                del game_id_to_player_id_to_data[self.game_id][self.player_id]

            if not game_id_to_player_id_to_data[
                self.game_id
            ]:  # If empty, delete game entry
                del game_id_to_player_id_to_data[self.game_id]

        print(f"IMU Upload Consumer {self.player_id} disconnected (code: {close_code})")
        await self.close()

    async def receive(self, text_data):
        global game_id_to_player_id_to_data

        data = json.loads(text_data)
        if self.game_id in game_id_to_player_id_to_data:
            if self.player_id in game_id_to_player_id_to_data[self.game_id]:
                game_id_to_player_id_to_data[self.game_id][self.player_id] = data


class IMUGameBroadcastConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        await self.accept()

        # Add this connection to the group dedicated to this game ID
        await self.channel_layer.group_add(
            f"imu_game_broadcast_group_{self.game_id}", self.channel_name
        )

        await self.send(
            text_data=json.dumps({"message": "Connected to IMU Broadcast Consumer"})
        )

    async def disconnect(self, close_code):
        # Remove the connection from the dedicated group
        await self.channel_layer.group_discard(
            f"imu_game_broadcast_group_{self.game_id}", self.channel_name
        )
        print(
            f"IMU Broadcast Consumer {self.game_id} disconnected (code: {close_code})"
        )
        await self.close()

    async def send_data(self, event):
        """Handler to forward the latest data to subscribers in this game’s group."""
        data = event["data"]
        await self.send(text_data=json.dumps({"data": data}))

    @staticmethod
    async def broadcast_data(game_id, data):
        """Broadcast new game state to all connected clients."""
        print("Broadcast", game_id, data)

        channel_layer = get_channel_layer()
        if not channel_layer:
            print("No channel layer configured!")
            return

        try:
            await channel_layer.group_send(
                f"imu_game_broadcast_group_{game_id}",
                {"type": "send_data", "data": data},
            )
        except Exception as e:
            print("Error during group_send:", e)


async def game_loop(game_id):
    """Continuously updates game state and broadcasts data to clients."""
    global game_id_to_player_id_to_data, game_loop_task

    print("Game loop started for game:", game_id)

    while (
        game_id in game_id_to_player_id_to_data
        and game_id_to_player_id_to_data[game_id]
    ):
        print("Game loop running for game:", game_id)
        player_id_to_data = game_id_to_player_id_to_data[game_id]

        for player_id, data in player_id_to_data.items():
            data["x"] += 1  # Example update logic
            data["y"] += 1  # Modify this logic as needed

        # Broadcast updated data to all clients in the group
        await IMUGameBroadcastConsumer.broadcast_data(game_id, player_id_to_data)

        await asyncio.sleep(0.1)  # Adjust update frequency (100ms)

    print("Game loop stopped for game:", game_id)
    game_loop_task = None  # Reset game loop task when it ends

import json
from channels.generic.websocket import AsyncWebsocketConsumer

# Global variable to store the latest JPEG image in memory
latest_image = None


class ImageUploadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(
            text_data=json.dumps({"message": "Connected to Image Upload Consumer"})
        )

    async def disconnect(self, close_code):
        print("Image upload consumer disconnected")

    async def receive(self, text_data):
        global latest_image
        data = json.loads(text_data)
        image_data = data.get("image")  # Base64 encoded JPEG image

        if image_data:
            latest_image = image_data  # Store in memory
            await self.channel_layer.group_send(
                "image_broadcast_group",
                {
                    "type": "send_image",
                    "image": latest_image,
                },
            )
            await self.send(
                text_data=json.dumps({"message": "Image received and stored"})
            )
        else:
            await self.send(text_data=json.dumps({"error": "Invalid image data"}))


class ImageBroadcastConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("image_broadcast_group", self.channel_name)
        await self.accept()
        await self.send(
            text_data=json.dumps({"message": "Connected to Image Broadcast Consumer"})
        )

        # If an image is available, send it immediately
        if latest_image:
            await self.send(text_data=json.dumps({"image": latest_image}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "image_broadcast_group", self.channel_name
        )
        print("Image broadcast consumer disconnected")

    async def send_image(self, event):
        """Send the latest image to all connected clients"""
        image = event["image"]
        await self.send(text_data=json.dumps({"image": image}))

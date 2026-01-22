#!/usr/bin/env python3
import asyncio
import logging
import json
from pathlib import Path
from aiohttp import web

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradeAssistant:
    def __init__(self):
        self.data = {"prices": {}, "feed": []}

    async def handle_health(self, request):
        return web.json_response({'status': 'ok'})

    async def handle_status(self, request):
        return web.json_response({'connected': True})

    async def handle_latest(self, request):
        return web.json_response(self.data['prices'])

    async def handle_websocket(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    await ws.send_json({'status': 'ok'})
        except:
            pass
        return ws

    def create_app(self):
        app = web.Application()
        app.router.add_get('/health', self.handle_health)
        app.router.add_get('/api/status', self.handle_status)
        app.router.add_get('/api/latest', self.handle_latest)
        app.router.add_get('/ws', self.handle_websocket)
        return app

    async def run(self):
        logger.info("Starting TradeAssistant...")
        app = self.create_app()
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', 8898)
        await site.start()
        logger.info("✓ API listening on 0.0.0.0:8898")
        await asyncio.Event().wait()

if __name__ == '__main__':
    assistant = TradeAssistant()
    asyncio.run(assistant.run())

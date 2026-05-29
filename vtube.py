import pyvts
import asyncio

plugin_info = {
    "plugin_name": "Dora-chan",
    "developer": "Chi",
    "authentication_token_path": "./pyvts_token.txt"
}

# Hotkey names phải khớp với tên trong VTube Studio (model 魔女)
EMOTION_MAP = {
    "happy": "爱心眼",
    "sad": "哭哭",
    "angry": "生气",
    "excited": "星星眼",
    "neutral": "归零"
}

class VTubeController():
    def __init__(self):
        self.plugin_info = plugin_info
        self.vts = pyvts.vts(plugin_info=self.plugin_info)

    async def connect(self):
        await self.vts.connect()
        await self.vts.request_authenticate_token()
        await self.vts.request_authenticate()

    async def list_hotkeys(self):
        request = self.vts.vts_request.requestHotKeyList()
        response = await self.vts.request(request)
        hotkeys = response.get("data", {}).get("availableHotkeys", [])
        print("[VTube] Danh sách hotkeys:")
        for hk in hotkeys:
            print(f"  name='{hk.get('name')}' | id='{hk.get('hotkeyID')}' | type='{hk.get('type')}'")
        return hotkeys

    async def set_mouth_open(self, value):
        try:
            request = self.vts.vts_request.requestSetParameterValue("MouthOpen", value)
            await self.vts.request(request)
        except Exception as e:
            print(f"[VTube] set_mouth_open lỗi: {e}")

    async def trigger_expression(self, emotion):
        hotkey_name = EMOTION_MAP.get(emotion, "归零")
        try:
            # Reset trước
            reset = self.vts.vts_request.requestTriggerHotKey("归零")
            await self.vts.request(reset)
            # Trigger emotion mới (bỏ qua nếu là neutral)
            if hotkey_name != "归零":
                request = self.vts.vts_request.requestTriggerHotKey(hotkey_name)
                await self.vts.request(request)
            print(f"[VTube] triggered: {hotkey_name} ({emotion})")
        except Exception as e:
            print(f"[VTube] mất kết nối, đang kết nối lại... ({e})")
            try:
                await self.vts.close()
            except Exception:
                pass
            try:
                self.vts = pyvts.vts(plugin_info=self.plugin_info)
                await self.connect()
                request = self.vts.vts_request.requestTriggerHotKey(hotkey_name)
                await self.vts.request(request)
                print(f"[VTube] triggered sau reconnect: {hotkey_name}")
            except Exception as e2:
                print(f"[VTube] thất bại: {e2}")

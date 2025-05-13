import io
import os
import time
import requests

from typing import Callable, Dict, Any, List, Optional
from yophonepy.utils import determine_mime_type, parse_update
from yophonepy.models import Message


class YoPhonePy:
    """
    Python client wrapper for interacting with the YoPhone Bot API.
    Provides utility methods for polling messages, handling commands,
    sending media, and configuring webhooks.
    """

    def __init__(self, api_key: str, base_url: str = "https://yoai.yophone.com/api/pub", verbose: bool = True):
        """
        Initializes the YoPhone bot client.

        Args:
            api_key (str): API key for authenticating with the YoPhone service.
            base_url (str): Optional custom base URL for the API.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.verbose = verbose

        self._message_callbacks: List[Callable[[Dict[str, Any]], None]] = []
        self._command_callbacks: Dict[str, Callable[[Message], None]] = {}

        self._polling_active = False

    def _log(self, message: str):
        if self.verbose:
            print(message)

    def _make_request(
            self,
            method: str,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            files: Optional[List[tuple]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/{endpoint}"

        # Merge default and custom headers
        default_headers = {"X-YoAI-API-Key": self.api_key}
        merged_headers = {**default_headers, **(headers or {})}

        try:
            response = requests.request(method, url, headers=merged_headers, json=data, files=files)
            response.raise_for_status()

            if response.status_code == 200 and response.text.strip():
                self._log(f"[YoPhonePy] ✅ Success: {endpoint}")
                return response.json()

            return None
        except requests.exceptions.RequestException as err:
            self._log(f"[YoPhonePy] ❌ Error in {endpoint}: {err}")
            return None

    def message_handler(
            self,
            func: Callable[[Dict[str, Any]], None]
    ):
        """
        Registers a generic handler for incoming messages.
        """
        self._message_callbacks.append(func)
        return func

    def command_handler(self, command: str):
        """
        Registers a specific handler for a command (without leading slash).
        """

        def decorator(func: Callable[[Message], None]):
            self._command_callbacks[f"/{command}"] = func
            return func

        return decorator

    def fetch_updates(self) -> List[Dict[str, Any]]:
        """
        Fetches new messages or events from YoPhone.
        """
        updates = self._make_request("POST", "getUpdates")
        self._log(f"[YoPhonePy] 📦 Update received: {updates}")
        if updates and "data" in updates:
            return updates["data"]
        return []

    def process_updates(self):
        """
        Handles and dispatches incoming updates to appropriate handlers.
        """
        for raw_update in self.fetch_updates():
            try:
                parsed = parse_update(raw_update)
                msg_obj = Message.from_dict(parsed)

                if msg_obj.text and msg_obj.text.startswith("/"):
                    command = msg_obj.text.split()[0]
                    if command in self._command_callbacks:
                        self._command_callbacks[command](msg_obj)
                        continue

                for handler in self._message_callbacks:
                    handler(parsed)

            except Exception as ex:
                self._log(f"[YoPhonePy] ❌ Failed to process update: {ex}")

    def start_polling(self, interval: int = 3):
        """
        Continuously polls for updates at a specified interval.

        Args:
            interval (int): Delay in seconds between polls.
        """
        self._log("[YoPhonePy] 🚀 Polling started. Press Ctrl+C to stop.")
        self._polling_active = True
        try:
            while self._polling_active:
                self.process_updates()
                time.sleep(interval)
        except KeyboardInterrupt:
            self._log("\n[YoPhonePy] ⛔️ Polling stopped by user (Ctrl+C).")
            self.stop_polling()
        finally:
            self._polling_active = False

    def stop_polling(self):
        """
        Stops the polling loop gracefully.
        """
        self._log("[YoPhonePy] 🛑 Stopping polling loop...")
        self._polling_active = False

    def send_message(
            self,
            chat_id: str,
            text: str
    ) -> Optional[Dict[str, Any]]:
        return self._make_request("POST", "sendMessage", data={"to": chat_id, "text": text})

    def send_message_with_options(
            self,
            chat_id: str,
            text: str,
            options: List[Dict[str, str]]
    ) -> Optional[Dict[str, Any]]:
        payload = {"to": chat_id, "text": text, "options": options}
        return self._make_request("POST", "sendMessage", data=payload)

    def send_message_with_buttons(
            self,
            chat_id: str,
            text: str,
            grid: int = 1,
            options: Optional[List[Dict[str, str]]] = None,
            inline_buttons: Optional[List[Dict[str, str]]] = None
    ) -> Optional[Dict[str, Any]]:
        payload = {
            "to": chat_id,
            "text": text,
            "buttons": {
                "grid": grid,
                "options": options or [],
                "inline_buttons": inline_buttons or []
            }
        }
        return self._make_request("POST", "sendMessage", data=payload)

    def send_files(
            self,
            chat_id: str,
            file_paths: List[str],
            caption: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        payload = {"to": chat_id, "text": caption or ""}
        file_data = []

        for path in file_paths:
            if not os.path.exists(path):
                self._log(f"[YoPhonePy] ❌ File does not exist: {path}")
                return None

            if os.path.getsize(path) > 50 * 1024 * 1024:
                self._log(f"[YoPhonePy] ❌ File exceeds 50MB limit: {path}")
                return None

            try:
                with open(path, "rb") as f:
                    content = f.read()
                mime_type = determine_mime_type(path)
                file_data.append(("file", (os.path.basename(path), io.BytesIO(content), mime_type)))
            except Exception as err:
                self._log(f"[YoPhonePy] ❌ Failed to read file {path}: {err}")
                return None

        return self._make_request("POST", "sendMessage", data=payload, files=file_data)

    def send_message_with_media_url(
            self,
            chat_id: str,
            text: str,
            media_urls: List[str]
    ) -> Optional[Dict[str, Any]]:
        payload = {"to": chat_id, "text": text, "mediaURLs": media_urls}
        return self._make_request("POST", "sendMessage", data=payload)

    def configure_commands(
            self,
            commands: List[Dict[str, str]]
    ) -> Optional[Dict[str, Any]]:
        response = self._make_request("POST", "setCommands", data={"commands": commands})
        if response:
            self._log(f"[YoPhonePy] ✅ Commands configured successfully.")
        return response

    def set_webhook(
            self,
            webhook_url: str
    ) -> Optional[Dict[str, Any]]:
        response = self._make_request("POST", "setWebhook", data={"webhookURL": webhook_url})
        if response:
            self._log(f"[YoPhonePy] ✅ Webhook URL set to: {webhook_url}")
        return response

    def get_webhook_info(self) -> Optional[Dict[str, Any]]:
        return self._make_request("POST", "getWebhookInfo")

    def remove_webhook(self) -> Optional[Dict[str, Any]]:
        response = self._make_request("POST", "deleteWebhook")
        if response:
            self._log(f"[YoPhonePy] ✅ Webhook deleted successfully.")
        return response

    def get_bot_info(self) -> Optional[Dict[str, Any]]:
        return self._make_request("POST", "getMe")

    def get_channel_user_status(
            self,
            channel_id: str,
            user_id: str
    ) -> Optional[Dict[str, Any]]:
        return self._make_request("POST", "getChannelMember", data={"channelId": channel_id, "userId": user_id})

import hashlib
import json
import uuid
import time

from datetime import datetime
from inspect import stack
from typing import Any, Callable

import msgspec
from pydantic import BaseModel

from .payloads import (
    new_bool_payload,
    new_clear_all_payload,
    new_clear_screen_payload,
    new_color_payload,
    new_create_lock_payload,
    new_custom_payload,
    new_dump_payload,
    new_hide_app_payload,
    new_hide_payload,
    new_html_payload,
    new_image_payload,
    new_json_string_payload,
    new_new_screen_payload,
    new_notify_payload,
    new_null_payload,
    new_remove_payload,
    new_show_app_payload,
    new_size_payload,
    new_string_payload,
    new_time_payload,
    new_sql_payload,
    new_log_payload,
)

from .client import Client

class ApplicationMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Application(metaclass=ApplicationMeta):
    def __init__(self, origin=Any):
        self._host = "127.0.0.1"
        self._port = 23517
        self._enabled = True
        self._sent_payloads = []
        self._pending_payloads = []
        self._client = Client(self._host, self._port)
        self._origin = origin
    
    def add(self, payload) -> "Application":
        if self._origin:
           payload.origin = self._origin
        self._pending_payloads.append(payload)
        return self
    
    def flush(self) -> "Application":
        if self._pending_payloads:
            self._sent_payloads = list(self._pending_payloads)
            
            request_payload = {
                "uuid": str(uuid.uuid4()),
                "payloads": [p.to_dict() for p in self._pending_payloads],
                "meta": { "ray_package_version": "0.1.4" },
            }
            if self._enabled:
                try:
                    self.client().send(request_payload)
                except Exception as e:
                    raise ConnectionError(
                        f"Couldn't connect to Ray. It doesn't seem to be running at {self._host}:{self._port}"
                    ) from e
            self._pending_payloads = []
        return self
    
    def client(self) -> Client:
        self._client.set_host(self._host)
        self._client.set_port(self._port)
        return self._client
    
    def port(self) -> int:
        return self._port
    
    def set_port(self, port: int):
        self._port = port
    
    def host(self) -> str:
        return self._host
    
    def set_host(self, host: str):
        self._host = host
    
    def enable(self):
        self._enabled = True
    
    def disable(self):
        self._enabled = False
    
    def enabled(self) -> bool:
        return self._enabled
    
    def disabled(self) -> bool:
        return not self._enabled
    
    def sent_json_payloads(self) -> str:
        return json.dumps([p.to_dict() for p in self._sent_payloads])
    
    def send_custom(self, content: Any, label: str) -> "Application":
        return self.add(new_custom_payload(content, label))
    
    def new_screen(self, name: str) -> "Application":
        return self.add(new_new_screen_payload(name))
    
    def color(self, color: str) -> "Application":
        return self.add(new_color_payload(color))
    
    def size(self, size: str) -> "Application":
        return self.add(new_size_payload(size))
    
    def hide(self) -> "Application":
        return self.add(new_hide_payload())
    
    def hide_app(self) -> "Application":
        return self.add(new_hide_app_payload())
    
    def show_app(self) -> "Application":
        return self.add(new_show_app_payload())
    
    def clear_screen(self) -> "Application":
        return self.add(new_clear_screen_payload())
    
    def clear_all(self) -> "Application":
        return self.add(new_clear_all_payload())
    
    def html(self, html: str) -> "Application":
        return self.add(new_html_payload(html)).flush()
    
    def notify(self, text: str) -> "Application":
        return self.add(new_notify_payload(text))
    
    def bool(self, val: bool) -> "Application":
        return self.add(new_bool_payload(val))
    
    def null(self) -> "Application":
        return self.add(new_null_payload())
    
    def string(self, s: str) -> "Application":
        return self.add(new_string_payload(s))
    
    def time(self, t: datetime) -> "Application":
        return self.add(new_time_payload(t, "%Y-%m-%d %H:%M:%S"))
    
    def time_with_format(self, t: datetime, fmt: str) -> "Application":
        return self.add(new_time_payload(t, fmt))
    
    def pause(self) -> "Application":
        h = hashlib.md5(str(time.time()).encode()).hexdigest()
        self.add(new_create_lock_payload(h)).flush()
        while True:
            time.sleep(1)
            if not self.client().lock_exists(h).get("active", False):
                break
        return self
    
    def to_json(self, *values: Any) -> "Application":
        for v in values:
            self.add(new_json_string_payload(v))
        return self
    
    def image(self, path: str) -> "Application":
        return self.add(new_image_payload(path))
    
    def charles(self) -> "Application":
        return self.add(new_custom_payload("🎶 🎹 🎷 🕺"))
    
    def ban(self) -> "Application":
        return self.add(new_custom_payload("🕶"))
    
    def sql(self, sql: str) -> "Application":
        return self.add(new_sql_payload(sql))
    
    def log(self, value: Any) -> "Application":
        return self.add(new_log_payload(value))
    
    def die(self):
        self.flush()
        self.die_with_status_code(1)
    
    @staticmethod
    def die_with_status_code(status: int):
        exit(status)
    
    def remove(self) -> "Application":
        return self.add(new_remove_payload())
    
    def show_when(self, cond: Callable) -> "Application":
        if callable(cond):
            cond = cond()
        return self if cond else self.remove()
    
    def show_if(self, cond: Callable) -> "Application":
        return self.show_when(cond)
    
    def remove_when(self, cond: Callable) -> "Application":
        if callable(cond):
            cond = cond()
        return self.remove() if cond else self
    
    def remove_if(self, cond: Callable) -> "Application":
        return self.remove_when(cond)


def get_caller_location() -> dict[str, str]:
    frames = stack()
    
    result = {
        "file": "",
        "line_number": "",
        "function_name": ""
    }
    
    for f in frames[2:]:
        if "/site-packages/" not in f.filename:
            result["file"] = f.filename
            result["line_number"] = str(f.lineno)
            result["function_name"] = f.function
            
    return result


def ray(*values: Any) -> Application:
    r = Application(
        origin=get_caller_location()
    )
    
    for value in values:
        if isinstance(value, bool):
            r.add(new_bool_payload(value))
        elif value is None:
            r.add(new_null_payload())
        elif isinstance(value, (str, int, float, complex)):
            r.add(new_custom_payload(value))
        elif isinstance(value, msgspec.Struct):
            r.add(new_json_string_payload(msgspec.json.encode(value).decode("utf-8")))
        elif isinstance(value, BaseModel):
            r.add(new_json_string_payload(value.model_dump()))
        else:
            r.add(new_dump_payload(value))
    return r

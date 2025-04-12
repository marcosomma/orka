import os
import pytest
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_logger_write_and_read(monkeypatch):
    from orka.memory_logger import RedisMemoryLogger
    logger = RedisMemoryLogger()
    logger.log("test_agent", "output", {"foo": "bar"})
    items = logger.client.xrevrange("orka:memory", count=1)
    assert len(items[0][1]) == 4
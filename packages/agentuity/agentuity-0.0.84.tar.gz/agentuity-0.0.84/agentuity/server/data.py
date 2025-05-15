from typing import Optional, Union
import base64
import json
from typing import IO
from aiohttp import StreamReader


class EmptyDataReader(StreamReader):
    def __init__(self, protocol=None, limit=1):
        super().__init__(protocol, limit)

    async def read(self) -> bytes:
        return b""

    async def readany(self) -> bytes:
        return b""

    async def readexactly(self, n: int) -> bytes:
        if n > 0:
            raise ValueError("Empty stream cannot provide requested bytes")
        return b""

    async def readline(self) -> bytes:
        return b""

    async def readchunk(self) -> tuple[bytes, bool]:
        return b"", True

    def at_eof(self) -> bool:
        return True

    def exception(self) -> Optional[Exception]:
        return None

    def set_exception(self, exc: Exception) -> None:
        pass

    def unread_data(self, data: bytes) -> None:
        pass

    def feed_eof(self) -> None:
        pass

    def feed_data(self, data: bytes) -> None:
        pass

    def begin_http_chunk_receiving(self) -> None:
        pass

    def end_http_chunk_receiving(self) -> None:
        pass


class StringStreamReader(StreamReader):
    def __init__(self, data: str, protocol=None, limit=2**16):
        super().__init__(protocol, limit)
        self._data = data.encode("utf-8")
        self._pos = 0
        self._eof = False

    async def read(self) -> bytes:
        if self._eof:
            return b""
        data = self._data[self._pos :]
        self._pos = len(self._data)
        self._eof = True
        return data

    async def readany(self) -> bytes:
        return await self.read()

    async def readexactly(self, n: int) -> bytes:
        if n < 0:
            raise ValueError("n must be non-negative")
        if self._eof:
            if n > 0:
                raise ValueError("Not enough data to read")
            return b""
        remaining = len(self._data) - self._pos
        if n > remaining:
            raise ValueError("Not enough data to read")
        data = self._data[self._pos : self._pos + n]
        self._pos += n
        if self._pos >= len(self._data):
            self._eof = True
        return data

    async def readline(self) -> bytes:
        if self._eof:
            return b""
        data = self._data[self._pos :]
        self._pos = len(self._data)
        self._eof = True
        return data

    async def readchunk(self) -> tuple[bytes, bool]:
        if self._eof:
            return b"", True
        data = self._data[self._pos :]
        self._pos = len(self._data)
        self._eof = True
        return data, True

    def at_eof(self) -> bool:
        return self._eof

    def exception(self) -> Optional[Exception]:
        return None

    def set_exception(self, exc: Exception) -> None:
        pass

    def unread_data(self, data: bytes) -> None:
        if self._pos < len(data):
            raise ValueError("Cannot unread more data than was read")
        self._pos -= len(data)
        self._eof = False

    def feed_eof(self) -> None:
        self._eof = True

    def feed_data(self, data: bytes) -> None:
        raise NotImplementedError("StringStreamReader does not support feeding data")

    def begin_http_chunk_receiving(self) -> None:
        pass

    def end_http_chunk_receiving(self) -> None:
        pass


class BytesStreamReader(StreamReader):
    def __init__(self, data: bytes, protocol=None, limit=2**16):
        super().__init__(protocol, limit)
        self._data = data
        self._pos = 0
        self._eof = False

    async def read(self) -> bytes:
        if self._eof:
            return b""
        data = self._data[self._pos :]
        self._pos = len(self._data)
        self._eof = True
        return data

    async def readany(self) -> bytes:
        return await self.read()

    async def readexactly(self, n: int) -> bytes:
        if n < 0:
            raise ValueError("n must be non-negative")
        if self._eof:
            if n > 0:
                raise ValueError("Not enough data to read")
            return b""
        remaining = len(self._data) - self._pos
        if n > remaining:
            raise ValueError("Not enough data to read")
        data = self._data[self._pos : self._pos + n]
        self._pos += n
        if self._pos >= len(self._data):
            self._eof = True
        return data

    async def readline(self) -> bytes:
        if self._eof:
            return b""
        data = self._data[self._pos :]
        self._pos = len(self._data)
        self._eof = True
        return data

    async def readchunk(self) -> tuple[bytes, bool]:
        if self._eof:
            return b"", True
        data = self._data[self._pos :]
        self._pos = len(self._data)
        self._eof = True
        return data, True

    def at_eof(self) -> bool:
        return self._eof

    def exception(self) -> Optional[Exception]:
        return None

    def set_exception(self, exc: Exception) -> None:
        pass

    def unread_data(self, data: bytes) -> None:
        if self._pos < len(data):
            raise ValueError("Cannot unread more data than was read")
        self._pos -= len(data)
        self._eof = False

    def feed_eof(self) -> None:
        self._eof = True

    def feed_data(self, data: bytes) -> None:
        raise NotImplementedError("BytesStreamReader does not support feeding data")

    def begin_http_chunk_receiving(self) -> None:
        pass

    def end_http_chunk_receiving(self) -> None:
        pass


class DataResult:
    """
    A container class for the result of a data operation, providing access to the data
    and information about whether the data exists.
    """

    def __init__(self, data: Optional["Data"] = None):
        """
        Initialize a DataResult with optional data.

        Args:
            data: Optional Data object containing the result data
        """
        if data is None:
            self._exists = False
            self._data = Data("application/octet-stream", EmptyDataReader())
        else:
            self._exists = True
            self._data = data

    @property
    def data(self) -> Optional["Data"]:
        """
        Get the data from the result of the operation.

        Returns:
            Optional[Data]: The data object containing the result content, or None if exists is False
        """
        return None if not self._exists else self._data

    @property
    def exists(self) -> bool:
        """
        Check if the data was found.

        Returns:
            bool: True if the data exists, False otherwise
        """
        return self._exists

    def __str__(self) -> str:
        """
        Get a string representation of the data result.

        Returns:
            str: A formatted string containing the content type and payload
        """
        return f"DataResult(data={self._data})"


class Data:
    """
    A container class for working with agent data payloads. This class provides methods
    to handle different types of data (text, JSON, binary) and supports streaming
    functionality for large payloads.
    """

    def __init__(self, contentType: str, stream: StreamReader):
        """
        Initialize a Data object with a dictionary containing payload information.

        Args:
            data: Dictionary containing:
        """
        self._contentType = contentType
        self._stream = stream
        self._loaded = False
        self._data = None

    async def _ensure_stream_loaded(self):
        if not self._loaded:
            self._loaded = True
            self._data = await self._stream.read()
        return self._data

    async def stream(self) -> IO[bytes]:
        """
        Get the data as a stream of bytes.

        Returns:
            IO[bytes]: A file-like object providing access to the data as bytes
        """
        if self._loaded:
            raise ValueError("Stream already loaded")
        return self._stream

    @property
    def contentType(self) -> str:
        """
        Get the content type of the data.

        Returns:
            str: The MIME type of the data. If not provided, it will be inferred from
                the data. If it cannot be inferred, returns 'application/octet-stream'
        """
        return self._contentType

    async def base64(self) -> str:
        """
        Get the base64 encoded string of the data.

        Returns:
            str: The base64 encoded payload
        """
        data = await self._ensure_stream_loaded()
        return encode_payload(data)

    async def text(self) -> bytes:
        """
        Get the data as a string.

        Returns:
            bytes: The decoded text content
        """
        data = await self._ensure_stream_loaded()
        return data.decode("utf-8")

    async def json(self) -> dict:
        """
        Get the data as a JSON object.

        Returns:
            dict: The parsed JSON data

        Raises:
            ValueError: If the data is not valid JSON
        """
        try:
            return json.loads(await self.text())
        except Exception as e:
            raise ValueError(f"Data is not JSON: {e}") from e

    async def binary(self) -> bytes:
        """
        Get the data as binary bytes.

        Returns:
            bytes: The raw binary data
        """
        data = await self._ensure_stream_loaded()
        return data


def encode_payload(data: Union[str, bytes]) -> str:
    """
    Encode a string or bytes into base64.

    Args:
        data: UTF-8 string or bytes to encode

    Returns:
        str: Base64 encoded string
    """
    if isinstance(data, bytes):
        return base64.b64encode(data).decode("utf-8")
    else:
        return base64.b64encode(data.encode("utf-8")).decode("utf-8")


def value_to_payload(
    content_type: str, value: Union[str, int, float, bool, list, dict, bytes, "Data"]
) -> Data:
    """
    Convert a value to a Data object.

    Args:
        content_type: The desired content type for the payload
        value: The value to convert. Can be:
            - Data object
            - bytes
            - str, int, float, bool
            - list or dict (will be converted to JSON)

    Returns:
        Data: The Data object containing

    Raises:
        ValueError: If the value type is not supported
    """
    if isinstance(value, Data):
        return value
    elif isinstance(value, bytes):
        content_type = content_type or "application/octet-stream"
        return Data(content_type, BytesStreamReader(value))
    elif isinstance(value, (str, int, float, bool)):
        content_type = content_type or "text/plain"
        payload = str(value)
        return Data(content_type, StringStreamReader(payload))
    elif isinstance(value, (list, dict)):
        content_type = content_type or "application/json"
        payload = json.dumps(value)
        return Data(content_type, StringStreamReader(payload))
    else:
        raise ValueError(f"Unsupported value type: {type(value)}")

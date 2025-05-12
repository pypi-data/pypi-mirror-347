import atexit
import contextlib
import json
import time
from functools import wraps
import traceback
from typing import Any, Dict, Generator, Iterator, List, Optional, Tuple, Union

import grpc

from tensorpc.core import core_io as core_io
from tensorpc.core.defs import RelayCallType
from tensorpc.protos_export import remote_object_pb2 as rpc_pb2
from tensorpc.protos_export import rpc_message_pb2 as rpc_msg_pb2

from tensorpc.protos_export import \
    remote_object_pb2_grpc as remote_object_pb2_grpc
from tensorpc.utils.wait_tools import wait_until
from tensorpc.utils.df_logging import get_logger

LOGGER = get_logger()


class RemoteException(RuntimeError):
    pass


class _PlaceHolder:
    pass


def format_stdout(stdout_string: str, prefix: str) -> str:
    lines = stdout_string.split("\n")
    if lines[-1] == "\n":
        lines = lines[:-1]
    res = "\n".join([prefix + s for s in lines[:-1]])
    res += "\n"
    return res


class RemoteObject(object):
    """
    channel: grpc.Channel
    stub: remote_object_pb2_grpc.RemoteObjectStub
    func_dict: Dict[str, Any]
    name: str
    shared_mem: np.ndarray
    output_shared_mem: np.ndarray
    num_blocks: int
    """
    _stub: Optional[remote_object_pb2_grpc.RemoteObjectStub]

    def __init__(self,
                 channel: Optional[grpc.Channel],
                 name="",
                 print_stdout=True):

        self._channel = channel
        if channel is not None:
            self._stub = remote_object_pb2_grpc.RemoteObjectStub(channel)
        else:
            self._stub = None
        self.name = name
        self.print_stdout = print_stdout

    def enabled(self):
        return self._channel is not None

    @property
    def channel(self):
        assert self._channel is not None, "you need to provide a channel to enable rpc feature."
        return self._channel

    @property
    def stub(self):
        assert self._stub is not None, "you need to provide a channel to enable rpc feature."
        return self._stub

    def query_server_meta(self):
        response = self.stub.QueryServerMeta(rpc_msg_pb2.RemoteCallRequest())
        return json.loads(response.data)

    def query_service_meta(self, key):
        response = self.stub.QueryServiceMeta(
            rpc_msg_pb2.RemoteCallRequest(service_key=key))
        return json.loads(response.data)

    def _remote_print(self, stdout):
        if not self.print_stdout:
            return
        if stdout == "":
            return
        prefix = ""
        if self.name != "":
            prefix = "[{}]".format(self.name)
        print(format_stdout(stdout, prefix), end="")

    def _check_remote_exception(self, exception_bytes: bytes):
        if exception_bytes == "":
            return
        exc_dict = json.loads(exception_bytes)
        raise RemoteException(exc_dict["detail"])

    def _check_remote_exception_noexcept(self, exception_bytes: bytes):
        if exception_bytes == "":
            return None
        exc_dict = json.loads(exception_bytes)
        return RemoteException(exc_dict["detail"])

    def say_hello(self, msg: str):
        response = self.stub.SayHello(rpc_msg_pb2.HelloRequest(data=msg))
        return response.data

    def remote_call_future(self,
                           key: str,
                           *args,
                           rpc_callback="",
                           rpc_flags: int = rpc_msg_pb2.PickleArray,
                           **kwargs) -> grpc.Future:
        data_to_be_send = core_io.data_to_pb((args, kwargs), rpc_flags)
        request = rpc_msg_pb2.RemoteCallRequest(service_key=key,
                                                arrays=data_to_be_send,
                                                flags=rpc_flags,
                                                callback=rpc_callback)
        return self.stub.RemoteCall.future(request)

    def remote_json_call_future(self,
                                key: str,
                                *args,
                                rpc_callback="",
                                rpc_flags: int = rpc_msg_pb2.JsonArray,
                                **kwargs) -> grpc.Future:
        arrays, decoupled = core_io.data_to_json((args, kwargs), rpc_flags)
        request = rpc_msg_pb2.RemoteJsonCallRequest(service_key=key,
                                                    arrays=arrays,
                                                    data=decoupled,
                                                    flags=rpc_flags,
                                                    callback=rpc_callback)
        return self.stub.RemoteJsonCall.future(request)

    def remote_call(self,
                    key: str,
                    *args,
                    rpc_timeout: Optional[int] = None,
                    rpc_callback="",
                    rpc_flags: int = rpc_msg_pb2.PickleArray,
                    **kwargs) -> Any:
        future = self.remote_call_future(key,
                                         *args,
                                         rpc_callback=rpc_callback,
                                         rpc_flags=rpc_flags,
                                         **kwargs)
        # return future.result(timeout)
        return self.parse_remote_response(future.result(rpc_timeout))

    def remote_json_call(self,
                         key: str,
                         *args,
                         rpc_timeout: Optional[int] = None,
                         rpc_callback="",
                         rpc_flags: int = rpc_msg_pb2.JsonArray,
                         **kwargs) -> Any:
        future = self.remote_json_call_future(key,
                                              *args,
                                              rpc_callback=rpc_callback,
                                              rpc_flags=rpc_flags,
                                              **kwargs)
        return self.parse_remote_json_response(future.result(rpc_timeout))

    def parse_remote_json_response(self, response):
        self._check_remote_exception(response.exception)
        return core_io.data_from_json(response.arrays, response.data,
                                      response.flags)[0]

    def parse_remote_response_noexcept(self, response):
        exc = self._check_remote_exception_noexcept(response.exception)
        if exc is not None:
            return response, exc
        # TODO core_io.data_from_pb is slow (45us), try to optimize it.
        results = core_io.data_from_pb(response.arrays, response.flags)
        results = results[0]
        return results, exc

    def parse_remote_response(self, response):
        res, exc = self.parse_remote_response_noexcept(response)
        if exc is not None:
            raise exc
        return res

    def remote_generator(self,
                         key: str,
                         *args,
                         timeout: Optional[int] = None,
                         rpc_callback="",
                         rpc_flags: int = rpc_msg_pb2.PickleArray,
                         **kwargs) -> Any:
        data_to_be_send = core_io.data_to_pb((args, kwargs), rpc_flags)
        request = rpc_msg_pb2.RemoteCallRequest(service_key=key,
                                                arrays=data_to_be_send,
                                                flags=rpc_flags,
                                                callback=rpc_callback)
        for response in self.stub.RemoteGenerator(request):
            yield self.parse_remote_response(response)

    def client_stream(self,
                      key: str,
                      stream_iter,
                      *args,
                      timeout: Optional[int] = None,
                      rpc_flags: int = rpc_msg_pb2.PickleArray,
                      **kwargs) -> Any:
        flags = rpc_flags

        def wrapped_generator():
            data_to_be_send = core_io.data_to_pb((args, kwargs), flags)
            request = rpc_msg_pb2.RemoteCallRequest(service_key=key,
                                                    arrays=data_to_be_send,
                                                    flags=flags)
            yield request
            for data in stream_iter:
                data_to_be_send = core_io.data_to_pb(((data, ), {}), flags)
                request = rpc_msg_pb2.RemoteCallRequest(service_key=key,
                                                        arrays=data_to_be_send,
                                                        flags=flags)
                yield request

        response = self.stub.ClientStreamRemoteCall(wrapped_generator())
        return self.parse_remote_response(response)

    def bi_stream(self,
                  key: str,
                  stream_iter,
                  *args,
                  timeout: Optional[int] = None,
                  rpc_flags: int = rpc_msg_pb2.PickleArray,
                  **kwargs):
        flags = rpc_flags

        def wrapped_generator():
            data_to_be_send = core_io.data_to_pb((args, kwargs), flags)
            request = rpc_msg_pb2.RemoteCallRequest(service_key=key,
                                                    arrays=data_to_be_send,
                                                    flags=flags)
            yield request
            for data in stream_iter:
                data_to_be_send = core_io.data_to_pb(((data, ), {}), flags)
                request = rpc_msg_pb2.RemoteCallRequest(service_key=key,
                                                        arrays=data_to_be_send,
                                                        flags=flags)
                yield request

        for response in self.stub.BiStreamRemoteCall(wrapped_generator()):
            yield self.parse_remote_response(response)

    def stream_remote_call(
            self,
            key: str,
            stream_iter: Iterator[Any],
            rpc_flags: int = rpc_msg_pb2.PickleArray) -> Iterator[Any]:
        # assert key in self.func_dict
        flags = rpc_flags

        def stream_generator():
            for data in stream_iter:
                # data must be (args, kwargs)
                data_to_be_send = core_io.data_to_pb(data, flags)
                yield rpc_msg_pb2.RemoteCallRequest(service_key=key,
                                                    arrays=data_to_be_send,
                                                    flags=flags)

        responses = self.stub.RemoteStreamCall(stream_generator())
        for response in responses:
            yield self.parse_remote_response(response)

    def shutdown(self) -> None:
        self.stub.ServerShutdown(rpc_msg_pb2.HealthCheckRequest())

    def health_check(self, wait_for_ready=False,
                           timeout=None) -> Dict[str, float]:
        t = time.time()
        response = self.stub.HealthCheck(rpc_msg_pb2.HealthCheckRequest(),
            wait_for_ready=wait_for_ready,
            timeout=timeout)
        # server_time = json.loads(response.data)
        return {
            "total": time.time() - t,
            # "to_server": server_time - t,
        }

    def _prepare_relay_reqs(self,
                            urls: list[str],
                            type: RelayCallType,
                            rpc_timeout: Optional[int] = None,
                            rpc_flags: int = rpc_msg_pb2.PickleArray):
        relay_data = {
            "urls": urls,
            "type": int(type),
            "rpc_timeout": rpc_timeout
        }
        relay_bin = core_io.dumps_method(relay_data, rpc_flags)
        res = core_io.to_protobuf_stream([relay_bin], "", rpc_flags)
        return res 

    def chunked_stream_remote_call(
            self,
            key: str,
            stream_iter,
            rpc_flags: int = rpc_msg_pb2.PickleArray,
            rpc_timeout: Optional[int] = None,
            rpc_chunk_size: int = 256 * 1024,
            rpc_relay_urls: Optional[list[str]] = None) -> Iterator[Any]:
        # assert key in self.func_dict
        flags = rpc_flags

        def stream_generator():
            if rpc_relay_urls is not None:
                relay_reqs = self._prepare_relay_reqs(
                    rpc_relay_urls, RelayCallType.RemoteCall, rpc_timeout,
                    rpc_flags)
                for chunk in relay_reqs:
                    yield chunk

            for data in stream_iter:
                arrays, data_skeleton = core_io.extract_arrays_from_data(data)
                data_to_be_send = arrays + [
                    core_io.dumps_method(data_skeleton, flags)
                ]
                stream = core_io.to_protobuf_stream_gen(
                    data_to_be_send, key, flags, rpc_chunk_size)
                for s in stream:
                    yield s
        if rpc_relay_urls is not None:
            serv_fn = self.stub.RelayStream
        else:
            serv_fn = self.stub.ChunkedRemoteCall
        responses = serv_fn(stream_generator(), timeout=rpc_timeout)
        from_stream = core_io.FromBufferStream()
        for response in responses:
            self._check_remote_exception(response.exception)
            res = from_stream(response)
            if res is not None:
                from_stream.clear()
                results_raw, _ = res
                results_array = results_raw[:-1]
                data_skeleton_bytes = results_raw[-1]
                data_skeleton = core_io.loads_method(data_skeleton_bytes,
                                                     flags)
                results = core_io.put_arrays_to_data(results_array,
                                                     data_skeleton)
                results = results[0]
                yield results

    def chunked_remote_call(self,
                            key,
                            *args,
                            rpc_flags: int = rpc_msg_pb2.PickleArray,
                            rpc_timeout: Optional[int] = None,
                                  rpc_relay_urls: Optional[list[str]] = None,
                            **kwargs) -> Any:

        def stream_generator():
            yield (args, kwargs)

        count = 0
        res: Optional[_PlaceHolder] = _PlaceHolder()
        for res in self.chunked_stream_remote_call(key,
                                                   stream_generator(),
                                                   rpc_flags=rpc_flags,
                                                   rpc_timeout=rpc_timeout,
                                                   rpc_relay_urls=rpc_relay_urls):
            count += 1
        assert count == 1
        assert not isinstance(res, _PlaceHolder)
        return res

    def _wait_func(self):
        try:
            self.health_check()
            return True
        except grpc.RpcError:
            LOGGER.info("server still not ready")
            return False

    def wait_for_remote_ready(self, timeout: float = 10, max_retries=20):
        try:
            wait_until(self._wait_func, max_retries, timeout / max_retries)
        except TimeoutError as e:
            LOGGER.error("server timeout.")
            raise e

    def reconnect(self, timeout=10, max_retries=20):
        self.wait_for_remote_ready(timeout / max_retries, max_retries)


class RemoteManager(RemoteObject):

    def __init__(self,
                 url,
                 name="",
                 channel_options=None,
                 credentials=None,
                 print_stdout=True,
                 enabled=True):
        if enabled:
            if credentials is not None:
                channel = grpc.secure_channel(url,
                                              credentials,
                                              options=channel_options)
            else:
                channel = grpc.insecure_channel(url, options=channel_options)
        else:
            channel = None
        self.credentials = credentials
        self._channel_options = channel_options
        self.url = url
        if enabled:
            self._channel = channel
        super().__init__(channel, name, print_stdout)
        # if enabled:
        #     self.wait_for_channel_ready()
        # atexit.register(self.close)

    def reconnect(self, timeout=10, max_retries=20):
        self.close()
        if self.credentials is not None:
            self._channel = grpc.secure_channel(self.url,
                                                self.credentials,
                                                options=self._channel_options)
        else:
            self._channel = grpc.insecure_channel(
                self.url, options=self._channel_options)
        self._stub = remote_object_pb2_grpc.RemoteObjectStub(self.channel)
        self.wait_for_remote_ready(timeout, max_retries)

    def wait_for_channel_ready(self, timeout: float = 10):
        assert self._channel is not None
        wait_for_ready = True
        try:
            self.health_check(wait_for_ready, timeout)
        except grpc.RpcError as rpc_error:
            traceback.print_exc()
            assert rpc_error.code() == grpc.StatusCode.UNAVAILABLE
            assert not wait_for_ready

    def wait_for_remote_ready(self, timeout: float = 10, max_retries=20):
        self.wait_for_channel_ready(timeout)
        super().wait_for_remote_ready(timeout, max_retries)

    def available(self, timeout=10, max_retries=20):
        try:
            self.wait_for_remote_ready(timeout, max_retries)
            return True
        except TimeoutError:
            return False

    def close(self, close_channel: bool = True):
        if self._channel is not None:
            # if we shutdown remote and close channel,
            # will raise strange error.
            if close_channel:
                self.channel.close()
            del self._channel
            self._channel = None

    def shutdown(self):
        super().shutdown()
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self._channel is not None:
            self._channel.__exit__(exc_type, exc_value, exc_traceback)
        return self.close(close_channel=False)


@contextlib.contextmanager
def simple_client(addr):
    with RemoteManager(addr) as robj:
        yield robj


def simple_remote_call(addr, key, *args, rpc_timeout=None, **kwargs):
    with RemoteManager(addr) as robj:
        return robj.remote_call(key, *args, rpc_timeout=rpc_timeout, **kwargs)


def simple_chunk_call(addr, key, *args, rpc_timeout: Optional[int] = None, rpc_relay_urls: Optional[list[str]] = None, **kwargs):
    with RemoteManager(addr) as robj:
        return robj.chunked_remote_call(key, *args, rpc_timeout=rpc_timeout, rpc_relay_urls=rpc_relay_urls, **kwargs)

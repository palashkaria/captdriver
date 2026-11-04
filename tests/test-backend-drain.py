#!/usr/bin/env python3
"""Exercise the real CUPS backend against a fake USB daemon; no hardware needed."""
import os
from pathlib import Path
import select
import signal
import socket
import struct
import tempfile

BACKEND = os.environ.get("CAPT_BACKEND", str(Path(__file__).resolve().parents[1] / "persistent" / "capt"))

def check_drain(payload):
    with tempfile.TemporaryDirectory(prefix="capt-test-") as directory:
        path = directory + "/usb.sock"
        listener = socket.socket(socket.AF_UNIX)
        listener.bind(path)
        listener.listen(1)
        listener.settimeout(3)
        read_fd, write_fd = os.pipe()
        side, child_side = socket.socketpair()
        # Both input and DRAIN_OUTPUT are ready before the backend starts.
        os.write(write_fd, payload)
        side.sendall(bytes([2, 0, 0, 0]))  # CUPS_SC_CMD_DRAIN_OUTPUT
        pid = os.fork()
        if pid == 0:
            try:
                os.dup2(read_fd, 0)
                os.dup2(child_side.fileno(), 4)  # CUPS_SC_FD
                for fd in (read_fd, write_fd, side.fileno(), child_side.fileno(), listener.fileno()):
                    if fd not in (0, 4):
                        try:
                            os.close(fd)
                        except OSError:
                            pass
                os.set_inheritable(4, True)
                env = dict(os.environ, DEVICE_URI="capt:" + path)
                os.execve(BACKEND, [BACKEND, "1", "test", "drain-test", "1", ""], env)
            finally:
                os._exit(127)
        connection = None
        try:
            os.close(read_fd)
            child_side.close()
            connection, _ = listener.accept()
            connection.settimeout(3)
            def exact(count):
                data = b""
                while len(data) < count:
                    part = connection.recv(count - len(data))
                    assert part, "backend disconnected before forwarding print data"
                    data += part
                return data
            received = b""
            while len(received) < len(payload):
                length = struct.unpack("<I", exact(4))[0]
                assert 0 < length <= 4096, "USB frames must be at most 4096 bytes"
                received += exact(length)
                if len(received) < len(payload):
                    connection.sendall(b"K")
            assert received == payload, "print data changed or was reordered"
            # Withhold the last USB acknowledgement: DRAIN must still be pending.
            assert not select.select([side], [], [], 0.2)[0], "drain acknowledged before USB completion"
            connection.sendall(b"K")
            assert select.select([side], [], [], 2)[0], "missing acknowledgement after USB completion"
            assert side.recv(4) == bytes([2, 1, 0, 0]), "unexpected CUPS drain response"
        finally:
            try:
                os.kill(pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            os.waitpid(pid, 0)
            if connection:
                connection.close()
            listener.close()
            side.close()
            os.close(write_fd)

if __name__ == "__main__":
    for size in (4, 4097):
        check_drain(bytes(index % 251 for index in range(size)))
        print("PASS: drain ordering and 4 KB frame limit ({} bytes)".format(size))

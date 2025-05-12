from mcp.server.fastmcp import FastMCP
import subprocess
import socket
import os

DEFAULT_PORT = 12345
DEVICE_PATH = '/data/local/tmp/traceserver'

server = FastMCP(transport_type='stdio')

def adb_cmd(sn, base_cmd):
    """Construct an adb command for a specific device serial number."""
    return ['adb', '-s', sn] + base_cmd if sn else ['adb'] + base_cmd

def get_device_abi(sn=''):
    """Get the ABI of the connected Android device."""
    cmd = adb_cmd(sn, ['shell', 'getprop', 'ro.product.cpu.abi'])
    return subprocess.check_output(cmd, encoding='utf-8').strip()

def get_binary_path_for_abi(abi):
    """Get the path to the traceserver binary for the specified ABI."""
    binary_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'bin', abi, 'traceserver')
    if not os.path.exists(binary_path):
        raise FileNotFoundError(f'No binary for ABI: {abi} at {binary_path}')
    return binary_path

def push_and_start_server(sn='', test_mode=False):
    """Push traceserver binary, make it executable, kill previous instance, start it, and forward the port."""
    abi = get_device_abi(sn)
    binary_path = get_binary_path_for_abi(abi)
    subprocess.run(adb_cmd(sn, ['push', binary_path, DEVICE_PATH]), check=True)
    subprocess.run(adb_cmd(sn, ['shell', 'chmod', '755', DEVICE_PATH]), check=True)
    subprocess.run(adb_cmd(sn, ['shell', 'pkill', '-f', DEVICE_PATH]), check=False)
    args = ['shell', DEVICE_PATH]
    if test_mode:
        args.append('-t')
    args += ['-p', str(DEFAULT_PORT)]
    subprocess.Popen(adb_cmd(sn, args))
    subprocess.run(adb_cmd(sn, ['forward', f'tcp:{DEFAULT_PORT}', f'tcp:{DEFAULT_PORT}']), check=True)

def ensure_server_and_socket(sn=''):
    """Try to connect to the traceserver socket. If fails, push/start traceserver and retry."""
    try:
        return socket.create_connection(('127.0.0.1', DEFAULT_PORT), timeout=0.1)
    except Exception:
        push_and_start_server(sn)
        import time
        for _ in range(10):
            try:
                return socket.create_connection(('127.0.0.1', DEFAULT_PORT), timeout=0.1)
            except Exception:
                time.sleep(0.1)
        raise RuntimeError('Failed to connect to traceserver socket after starting server.')

def send_trace_command(cmd, tag, sn=''):
    """Send a trace command to the traceserver via a new socket connection."""
    with ensure_server_and_socket(sn) as s:
        s.sendall(f"{cmd}|{tag}\n".encode())

@server.tool()
def begin_trace(trace_tag: str, sn: str = ''):
    """
    Begin a trace section with the given tag name on the selected Android device.
    After calling this function, you should  call end_trace with the same tag name to end the trace section in the future.
    Args:
        trace_tag (str): Trace tag name.
        sn (str, optional): Device serial number. Defaults to ''.
    
    Returns:
        dict: Status and action information.
    """
    send_trace_command('begin', trace_tag, sn)
    return {'status': 'ok', 'action': 'begin', 'tag': trace_tag, 'sn': sn}

@server.tool()
def end_trace(trace_tag: str, sn: str = ''):
    """
    End a trace section with the given tag name on the selected Android device.
    Before calling this function, you should call begin_trace with the same tag name.
    Args:
        trace_tag (str): Trace tag name.
        sn (str, optional): Device serial number. Defaults to ''.
    
    Returns:
        dict: Status and action information.
    """
    send_trace_command('end', trace_tag, sn)
    return {'status': 'ok', 'action': 'end', 'tag': trace_tag, 'sn': sn}

@server.tool()
def trace_test_mode(sn: str = ''):
    """
    Start the traceserver in test mode (-t) on the selected Android device.
    
    Args:
        sn (str, optional): Device serial number. Defaults to ''.
    
    Returns:
        dict: Status and mode information.
    """
    push_and_start_server(sn, test_mode=True)
    return {"status": "ok", "mode": "test", "sn": sn}

@server.tool()
def stop_traceserver(sn: str = ''):
    """
    Stop the traceserver process and remove adb port forwarding.
    
    Args:
        sn (str, optional): Device serial number. Defaults to ''.
    
    Returns:
        dict: Status and action information.
    """
    subprocess.run(adb_cmd(sn, ['shell', 'pkill', '-f', DEVICE_PATH]), check=False)
    subprocess.run(adb_cmd(sn, ['forward', '--remove', f'tcp:{DEFAULT_PORT}']), check=False)
    return {"status": "ok", "action": "stop", "sn": sn}

def main():
    """Entry point for running the FASTMCP server with stdio transport."""
    server.run(transport='stdio')

if __name__ == "__main__":
    main()

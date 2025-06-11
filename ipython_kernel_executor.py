import logging
from typing import Any, Optional, Tuple, List
from contextlib import contextmanager
from jupyter_client import KernelManager


class IPythonKernelExecutor:
    def __init__(self):
        self.km = KernelManager()
        self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()

    def __call__(self, code):
        result_lines = []
        stdout_lines = []
        stderr_lines = []

        def handle_msg(msg):
            msg_type = msg['msg_type']

            if msg_type == 'execute_input':
                logging.debug('Code to IPython kernel executor: %r', msg['content']['code'])
            elif msg_type == 'execute_result':
                result_line = msg['content']['data']['text/plain']
                result_lines.append(result_line)
                logging.debug('Result from IPython kernel executor: %r', result_line)
            elif msg_type == 'stream' and msg['content']['name'] == 'stdout':
                stdout_line = msg['content']['text']
                stdout_lines.append(stdout_line)
                logging.debug('Stdout line from IPython kernel executor: %r', stdout_line)
            elif msg_type == 'stream' and msg['content']['name'] == 'stderr':
                stderr_line = msg['content']['text']
                stderr_lines.append(stderr_line)
                logging.debug('Stderr line from IPython kernel executor: %r', stderr_line)
            elif msg_type == 'error':
                traceback = msg['content']['traceback']
                stderr_lines.extend(traceback)
                logging.debug('Traceback from IPython kernel executor: %r', traceback)

        self.kc.execute_interactive(code, output_hook=handle_msg)
        return '\n'.join(result_lines), '\n'.join(stdout_lines), '\n'.join(stderr_lines)

    def shutdown(self):
        """Manually shut down the kernel."""
        self.kc.stop_channels()
        self.km.shutdown_kernel()

    def __enter__(self):
        """Allows the executor to be used in a `with` statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Automatically shuts down the kernel when exiting the `with` block."""
        self.shutdown()
# IPython Kernel Executor

A lightweight Python package to execute code in an isolated IPython kernel and capture results, stdout, and stderr.

Supports Python 2+.

## **Installation**

Make sure you have `jupyter-client` and `ipykernel` installed:

```bash
pip install jupyter-client ipykernel
```

Then, install this package:

```bash
pip install ipython-kernel-executor
```

## **Usage**

### **Basic Execution**

```python
from __future__ import print_function

from ipython_kernel_executor import IPythonKernelExecutor

with IPythonKernelExecutor() as executor:
    # Captures result
    result, stdout, stderr = executor("1 + 1")
    print(repr(result))  # '2'
    print(repr(stdout))  # ''
    print(repr(stderr))  # ''

    # Captures stdout
    result, stdout, stderr = executor("print('Hello, World!')")
    print(repr(result))  # ''
    print(repr(stdout))  # 'Hello, World!\n'
    print(repr(stderr))  # ''

    # Captures stderr
    result, stdout, stderr = executor("1 / 0")
    print(repr(result))  # ''
    print(repr(stdout))  # ''
    print(repr(stderr))  # contains 'ZeroDivisionError'
```

### **Manual Shutdown (Optional)**

If not using `with`, manually shut down the kernel:

```python
executor = IPythonKernelExecutor()
result, stdout, stderr = executor("2 * 3")
executor.shutdown()  # Clean up
```

## Contributing

Contributions are welcome!  Please submit pull requests or open issues on GitHub.

## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.
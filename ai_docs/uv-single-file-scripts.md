# 使用UV运行脚本

Python脚本是用于独立执行的文件，例如使用`python <script>.py`。使用uv执行脚本确保脚本依赖被管理，而无需手动管理环境。

## 运行无依赖的脚本

如果您的脚本没有依赖，您可以使用`uv run`执行它：

```python
# example.py
print("Hello world")
```

```bash
$ uv run example.py
Hello world
```

同样，如果您的脚本依赖于标准库中的模块，则无需做更多事情。

可以向脚本提供参数：

```python
# example.py
import sys
print(" ".join(sys.argv[1:]))
```

```bash
$ uv run example.py test
test

$ uv run example.py hello world!
hello world!
```

此外，您的脚本可以直接从stdin读取。

请注意，如果您在_项目_中使用`uv run`，即带有`pyproject.toml`的目录，它将在运行脚本之前安装当前项目。如果您的脚本不依赖于项目，请使用`--no-project`标志跳过此操作：

```bash
$ # 注意：`--no-project`标志必须在脚本名称_之前_提供。
$ uv run --no-project example.py
```

## 运行有依赖的脚本

当您的脚本需要其他包时，它们必须安装到脚本运行的环境中。使用`--with`选项请求依赖：

```bash
$ uv run --with rich example.py
```

如果需要特定版本，可以向请求的依赖添加约束：

```bash
$ uv run --with 'rich>12,<13' example.py
```

可以通过重复使用`--with`选项来请求多个依赖。

## 创建Python脚本

Python最近添加了内联脚本元数据的标准格式。它允许选择Python版本和定义依赖。使用`uv init --script`初始化带有内联元数据的脚本：

```bash
$ uv init --script example.py --python 3.12
```

## 声明脚本依赖

内联元数据格式允许在脚本本身中声明脚本的依赖。使用`uv add --script`为脚本声明依赖：

```bash
$ uv add --script example.py 'requests<3' 'rich'
```

这将在脚本顶部添加一个`script`部分，使用TOML声明依赖：

```python
# /// script
# dependencies = [\
#   "requests<3",\
#   "rich",\
# ]
# ///

import requests
from rich.pretty import pprint

resp = requests.get("https://peps.python.org/api/peps.json")
data = resp.json()
pprint([(k, v["title"]) for k, v in data.items()][:10])
```

uv将自动创建一个包含运行脚本所需依赖的环境。

## 使用shebang创建可执行文件

可以添加shebang使脚本在不使用`uv run`的情况下可执行：

```python
#!/usr/bin/env -S uv run --script

print("Hello, world!")
```

确保您的脚本是可执行的，例如使用`chmod +x greet`，然后运行脚本。

## 使用替代包索引

如果您希望使用替代包索引来解析依赖，可以使用`--index`选项提供索引：

```bash
$ uv add --index "https://example.com/simple" --script example.py 'requests<3' 'rich'
```

## 锁定依赖

uv支持使用`uv.lock`文件格式锁定PEP 723脚本的依赖：

```bash
$ uv lock --script example.py
```

运行`uv lock --script`将在脚本旁边创建一个`.lock`文件（例如，`example.py.lock`）。

## 提高可重现性

除了锁定依赖之外，uv在内联脚本元数据的`tool.uv`部分支持`exclude-newer`字段，以限制uv仅考虑在特定日期之前发布的分发版：

```python
# /// script
# dependencies = [\
#   "requests",\
# ]
# [tool.uv]
# exclude-newer = "2023-10-16T00:00:00Z"
# ///
```

## 使用不同的Python版本

uv允许在每次脚本调用时请求任意Python版本：

```bash
$ # 使用特定的Python版本
$ uv run --python 3.10 example.py
```

## 使用GUI脚本

在Windows上，`uv`将使用`pythonw`运行以`.pyw`扩展名结尾的脚本。
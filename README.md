# curve_toolkits
曲线分析小工具集


### 下载子模块（SDK）
``` bash
git submodule init
git submodule update
```

### 打包分发

> 打包后可分发的文件会放置在dist/${应用名称}文件夹中

1. 安装pyinstaller
``` bash
pip install pyinstaller -i https://pypi.douban.com/simple
```

2. 打包
``` bash
pyinstaller toolkit.spec
```

```shell
pyuic5 ./ui/toolkit.ui -o ./ui/toolkit.py
```
# firework

### 使用方法
- 安装python
- 安装cv2依赖
    ```bash
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python
    ```
- 进入项目根目录，运行firework.py
- 设置运行参数
    - 执行次数
    - 设置截图缩放比例
    - 选择点击次数
- 图片加载出来时点击选择表情和发送按钮位置(按esc键确认)
### exe文件打包
```bash
pyinstaller -F fireWork.spec
```
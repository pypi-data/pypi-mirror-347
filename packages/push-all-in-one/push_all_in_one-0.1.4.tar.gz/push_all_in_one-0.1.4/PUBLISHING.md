# 发布指南

本文档提供了如何发布`push-all-in-one`包到PyPI的详细说明。

## 准备工作

1. 确保你有PyPI账号
2. 安装必要的工具：
   ```bash
   pip install build twine
   ```
3. 创建PyPI API令牌：
   - 登录到 [PyPI](https://pypi.org/)
   - 点击右上角的用户名，然后选择"Account settings"
   - 滚动到"API tokens"部分，点击"Add API token"
   - 设置令牌的名称和权限（通常选择特定项目的权限更安全）
   - 复制生成的令牌（注意：令牌只会显示一次）

4. 配置认证（两种方式）：
   - 在`~/.pypirc`文件中设置：
     ```
     [distutils]
     index-servers =
         pypi
         testpypi
     
     [pypi]
     username = __token__
     password = pypi-AgEIcHlwaS5vcmc...  # 你的API令牌
     
     [testpypi]
     repository = https://test.pypi.org/legacy/
     username = __token__
     password = pypi-AgEIcHlwaS5vcmc...  # 你的TestPyPI API令牌
     ```
   - 或使用环境变量（推荐）：
     ```bash
     export TWINE_USERNAME=__token__
     export TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmc...  # 你的API令牌
     ```

## 版本更新步骤

1. 更新版本号
   - 修改`pyproject.toml`中的`version`
   - 修改`setup.py`中的`version`
   - 修改`__init__.py`中的`__version__`

2. 添加更新日志
   - 在`CHANGELOG.md`中记录新版本的变更内容

3. 清理旧的构建文件
   ```bash
   rm -rf build/ dist/ *.egg-info/
   ```

## 构建包

```bash
python -m build
```

这将在`dist/`目录下生成源代码分发包(`.tar.gz`)和轮子文件(`.whl`)。

## 测试发布到TestPyPI（可选但推荐）

```bash
twine upload --repository testpypi dist/*
```

然后测试安装：

```bash
pip install --index-url https://test.pypi.org/simple/ push-all-in-one
```

## 正式发布到PyPI

```bash
twine upload dist/*
```

## 使用GitHub Actions自动发布

本项目配置了GitHub Actions工作流，可以自动发布包到PyPI。

### 配置GitHub密钥

1. 在GitHub仓库页面，进入`Settings` -> `Secrets and variables` -> `Actions`
2. 添加一个密钥：
   - `PYPI_API_TOKEN`：PyPI API令牌

### 触发自动发布

有两种方式触发发布：

1. 创建新的GitHub Release：
   - 在GitHub仓库页面，点击`Releases` -> `Create a new release`
   - 填写版本号、标题和描述
   - 发布release后，GitHub Actions将自动构建并发布包

2. 手动触发工作流：
   - 在GitHub仓库页面，点击`Actions` -> `Publish Python Package`
   - 点击`Run workflow`按钮，并选择要部署的分支

## 发布后验证

```bash
# 卸载旧版本（如果已安装）
pip uninstall -y push-all-in-one

# 安装新版本
pip install push-all-in-one

# 验证版本号
python -c "import push_all_in_one; print(push_all_in_one.__version__)"
``` 
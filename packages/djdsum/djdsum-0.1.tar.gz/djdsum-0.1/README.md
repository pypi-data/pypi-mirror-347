
## 打包
```sh
pip install setuptools wheel
python setup.py sdist bdist_wheel
```

## 安装
```sh
pip install twine
```
## 上传
```sh
twine upload dist/*
```


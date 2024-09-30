## 手順
{cwd}: このリポジトリのディレクトリ
```sh
# venv
$ python -m venv venv
$ source ./venv/bin/activate

# dp_numpyのセットアップ
$ cd {cwd}
$ git clone git@github.com:secure-privacy-project/dp_numpy.git
$ cd dp_numpy
$ git checkout feature/dp_pandas
$ pip install -e .

# dp_numpyを内部的に使うpandasのセットアップ
$ cd {cwd}
$ git clone git@github.com:secure-privacy-project/pandas.git
$ cd pandas
$ git checkout feature/dp
$ pip install .

# 実行
$ cd {cwd}
$ pip install streamlit
$ streamlit run streamlit_app.py

# http://localhost:8501/にアクセス
# data/data_small.csvをアップロード
```

git clone https://gitee.com/zjchenchujie/VisualGLM-6B.git
cd ./VisualGLM-6B/
python -m venv venv
call .\vnev\Scripts\activate.bat
pip install -r requirements_wo_ds.txt
pip install -i https://mirrors.aliyun.com/pypi/simple/ --no-deps "SwissArmyTransformer>=0.4.4"
python.exe web_demo.py

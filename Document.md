# IntelliFusion使用教程

## 基础教程
### 使用模型
- 添加模型
  1. 选择模型类型
  2. 施工中

- 运行模型
  1. 输入**正确的**启动编译器路径及启动文件路径.
  2. 点击"运行"按钮.
  3. 等待启动成功.
  - **注意**
    1. 如果启动失败，原因为超时，请检查你的启动编译器和文件及其路径是否存在或者是否有效.
    2. 如果你确定启动编译器和文件及其路径均为有效且正确，可以在**设置-基础设置-启动超时**设置更长的时间(单位为秒).
    3. 如果没有启动不需要编译器，请在编译器文件输入" "(space键).

### 小组件(Widgets)
- 添加小组件
  1. 施工中

- 编辑小组件
  1. 施工中

- 排序小组件
  - 拖动小组件即可排序

## 开发教程

### 小组件开发
- 内置函数
  1. `Create_Session()`
    - 需要参数:
      1. `comment`  类型 `string`
      2. `model_id` 类型 `int`
    - 先要调用`Create_Session()`函数,需要填入两个参数，分别是`comment`和`model_id`，
    - 返回值:
      1. `SessionID` 类型 `int`
    - **注意**:当你在编写时，你需要获取其返回值，将这个值填入`request_OpenAI()`&`request_Json()`的第一个参数`Session_ID`中.
  2. `request_OpenAI()`
    - 需要参数:
      1. `Session_ID` 类型 `int`
      2. `Userinput`  类型 `string`
      3. `stream`     类型 `bool`
    - 输入`Userinput`,`stream`,当`stream`为`True`时，需要使用下列代码返回HTML:
      ```python
      result = request_OpenAI(SessionID=,Userinput=,stream=True)
      for r in result:
        yield r
      ```
      但当`stream`为`False`时，你只需要
      ```python
      result = request_OpenAI(SessionID=,Userinput=,stream=True)
      return result
      ```
    - 返回值:
      1. `response` 类型 `string`
  3. `request_Json`
    - 需要参数:
      1. `Session_ID` 类型 `int`
      2. `Userinput`  类型 `string`
    - 返回值:
      1. `response` 类型 `string`
  - 内置接口
    1.  `/GetModelList`
      - 输入值: ` `
      - 输出值：
        ```python
          [{
            'id': 1,
            'api_key': 'api_key',
            'launch_compiler': '/',
            'launch_path': '/',
            'name': 'gpt-3.5-turbo',
            'type': 'OpenAI',
            'url': 'https://api.example.com/v1'
            }]
        ```
    2. `/GetActiveModel`
      - 输入值: ` `
      - 输出值: 
        ```python
          [{
            'id': 1,
            'api_key': 'api_key',
            'launch_compiler': '/',
            'launch_path': '/',
            'name': 'gpt-3.5-turbo',
            'type': 'OpenAI',
            'url': 'https://api.example.com/v1'
            }]
        ```
      - **注意**: 当用户开启`ActiveExamin`时，`/GetActiveModel`将返回所以模型数据。
    3. `/GetHistory`
      - 输入值: `session_id`
      - 输出值: 
        ```python
          [{
            'id': 1,
            'session_id': '1',
            'Userinput': '/',
            'response': '/'
            },
            {
            'id': 1,
            'session_id': '1',
            'Userinput': '/',
            'response': '/'
            },
            {
            'id': 1,
            'session_id': '1',
            'Userinput': '/',
            'response': '/'
            },]
        ```
    4. 

- 编写小组件:
  1. 使用`html`/`js`/`css`/`python flask`蓝图编写微应用
  2. 替换内容
    1. `html`文件存放在`./widgets/templates/`下
    2. `css`文件存放在`./widgets/static/css/`下
    3. `javascripts`脚本存放在`./widgets/static/js/`下
    4. 打开`./widgets/views.py`，按照下列格式添加内容(添加路由):
    ```python
    @app.route('/your_widgets_url')
    def your_widgets_name():
        return render_templates("your_html_file.html")
    ```
    将以上代码中的部分内容替换为您自己的内容：
    | 代码中的内容        | 你需要输入的内容      |
    |---------------------|-----------------------|
    | /your_widgets_url   | 你的小组件地址        |
    | your_widgets_name   | 你的小组件名称        |
    | your_html_file.html | 你的html文件名称.html |


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
- 编写小组件:
  1. 使用html/js/css/python flask蓝图编写微应用
  2. 替换内容
    1. html文件存放在./widgets/templates/下
    2. css文件存放在./widgets/static/css/下
    3. javascripts脚本存放在./widgets/static/js/下
    4. 打开./widgets/views.py，按照下列格式添加内容(添加路由):
    ```
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


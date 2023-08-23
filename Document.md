# IntelliFusion使用教程

## 基础教程



## 开发教程

### 小组件开发
- 编写小组件:
  1. 使用html/js/css/python flask蓝图编写微应用
  2. 替换内容
    1. html文件存放在./widgets/templates/下
    2. css文件存放在./widgets/static/css/下
    3. javascripts脚本存放在./widgets/static/js/下
    4. 打开./widgets/views.py，按照下列格式添加内容:
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


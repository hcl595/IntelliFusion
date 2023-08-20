# intelliFusion

## 介绍

intelliFusion是一个开源的、高自由度、支持多种模型库的AI模型库的使用平台。为方便不通用库的使用，我们拥有用户可自行导入不同的模型库。
intelliFusion 运用flask处理后端，webui处理前端。使用echarts，可以让用户自行更改，添加小组件；使用Ajax，异步获取数据，使用echarts进行了数据可视化，使用户可以根据自己电脑的硬件使用率，自行规划使用率。

## 支持模型

**通过webui调用的语言模型**
- 支持所有带有原生界面的模型

**通过api调用的语言模型**
- [ChatGPT](https://chat.openai.com) ([GPT-4](https://openai.com/product/gpt-4))

**本地部署语言模型**
- [ChatGLM](https://github.com/THUDM/ChatGLM-6B) ([ChatGLM2](https://github.com/THUDM/ChatGLM2-6B))

## 更新信息

**[2023/08/05]** 发布[intelliFusion](https://github.com/hcl595/IntelliFusion),intelliFusion 的升级版本，在保留了之前带有的功能的基础之上，intelliFusion 引入了如下新特性：

1. **更好的体验**：修复了之前出现的bug
2. **优化小组件**：新增内置GPU占用监测
3. **更好的背景**：添加了深浅模式切换按钮，可以按照用户需求切换背景色
4. **更好的对胡**：提示词可更换语言（目前仅支持日语和中文）
5. **优化底层代码**：使用ajax，代替jinjia2和form表单

----
**[2023/08/01]** 发布[intelliFusion](https://github.com/hcl595/IntelliFusion),intelliFusion 的升级版本，在保留了之前带有的功能的基础之上，intelliFusion 引入了如下新特性：

1. **优化小组件**：我们优化了小插件的显示，更新了一部分的内容.
2. **更好的优化**：修复了bug.
3. **更好的调用**：添加了活跃检测，实时监测您所启用的模型，可以只调用在线模型.
4. **更好的沟通**：内置多语言提示词库，拥有提示词框，可以辅助您更方便的调用模型.

----
**[2023/07/29]** 发布[intelliFusion](https://github.com/hcl595/IntelliFusion),intelliFusion 的升级版本，在保留了之前带有的功能的基础之上，intelliFusion 引入了如下新特性：

1. **更方便的使用**：基于上一个版本的内测反应情况，我们全面升级了 intelliFusion 的基础功能。使用户可以在账户界面控制模型的开启与关闭
2. **更流畅的沟通**：我们改善了用户与ai交流之间的延迟

----
**[2023/06/23]** 发布[intelliFusion](https://github.com/hcl595/IntelliFusion)

## 了解更多



- [想反馈问题？]开发者邮箱：3545742020@qq.com
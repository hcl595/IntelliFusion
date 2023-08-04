# 变量.
>Model => 所有模型 按order由小到大排列.
>TimeOut => 最大等待时间.
>host => 本地加载地址.
>port => 本地加载端口.
>mode => 网页模式/客户端模型.
>BugM => DeBug模式.

> #### 链接.
> - /openai => openai插件调用接口.
>>userinput = 用户输入.
>>modelinput = 模型 --> 需对应数据库中的模型名称.
>
> - /llm => 普通api调用接口.
>>userinput = 用户输入.
>>modelinput = 模型 --> 需对应数据库中的模型名称 .
>
> - /exchange => 模型列表更改.
>   - state => 将进行的操作.
>       - run => 运行.
>       - stop => 关闭运行.
>       - edit => 编辑.
>       - del => 删除.
>       - add => 添加.
>   - number => 需进行操作的模型编号(Model.id).
>   - comment => 模型名称.
>   - type => 类型 { Openai/API/WebUI }.
>   - url => 访问地址.
>   - APIKEY => API密钥.
>   - LcCompiler => 启动所使用的编译器地址.
>   - LcUrl => 启动所使用的文件地址 **建议修改为LcPath**

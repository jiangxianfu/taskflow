# Task Flow

## 工具定位：

1. 一个可以敏捷定制化的流程任务工具
2. 用户只需要关注自己需要实现的模块
3. 支持流程中的任务进行重试，延迟执行，callback回调，任务跳过，任务终止
4. 具有任务执行分布式处理提高任务处理容量
5. 添加新模块不需要重启即可生效
6. 源代码极简模式，前端与后端分开管理没有依赖 (前端甚至可以没有)

## 功能列表:

1. 定时任务调度
   > 执行任务流程
   > 执行单步任务
2. 单步任务执行
   > 失败重试
3. 流程任务执行
    > 任务中断
    > 失败重试
    > 延迟执行


## 举个例子：

有一家互联网公司，需要上线一批服务器，为了完成自动化上线的功能，需要以下几个步骤：
1. CMS信息更新
2. 安装系统
3. 格式化数据盘
4. 配置系统环境
5. 安装应用环境
6. 服务器上线

以上6步骤,可以轻松按照模块来进行定义输入参数并实现代码

模块接入：

	为了敏捷和通用性，可以根据自己的需求快速的定制自己的模块,
	模块的规范特别简单,
	只需要在modules 文件夹中创建自己的模块脚本（以action_ 或check_开头）。

模块规范：

1. 必须有main() 函数

2. main函数返回值

	> 情况一：没有返回

	> 情况二：bool类型

	> 情况三：tuple类型 bool,message 

	> 情况四：tuple类型 bool,message,data 注:data必须是字典类型

主要的服务说明:

1. 待运行实例扫描服务(task_producer.py)   

2. 任务发送服务(task_consumer.py)   

3. 扩展接口服务(web_server.py)

主要的运行模块说明(task_run.py):

	它是整个架构中最重要的部分，也是最核心的部分；
	它负责整理流程步骤的顺序执行，加载并运行模块；
	同时整合模块参数输入，输出，模块数据的保存工作。
	这个模块如果在应急情况下也可以单独手工运行
	手工运行方法: task_run.py -i <task_flow_id>

测试模块脚本(test_module.py)

	这个脚本主要用于单独调试模板的脚本的;
	但是跑的主函数是test_main 并且参数不是自动适配数据的;
	需要自己填充已用于测试。
	使用方法: test_module.py -m <module_name>

运行流程图：

![image](https://github.com/jiangxianfu/smarttaskflow/blob/master/docs/architecture.png)


运行模块的关键程序instance表数据更新逻辑:

![image](https://github.com/jiangxianfu/smarttaskflow/blob/master/docs/task_run_flow.png)


单元测试使用的是pytest:

```
python -m unittest -v

```


数据示例:

![image](https://github.com/jiangxianfu/smarttaskflow/blob/master/docs/index.png)

![image](https://github.com/jiangxianfu/smarttaskflow/blob/master/docs/modules.png)

![image](https://github.com/jiangxianfu/smarttaskflow/blob/master/docs/flows.png)

![image](https://github.com/jiangxianfu/smarttaskflow/blob/master/docs/flow_steps.png)

![image](https://github.com/jiangxianfu/smarttaskflow/blob/master/docs/instances.png)

![image](https://github.com/jiangxianfu/smarttaskflow/blob/master/docs/instance_steps.png)


# workflow 说明

## Workflow Model

|attribute         |required   |description
|------------------|-----------|-------------
|description       |no         |描述
|begin_step        |yes        |用于开始的名称(step_name)
|end_step          |yes        |用于接受的名称(step_name)
|steps             |yes        |A dictionary of steps that defines the intent of this workflow.(dict)


## Step Model

|attribute         |required   |description                               
|------------------|-----------|------------------------------------------
|module            |yes        |具体执行的模块名称(action_xxx,check_xxx)  
|parameters        |yes        |模块对应的参数(dict)                      
|on-success        |yes        |执行成功后要执行的(step_name)             
|on-failure        |no         |执行失败后要执行的(step_name)             
|on-success-pause  |no         |如果成功后暂停整个流程(bool)              
|on-failure-retry  |no         |如果失败后可以重试次数(int)               

# module说明

模块主要以action_和check_开头的文件两种类型.

两种类型只有情况一的区别，其他都一样

## action_xxx(任务类型)

action: 允许使用4中类型(以下)

> 情况一：没有返回 **这种情况算执行成功**

> 情况二：bool类型

> 情况三：tuple类型 bool,message 

> 情况四：tuple类型 bool,message,data 注:data必须是字典类型


## check_xxx (轮询验证类型)

主要解决通过检测脚本执行情况为判断依据验证任务是否成功

check: 允许使用4种返回值：

> 情况一：没有返回 **说明还没有正式结果(这种情况会进行下次轮询检测验证)**

> 情况二：bool类型

> 情况三：tuple类型 bool,message

> 情况四：tuple类型 bool,message,data 注:data必须是字典类型

**特殊参数**:

check_interval: 用于定义check的重试周期(int,默认:300秒)
  
check_maxcount: 用于定义check的最大次数(int,默认0:不限制)

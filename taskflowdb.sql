--创建数据库
CREATE DATABASE taskflowdb;

USE taskflowdb;

-- 模块表：用于定义创建的模块信息
CREATE TABLE `modules` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `name` varchar(128) NOT NULL COMMENT '模块名称即对应的脚本文件名称(去除后缀)',
   `description` varchar(255) NOT NULL COMMENT '描述信息',
   `arguments` json NOT NULL COMMENT '参数定义[{"name":"id","type":"simple","description":"ip信息"},"name":"sm","type":"object","description":"对象类型"}] 目前参数只支持 object(list set tuple dict),simple(number string)',
   `creator` varchar(45) NOT NULL COMMENT '创建人',
   `createdtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
   `updator` varchar(45) NOT NULL COMMENT '更新者',
   `modifiedtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
   PRIMARY KEY (`id`),
   UNIQUE KEY `udx_module` (`name`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='模块定义表';
-- 流程表：用于定义流程信息
CREATE TABLE `flows` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `name` varchar(45) NOT NULL COMMENT '流程名称',
   `description` varchar(255) NOT NULL COMMENT '流程描述',
   `entry_arguments` json NOT NULL COMMENT '入口参数定义参数定义[{"name":"id","type":"simple","description":"ip信息"},"name":"sm","type":"object","description":"对象类型"}] 目前参数只支持 object(list set tuple dict),simple(number string)',
   `stepcount` int(11) NOT NULL COMMENT '步骤数',
   `creator` varchar(45) NOT NULL COMMENT '创建者',
   `createdtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
   `updator` varchar(45) NOT NULL COMMENT '更新者',
   `modifiedtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
   PRIMARY KEY (`id`),
   UNIQUE KEY `udx_flow` (`name`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='流程定义表';

-- 流程步骤表：用于定义流程步骤的功能
CREATE TABLE `flow_steps` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `flowid` int(11) NOT NULL COMMENT '所属流程',
   `modulename` varchar(128) NOT NULL COMMENT '所属模块名称',
   `inputargalias` json NOT NULL COMMENT '输入参数别名,解决模块间参数重名的问题 {"模块输入参数名称":"自定义模块参数名称别名防止冲突"}如:{"id":"id_as"}',
   `outputargalias` json NOT NULL COMMENT '输出参数别名,解决模块间参数重名的问题 {"模块输出参数名称":"自定义模块参数名称别名防止冲突"}如:{"id":"id_as"}',
   `stepnum` int(11) NOT NULL COMMENT '步骤序号 必须1开始并且连续',
   `stepname` varchar(45) NOT NULL COMMENT '步骤名称',
   `stepdescription` varchar(255) NOT NULL COMMENT '步骤描述',
   `failed_retrycounts` int(11) NOT NULL DEFAULT '0' COMMENT '失败重试次数(0:不重试)',
   `nextstep_waitseconds` int(11) NOT NULL DEFAULT '0' COMMENT '等待一定时间后自动继续下一个步骤执行(-1:暂停,0:不等待,>0:等待秒数)',
   `creator` varchar(45) NOT NULL COMMENT '创建者',
   `createdtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
   `updator` varchar(45) NOT NULL COMMENT '更新者',
   `modifiedtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
   PRIMARY KEY (`id`),
   UNIQUE KEY `udx_stepnum` (`flowid`,`stepnum`) /*!80000 INVISIBLE */
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='流程明细步骤';

-- 实例信息：真正运行的实例信息主表
CREATE TABLE `instances` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `title` varchar(128) NOT NULL COMMENT '主题',
   `description` varchar(255) NOT NULL COMMENT '描述',
   `flowid` int(11) NOT NULL COMMENT '对应的flowid',
   `arguments` json NOT NULL COMMENT '入口参数数据',
   `stepcount` int(11) NOT NULL COMMENT '实例对应的步骤数量',
   `curstepnum` int(11) NOT NULL DEFAULT '1' COMMENT '当前步骤',
   `curstepruncount` int(11) NOT NULL DEFAULT '0' COMMENT '当前步骤执行次数',
   `nextruntime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '下次运行时间',
   `status` varchar(10) NOT NULL COMMENT '状态(''init'',''standby'',''running''，''pause'',''fail'',''success'')',
   `creator` varchar(45) NOT NULL COMMENT '创建者',
   `createdtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
   `updator` varchar(45) NOT NULL COMMENT '更新者',
   `modifiedtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
   PRIMARY KEY (`id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='工作流实例';


-- 实例步骤表：记录当时实例运行的步骤信息及执行的参数与输出结果信息
CREATE TABLE `instance_steps` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `instanceid` int(11) DEFAULT NULL COMMENT '实例id',
   `stepnum` int(11) DEFAULT NULL COMMENT '步骤序号',
   `stepname` varchar(128) DEFAULT NULL COMMENT '步骤名称',
   `arguments` json DEFAULT NULL COMMENT '调用参数信息',
   `workername` varchar(45) DEFAULT NULL COMMENT '工作机名称',
   `status` varchar(10) DEFAULT NULL COMMENT '状态消息',
   `message` varchar(5000) DEFAULT NULL,
   `createdtime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
   `modifiedtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
   PRIMARY KEY (`id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='流程运行步骤信息';


-- 实例运行数据表：用于串接步骤间的数据关系，类似内存数据，这样可以更好的交换步骤间的数据输入与输出信息，目前支持int,str,json类型
CREATE TABLE `instance_rundata` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `instanceid` int(11) NOT NULL COMMENT '实例id',
   `keyname` varchar(128) NOT NULL COMMENT 'keyname',
   `keyvalue` varchar(2000) NOT NULL COMMENT 'key值',
   `keytype` varchar(45) NOT NULL COMMENT 'key类型(目前参数只支持 object(list set tuple dict),simple(number string))',
   `createdtime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
   PRIMARY KEY (`id`),
   UNIQUE KEY `udx_key` (`instanceid`,`keyname`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='实例运行中的数据';


#-------------------init sample data-------------------------------------------------

INSERT INTO `taskflowdb`.`modules` (`name`,`description`,`arguments`,`creator`,`updator`) VALUES ('install_os','安装操作系统','[{\"name\": \"os\", \"type\": \"simple\", \"description\": \"操作系统\"}, {\"name\": \"machine_name\", \"type\": \"simple\", \"description\": \"machine\"}, {\"name\": \"cpu_num\", \"type\": \"simple\", \"description\": \"cpu core num\"}, {\"name\": \"mem_gb\", \"type\": \"simple\", \"description\": \"memory size gb\"}, {\"name\": \"disk_gb\", \"type\": \"simple\", \"description\": \"disk size gb\"}]','steven','steven');
INSERT INTO `taskflowdb`.`modules` (`name`,`description`,`arguments`,`creator`,`updator`) VALUES ('init_os','初始化操作系统基础数据','[{\"name\": \"user\", \"type\": \"simple\", \"description\": \"连接服务器账号\"}, {\"name\": \"password\", \"type\": \"simple\", \"description\": \"连接服务器密码\"}, {\"name\": \"machine_name\", \"type\": \"simple\", \"description\": \"机器名称\"}, {\"name\": \"ip\", \"type\": \"simple\", \"description\": \"ip\"}, {\"name\": \"port\", \"type\": \"simple\", \"description\": \"port\"}]','steven','steven');
INSERT INTO `taskflowdb`.`modules` (`name`,`description`,`arguments`,`creator`,`updator`) VALUES ('notice','通知用户email','[]','steven','steven');
INSERT INTO `taskflowdb`.`modules` (`name`,`description`,`arguments`,`creator`,`updator`) VALUES ('demo','测试例子','[{\"name\": \"id\", \"type\": \"simple\", \"description\": \"测试id\"}]','steven','steven');


INSERT INTO `taskflowdb`.`flows` (`name`,`description`,`entry_arguments`,`stepcount`,`creator`,`updator`) VALUES ('install_server_flow','测试服务器上线流程','[{\"name\": \"os\", \"type\": \"simple\", \"description\": \"操作系统\"}, {\"name\": \"machine_name\", \"type\": \"simple\", \"description\": \"machine\"}, {\"name\": \"cpu_num\", \"type\": \"simple\", \"description\": \"cpu core num\"}, {\"name\": \"mem_gb\", \"type\": \"simple\", \"description\": \"memory size gb\"}, {\"name\": \"disk_gb\", \"type\": \"simple\", \"description\": \"disk size gb\"}]',3,'steven','steven');


INSERT INTO `taskflowdb`.`flow_steps` (`flowid`,`modulename`,`inputargalias`,`outputargalias`,`stepnum`,`stepname`,`stepdescription`,`failed_retrycounts`,`nextstep_waitseconds`,`creator`,`updator`) VALUES (1,'install_os','{}','{\"passwd\": \"password\"}',1,'安装操作系统','安装操作系统',-1,0,'steven','steven');
INSERT INTO `taskflowdb`.`flow_steps` (`flowid`,`modulename`,`inputargalias`,`outputargalias`,`stepnum`,`stepname`,`stepdescription`,`failed_retrycounts`,`nextstep_waitseconds`,`creator`,`updator`) VALUES (1,'init_os','{}','{}',2,'初始化配置信息','初始化配置信息',0,30,'steven','steven');
INSERT INTO `taskflowdb`.`flow_steps` (`flowid`,`modulename`,`inputargalias`,`outputargalias`,`stepnum`,`stepname`,`stepdescription`,`failed_retrycounts`,`nextstep_waitseconds`,`creator`,`updator`) VALUES (1,'notice','{}','{}',3,'通知','通知完成',3,0,'steven','steven');

INSERT INTO `taskflowdb`.`instances` (`title`,`description`,`flowid`,`arguments`,`stepcount`,`curstepnum`,`status`,`creator`,`updator`) VALUES ('VMS001上线','测试流程',1,'{\"os\": \"centos 8.0\", \"mem_gb\": 24, \"cpu_num\": 8, \"disk_gb\": 100, \"machine_name\": \"VMS001\"}',3,1,'init','steven','steven');



# 以下数据可以导入，也可以不导入都是测试数据结果参考的
INSERT INTO `taskflowdb`.`instance_rundata` (`id`,`instanceid`,`keyname`,`keyvalue`,`keytype`,`createdtime`) VALUES (1,1,'ip','127.0.0.1','simple','2020-02-22 15:04:04');
INSERT INTO `taskflowdb`.`instance_rundata` (`id`,`instanceid`,`keyname`,`keyvalue`,`keytype`,`createdtime`) VALUES (2,1,'port','22','simple','2020-02-22 15:04:04');
INSERT INTO `taskflowdb`.`instance_rundata` (`id`,`instanceid`,`keyname`,`keyvalue`,`keytype`,`createdtime`) VALUES (3,1,'user','op','simple','2020-02-22 15:04:04');
INSERT INTO `taskflowdb`.`instance_rundata` (`id`,`instanceid`,`keyname`,`keyvalue`,`keytype`,`createdtime`) VALUES (8,1,'password','test','simple','2020-02-22 15:15:02');


INSERT INTO `taskflowdb`.`instance_steps` (`id`,`instanceid`,`stepnum`,`stepname`,`arguments`,`workername`,`status`,`message`,`createdtime`,`modifiedtime`) VALUES (1,1,1,'安装操作系统','{\"os\": \"centos 8.0\", \"mem_gb\": 24, \"cpu_num\": 8, \"disk_gb\": 100, \"machine_name\": \"VMS001\", \"sys_taskflow_instance\": {\"id\": 1, \"title\": \"VMS001上线\", \"flowid\": 1, \"status\": \"init\", \"creator\": \"steven\", \"updator\": \"steven\", \"arguments\": \"{\\\"os\\\": \\\"centos 8.0\\\", \\\"mem_gb\\\": 24, \\\"cpu_num\\\": 8, \\\"disk_gb\\\": 100, \\\"machine_name\\\": \\\"VMS001\\\"}\", \"stepcount\": 3, \"curstepnum\": 1, \"createdtime\": \"2020-02-22 13:27:44\", \"description\": \"测试流程\", \"nextruntime\": \"2020-02-22 13:27:44\", \"modifiedtime\": \"2020-02-22 14:32:12\", \"curstepruncount\": 0}}','DESKTOP-STEVEN','fail','\'id\'','2020-02-22 15:01:07','2020-02-22 15:31:23');
INSERT INTO `taskflowdb`.`instance_steps` (`id`,`instanceid`,`stepnum`,`stepname`,`arguments`,`workername`,`status`,`message`,`createdtime`,`modifiedtime`) VALUES (2,1,1,'安装操作系统','{\"os\": \"centos 8.0\", \"mem_gb\": 24, \"cpu_num\": 8, \"disk_gb\": 100, \"machine_name\": \"VMS001\", \"sys_taskflow_instance\": {\"id\": 1, \"title\": \"VMS001上线\", \"flowid\": 1, \"status\": \"standby\", \"creator\": \"steven\", \"updator\": \"steven\", \"arguments\": \"{\\\"os\\\": \\\"centos 8.0\\\", \\\"mem_gb\\\": 24, \\\"cpu_num\\\": 8, \\\"disk_gb\\\": 100, \\\"machine_name\\\": \\\"VMS001\\\"}\", \"stepcount\": 3, \"curstepnum\": 1, \"createdtime\": \"2020-02-22 13:27:44\", \"description\": \"测试流程\", \"nextruntime\": \"2020-02-22 13:27:44\", \"modifiedtime\": \"2020-02-22 15:02:46\", \"curstepruncount\": 1}}','DESKTOP-STEVEN','fail','\'id\'','2020-02-22 15:03:19','2020-02-22 15:31:23');
INSERT INTO `taskflowdb`.`instance_steps` (`id`,`instanceid`,`stepnum`,`stepname`,`arguments`,`workername`,`status`,`message`,`createdtime`,`modifiedtime`) VALUES (3,1,1,'安装操作系统','{\"os\": \"centos 8.0\", \"mem_gb\": 24, \"cpu_num\": 8, \"disk_gb\": 100, \"machine_name\": \"VMS001\", \"sys_taskflow_instance\": {\"id\": 1, \"title\": \"VMS001上线\", \"flowid\": 1, \"status\": \"standby\", \"creator\": \"steven\", \"updator\": \"steven\", \"arguments\": \"{\\\"os\\\": \\\"centos 8.0\\\", \\\"mem_gb\\\": 24, \\\"cpu_num\\\": 8, \\\"disk_gb\\\": 100, \\\"machine_name\\\": \\\"VMS001\\\"}\", \"stepcount\": 3, \"curstepnum\": 1, \"createdtime\": \"2020-02-22 13:27:44\", \"description\": \"测试流程\", \"nextruntime\": \"2020-02-22 13:27:44\", \"modifiedtime\": \"2020-02-22 15:03:48\", \"curstepruncount\": 2}}','DESKTOP-STEVEN','success','ok','2020-02-22 15:03:58','2020-02-22 15:31:23');
INSERT INTO `taskflowdb`.`instance_steps` (`id`,`instanceid`,`stepnum`,`stepname`,`arguments`,`workername`,`status`,`message`,`createdtime`,`modifiedtime`) VALUES (4,1,1,'安装操作系统','{\"os\": \"centos 8.0\", \"mem_gb\": 24, \"cpu_num\": 8, \"disk_gb\": 100, \"machine_name\": \"VMS001\", \"sys_taskflow_instance\": {\"id\": 1, \"title\": \"VMS001上线\", \"flowid\": 1, \"status\": \"standby\", \"creator\": \"steven\", \"updator\": \"steven\", \"arguments\": \"{\\\"os\\\": \\\"centos 8.0\\\", \\\"mem_gb\\\": 24, \\\"cpu_num\\\": 8, \\\"disk_gb\\\": 100, \\\"machine_name\\\": \\\"VMS001\\\"}\", \"stepcount\": 3, \"curstepnum\": 1, \"createdtime\": \"2020-02-22 13:27:44\", \"description\": \"测试流程\", \"nextruntime\": \"2020-02-22 15:04:04\", \"modifiedtime\": \"2020-02-22 15:09:09\", \"curstepruncount\": 2}}','DESKTOP-STEVEN','success','ok','2020-02-22 15:14:56','2020-02-22 15:31:23');
INSERT INTO `taskflowdb`.`instance_steps` (`id`,`instanceid`,`stepnum`,`stepname`,`arguments`,`workername`,`status`,`message`,`createdtime`,`modifiedtime`) VALUES (5,1,2,'初始化配置信息','{\"ip\": \"127.0.0.1\", \"port\": \"22\", \"user\": \"op\", \"password\": \"test\", \"machine_name\": \"VMS001\", \"sys_taskflow_instance\": {\"id\": 1, \"title\": \"VMS001上线\", \"flowid\": 1, \"status\": \"standby\", \"creator\": \"steven\", \"updator\": \"steven\", \"arguments\": \"{\\\"os\\\": \\\"centos 8.0\\\", \\\"mem_gb\\\": 24, \\\"cpu_num\\\": 8, \\\"disk_gb\\\": 100, \\\"machine_name\\\": \\\"VMS001\\\"}\", \"stepcount\": 3, \"curstepnum\": 2, \"createdtime\": \"2020-02-22 13:27:44\", \"description\": \"测试流程\", \"nextruntime\": \"2020-02-22 15:15:02\", \"modifiedtime\": \"2020-02-22 15:15:02\", \"curstepruncount\": 2}}','DESKTOP-STEVEN','success','','2020-02-22 15:15:32','2020-02-22 15:31:23');
INSERT INTO `taskflowdb`.`instance_steps` (`id`,`instanceid`,`stepnum`,`stepname`,`arguments`,`workername`,`status`,`message`,`createdtime`,`modifiedtime`) VALUES (6,1,3,'通知','{\"sys_taskflow_instance\": {\"id\": 1, \"title\": \"VMS001上线\", \"flowid\": 1, \"status\": \"standby\", \"creator\": \"steven\", \"updator\": \"steven\", \"arguments\": \"{\\\"os\\\": \\\"centos 8.0\\\", \\\"mem_gb\\\": 24, \\\"cpu_num\\\": 8, \\\"disk_gb\\\": 100, \\\"machine_name\\\": \\\"VMS001\\\"}\", \"stepcount\": 3, \"curstepnum\": 3, \"createdtime\": \"2020-02-22 13:27:44\", \"description\": \"测试流程\", \"nextruntime\": \"2020-02-22 15:16:06\", \"modifiedtime\": \"2020-02-22 15:15:35\", \"curstepruncount\": 2}}','DESKTOP-STEVEN','fail','\'sys_instance\'','2020-02-22 15:15:54','2020-02-22 15:31:23');
INSERT INTO `taskflowdb`.`instance_steps` (`id`,`instanceid`,`stepnum`,`stepname`,`arguments`,`workername`,`status`,`message`,`createdtime`,`modifiedtime`) VALUES (7,1,3,'通知','{\"sys_taskflow_instance\": {\"id\": 1, \"title\": \"VMS001上线\", \"flowid\": 1, \"status\": \"standby\", \"creator\": \"steven\", \"updator\": \"steven\", \"arguments\": \"{\\\"os\\\": \\\"centos 8.0\\\", \\\"mem_gb\\\": 24, \\\"cpu_num\\\": 8, \\\"disk_gb\\\": 100, \\\"machine_name\\\": \\\"VMS001\\\"}\", \"stepcount\": 3, \"curstepnum\": 3, \"createdtime\": \"2020-02-22 13:27:44\", \"description\": \"测试流程\", \"nextruntime\": \"2020-02-22 15:16:54\", \"modifiedtime\": \"2020-02-22 15:15:54\", \"curstepruncount\": 3}}','DESKTOP-STEVEN','fail','\'sys_instance\'','2020-02-22 15:17:47','2020-02-22 15:31:23');
INSERT INTO `taskflowdb`.`instance_steps` (`id`,`instanceid`,`stepnum`,`stepname`,`arguments`,`workername`,`status`,`message`,`createdtime`,`modifiedtime`) VALUES (8,1,3,'通知','{\"sys_taskflow_instance\": {\"id\": 1, \"title\": \"VMS001上线\", \"flowid\": 1, \"status\": \"fail\", \"creator\": \"steven\", \"updator\": \"steven\", \"arguments\": \"{\\\"os\\\": \\\"centos 8.0\\\", \\\"mem_gb\\\": 24, \\\"cpu_num\\\": 8, \\\"disk_gb\\\": 100, \\\"machine_name\\\": \\\"VMS001\\\"}\", \"stepcount\": 3, \"curstepnum\": 3, \"createdtime\": \"2020-02-22 13:27:44\", \"description\": \"测试流程\", \"nextruntime\": \"2020-02-22 15:16:54\", \"modifiedtime\": \"2020-02-22 15:17:47\", \"curstepruncount\": 4}}','DESKTOP-STEVEN','fail','\'sys_instance\'','2020-02-22 15:17:49','2020-02-22 15:31:23');
INSERT INTO `taskflowdb`.`instance_steps` (`id`,`instanceid`,`stepnum`,`stepname`,`arguments`,`workername`,`status`,`message`,`createdtime`,`modifiedtime`) VALUES (9,1,3,'通知','{\"sys_taskflow_instance\": {\"id\": 1, \"title\": \"VMS001上线\", \"flowid\": 1, \"status\": \"fail\", \"creator\": \"steven\", \"updator\": \"steven\", \"arguments\": \"{\\\"os\\\": \\\"centos 8.0\\\", \\\"mem_gb\\\": 24, \\\"cpu_num\\\": 8, \\\"disk_gb\\\": 100, \\\"machine_name\\\": \\\"VMS001\\\"}\", \"stepcount\": 3, \"curstepnum\": 3, \"createdtime\": \"2020-02-22 13:27:44\", \"description\": \"测试流程\", \"nextruntime\": \"2020-02-22 15:16:54\", \"modifiedtime\": \"2020-02-22 15:17:49\", \"curstepruncount\": 5}}','DESKTOP-STEVEN','success','','2020-02-22 15:18:52','2020-02-22 15:31:23');
INSERT INTO `taskflowdb`.`instance_steps` (`id`,`instanceid`,`stepnum`,`stepname`,`arguments`,`workername`,`status`,`message`,`createdtime`,`modifiedtime`) VALUES (10,1,3,'通知','{\"sys_taskflow_instance\": {\"id\": 1, \"title\": \"VMS001上线\", \"flowid\": 1, \"status\": \"success\", \"creator\": \"steven\", \"updator\": \"steven\", \"arguments\": \"{\\\"os\\\": \\\"centos 8.0\\\", \\\"mem_gb\\\": 24, \\\"cpu_num\\\": 8, \\\"disk_gb\\\": 100, \\\"machine_name\\\": \\\"VMS001\\\"}\", \"stepcount\": 3, \"curstepnum\": 3, \"createdtime\": \"2020-02-22 13:27:44\", \"description\": \"测试流程\", \"nextruntime\": \"2020-02-22 15:16:54\", \"modifiedtime\": \"2020-02-22 15:18:55\", \"curstepruncount\": 5}}','DESKTOP-STEVEN','success','','2020-02-22 15:19:28','2020-02-22 15:31:23');
INSERT INTO `taskflowdb`.`instance_steps` (`id`,`instanceid`,`stepnum`,`stepname`,`arguments`,`workername`,`status`,`message`,`createdtime`,`modifiedtime`) VALUES (11,1,3,'通知','{\"sys_taskflow_instance\": {\"id\": 1, \"title\": \"VMS001上线\", \"flowid\": 1, \"status\": \"success\", \"creator\": \"steven\", \"updator\": \"steven\", \"arguments\": \"{\\\"os\\\": \\\"centos 8.0\\\", \\\"mem_gb\\\": 24, \\\"cpu_num\\\": 8, \\\"disk_gb\\\": 100, \\\"machine_name\\\": \\\"VMS001\\\"}\", \"stepcount\": 3, \"curstepnum\": 3, \"createdtime\": \"2020-02-22 13:27:44\", \"description\": \"测试流程\", \"nextruntime\": \"2020-02-22 15:16:54\", \"modifiedtime\": \"2020-02-22 15:18:55\", \"curstepruncount\": 5}}','DESKTOP-STEVEN','success','','2020-02-22 15:30:40','2020-02-22 15:30:43');
INSERT INTO `taskflowdb`.`instance_steps` (`id`,`instanceid`,`stepnum`,`stepname`,`arguments`,`workername`,`status`,`message`,`createdtime`,`modifiedtime`) VALUES (12,1,3,'通知','{\"sys_taskflow_instance\": {\"id\": 1, \"title\": \"VMS001上线\", \"flowid\": 1, \"status\": \"success\", \"creator\": \"steven\", \"updator\": \"steven\", \"arguments\": \"{\\\"os\\\": \\\"centos 8.0\\\", \\\"mem_gb\\\": 24, \\\"cpu_num\\\": 8, \\\"disk_gb\\\": 100, \\\"machine_name\\\": \\\"VMS001\\\"}\", \"stepcount\": 3, \"curstepnum\": 3, \"createdtime\": \"2020-02-22 13:27:44\", \"description\": \"测试流程\", \"nextruntime\": \"2020-02-22 15:16:54\", \"modifiedtime\": \"2020-02-22 15:18:55\", \"curstepruncount\": 5}}','DESKTOP-STEVEN','success','','2020-02-22 15:33:13','2020-02-22 15:33:16');
INSERT INTO `taskflowdb`.`instance_steps` (`id`,`instanceid`,`stepnum`,`stepname`,`arguments`,`workername`,`status`,`message`,`createdtime`,`modifiedtime`) VALUES (13,1,3,'通知','{\"sys_taskflow_instance\": {\"id\": 1, \"title\": \"VMS001上线\", \"flowid\": 1, \"status\": \"success\", \"creator\": \"steven\", \"updator\": \"steven\", \"arguments\": \"{\\\"os\\\": \\\"centos 8.0\\\", \\\"mem_gb\\\": 24, \\\"cpu_num\\\": 8, \\\"disk_gb\\\": 100, \\\"machine_name\\\": \\\"VMS001\\\"}\", \"stepcount\": 3, \"curstepnum\": 3, \"createdtime\": \"2020-02-22 13:27:44\", \"description\": \"测试流程\", \"nextruntime\": \"2020-02-22 15:16:54\", \"modifiedtime\": \"2020-02-22 15:18:55\", \"curstepruncount\": 5}}','DESKTOP-STEVEN','success','','2020-02-22 15:35:06','2020-02-22 15:35:09');

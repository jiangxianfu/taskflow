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
   `id` int(11) NOT NULL,
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



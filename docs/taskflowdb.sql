CREATE SCHEMA IF NOT EXISTS `taskflowdb`;

use `taskflowdb`;

CREATE TABLE `task_form` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL COMMENT '任务主题',
  `description` varchar(1000) NOT NULL COMMENT '任务描述',
  `task_type` varchar(12) NOT NULL COMMENT '任务类型(workflow,module)',
  `task_name` varchar(255) NOT NULL COMMENT '任务名称(workflow_name,module_name)',
  `args_json` json NOT NULL COMMENT '表单参数',
  `plan_runtime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '计划运行时间',
  `status` varchar(15) NOT NULL COMMENT 'standby---待运行，pause----暂停中, running----运行中,success----成功，failure----失败',
  `creator` varchar(128) NOT NULL COMMENT '创建者',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='表单任务表';


CREATE TABLE `task_schedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL COMMENT '任务主题',
  `description` varchar(1000) NOT NULL COMMENT '任务描述',
  `cron_sched` varchar(25) NOT NULL COMMENT '调度cron表达式',
  `cron_enabled` tinyint(1) NOT NULL DEFAULT '1' COMMENT '调度是否启动',
  `task_type` varchar(12) NOT NULL COMMENT '任务类型(workflow,module)',
  `task_name` varchar(255) NOT NULL COMMENT '任务名称(workflow_name,module_name)',
  `args_python_code` text NOT NULL COMMENT '表单参数python脚本(def get_arguments(**kwargs))',
  `trigger_last_time` datetime DEFAULT NULL COMMENT '上次运行时间',
  `trigger_next_time` datetime DEFAULT NULL COMMENT '下次运行时间',
  `status` varchar(15) NOT NULL COMMENT 'standby---待运行，pause----暂停中,running----运行中,success----成功，failure----失败',
  `creator` varchar(128) NOT NULL COMMENT '创建者',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='调度任务表';

CREATE TABLE `task_instance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT 'step_name或者module_name或者workflow_name',
  `source_id` int NOT NULL COMMENT '来源ID',
  `source_type` varchar(50) NOT NULL COMMENT '来源类型(schedule,form)',
  `parent_id` int NOT NULL DEFAULT '0' COMMENT '任务parent id,用于workflow类型',
  `task_type` varchar(12) NOT NULL COMMENT '任务类型(workflow,module)',
  `task_name` varchar(255) NOT NULL COMMENT '任务名称(workflow_name,module_name)',
  `args_json` json NOT NULL COMMENT '表单参数',
  `status` varchar(15) NOT NULL COMMENT 'running----运行中,success----成功，failure----失败',
  `worker_hostname` varchar(20) COMMENT 'worker的机器名称',
  `result_json` json COMMENT '执行的结果返回值',
  `result_message` varchar(5000) COMMENT '执行结果',
  `retry_count` int NOT NULL DEFAULT '0' COMMENT '重试次数',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务实例表';

CREATE TABLE `task_instance_log` (
   `id` int(11) NOT NULL AUTO_INCREMENT,
   `instance_id` int(11) NOT NULL,
   `level` varchar(45) NOT NULL DEFAULT 'info' COMMENT '告警级别:info,warning,error',
   `title` varchar(50) NOT NULL COMMENT '主题',
   `message` varchar(8000) NOT NULL,
   `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
   PRIMARY KEY (`id`),
   KEY `idx_insid` (`instance_id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4

/*
-------------------init sample data------------------------------------------------

INSERT INTO `task_form`(`title`,`description`,`task_type`,`task_name`,`args_json`,`status`,`creator`) 
VALUES ('VMS001上线','测试流程','module','action_init_os',
'{\"os\": \"centos 8.0\", \"mem_gb\": 24, \"cpu_num\": 8, \"disk_gb\": 100, \"machine_name\": \"VMS001\"}',
'standby','steven');


INSERT INTO `task_schedule`(`title`,`description`,`cron_sched`,`task_type`,`task_name`,`args_python_code`,`status`,`creator`) 
VALUES ('VMS001上线','测试流程','module','action_init_os',
'import datetime

import requests
import time
def get_arguments(**kwargs):
    data={}
    data["start_time"]=int((time.time()-100000)*1000)
    data["end_time"]=int(time.time()*1000)
    data["data"]="ok"
    return data
',
'standby','steven');

*/

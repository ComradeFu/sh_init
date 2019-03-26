#!/usr/bin/python
# -*- coding: utf-8 -*-  

import os,sys,getopt

# 还原备份的类型
# 目前支持file、mongo两类
backup_type = "unknow"

def usage():

    print('''useage: unbackup [option] ... [--tp [mongo | file]] [arg] ... 
    arg 参数说明：
    -t : 还原备份的类型，比如 file、mongo 等
    --help: 帮助
    -h : 还原备份mongo时，mongo的主机地址，默认 127.0.0.1
    -p : 还原备份mongo时，mongo的端口，默认 27017
    --docker: 有值时，以docker容器的方式进行，比如 docker=mongo
    --db : 需要还原备份的mongo库，比如 --db=test，如果不赋值则默认
    -f : from 备份 file 时，file的地址，以及还原的时候mongo的备份
    -d : 还原的目标文件夹路径''')


def invalid_notice(msg):
    print(msg + ''', 使用 unbackup --help 查看帮助''')

def check_and_get_arg(args, key):
    val = args.get(key)
    if val == None:
        invalid_notice("缺少参数{0}".format(key))
        exit(1)

    return val

def unbackup_file(run_args):
    # 备份的路径
    from_path = check_and_get_arg(run_args, "-f")

    # 还原的路径
    dest_path = check_and_get_arg(run_args, "-d")

    # 获取当前路径
    old_wd = os.getcwd()

    # cd 到还原目录下
    os.chdir(dest_path)

    # 使用 unzip 直接解压缩到指定的路径去
    os.system("unzip {0}".format(from_path))

    # 还原
    os.chdir(old_wd)

def unbackup_docker_mongo(run_args):

    # 用来还原的备份的路径
    from_path = check_and_get_arg(run_args, "-f")

    # 本地的临时文件夹
    local_tmp_path = "/tmp/unbackup_py"
    os.system("mkdir {0}".format(local_tmp_path))

    # 解压好备份的数据库文件
    os.system("unzip {0} -d {1}".format(from_path, local_tmp_path))

    docker_name = check_and_get_arg(run_args, "--docker")
    
    host = run_args.get("-h")
    if host == None:
        host = "127.0.0.1"
    
    port = run_args.get("-p")
    if port == None:
        port = 27017

    docker_target = "/tmp/restoretmp"

    # 把备份文件拷贝到 docker 里面去
    cmd_exec = "docker exec {0} /bin/bash -c \"mkdir {1}\"".format(
        docker_name,
        docker_target
    )
    os.system(cmd_exec)

    # 获取当前路径
    old_wd = os.getcwd()

    # cd 到还原目录下
    os.chdir(local_tmp_path)

    # 由于是只有一个库，所以直接找出来此库的名称
    files = os.listdir("./")
    only_one_origin_db = files[0]

    os.chdir("./{0}".format(only_one_origin_db))

    db = run_args.get("--db")
    if db == None:
        db = only_one_origin_db

    cmd_exec = "docker cp ./ {1}:{2}".format(only_one_origin_db, docker_name, docker_target)
    print("cmd exec :", cmd_exec)
    os.system(cmd_exec)

    # 还原
    os.chdir(old_wd)

    # 对docker执行还原备份指令
    cmd_exec = "docker exec {0} /bin/bash -c \"mongorestore -h {1} -p {2} -d {3} {4}\"".format(
        docker_name,
        host,
        port,
        db,
        docker_target
    )
    os.system(cmd_exec)

    # 清空临时目录
    cmd_exec = "docker exec {0} /bin/bash -c \"rm -rf {1}\"".format(
        docker_name,
        docker_target
    )
    os.system(cmd_exec)

    os.system("rm -rf {0}".format(local_tmp_path))

def unbackup_host_mongo(run_args):
    # 用来还原的备份的路径
    from_path = check_and_get_arg(run_args, "-f")

    # 本地的临时文件夹
    local_tmp_path = "/tmp/unbackup_py"
    os.system("mkdir {0}".format(local_tmp_path))

    # 解压好备份的数据库文件
    os.system("unzip {0} -d {1}".format(from_path, local_tmp_path))

    host = run_args.get("-h")
    if host == None:
        host = "127.0.0.1"
    
    port = run_args.get("-p")
    if port == None:
        port = 27017

    # 由于是只有一个库，所以直接找出来此库的名称
    files = os.listdir(local_tmp_path)
    only_one_origin_db = files[0]

    db = run_args.get("--db")
    if db == None:
        db = only_one_origin_db

    # 执行还原备份指令
    cmd_exec = "mongorestore -h {0} -p {1} -d {2} {3}".format(
        host,
        port,
        db,
        "{0}/{1}".format(local_tmp_path, only_one_origin_db)
    )
    os.system(cmd_exec)

    # 清空临时目录
    os.system("rm -rf {0}".format(local_tmp_path))

# 还原mongo的话，有两种方式，docker中的以及非docker中的
def unbackup_mongo(run_args):
    docker_name = run_args.get("--docker")
    if docker_name == None:
        unbackup_host_mongo(run_args)
    else:
        unbackup_docker_mongo(run_args)

def main():

    # sys.argv[0]是脚本名字，所以过滤掉
    opts, args = getopt.getopt(sys.argv[1:], "t:h:p:f:d:", ["help","db=","docker="])

    # 转换成字典
    run_args = {}
    for key, val in opts:
        run_args[key] = val

    if(run_args.get("--help") != None):
        usage()
        exit(0)

    backup_tp = run_args.get("-t")
    # 查看是那种类型
    if(backup_tp == None):
        invalid_notice("请使用 -t 选择一个还原的类型")
        exit(1)
    
    if backup_tp == "file":
        unbackup_file(run_args)
    elif backup_tp == "mongo":
        unbackup_mongo(run_args)
    else:
        invalid_notice("不支持的还原类型:" + backup_tp)

    print("还原备份完成")
    exit(0)

main()

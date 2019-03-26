#!/usr/bin/python
# -*- coding: utf-8 -*-  

import os,sys,getopt

# 备份的类型
# 目前支持file、mongo两类
backup_type = "unknow"

def usage():

    print('''useage: backup [option] ... [--tp [mongo | file]] [arg] ... 
    arg 参数说明：
    -t : 备份的类型，比如 file、mongo 等
    --help: 帮助
    -h : 备份mongo时，mongo的主机地址，默认 127.0.0.1
    -p : 备份mongo时，mongo的端口，默认 27017
    --docker: 有值时，以docker容器的方式进行，比如 docker=mongo
    --db : 需要备份的mongo库，比如 --db=test
    -f : from 备份 file 时，file的地址
    -d : 备份的目标文件夹路径''')

def invalid_notice(msg):
    print(msg + ''', 使用 backup --help 查看帮助''')

def check_and_get_arg(args, key):
    val = args.get(key)
    if val == None:
        invalid_notice("缺少参数{0}".format(key))
        exit(1)

    return val

def backup_file(run_args):
    # 被备份的路径
    from_path = check_and_get_arg(run_args, "-f")

    # 欲备份的路径
    dest_path = check_and_get_arg(run_args, "-d")

    # 获取当前路径
    old_wd = os.getcwd()

    # cd 到当前目录下
    os.chdir(from_path)

    # 使用 zip 直接压缩到指定的路径去
    os.system("zip {0} -r ./*".format(dest_path))

    # 还原
    os.chdir(old_wd)

def backup_docker_mongo(run_args):

    # 欲备份的路径
    dest_path = check_and_get_arg(run_args, "-d")

    docker_name = check_and_get_arg(run_args, "--docker")
    
    host = run_args.get("-h")
    if host == None:
        host = "127.0.0.1"
    
    port = run_args.get("-p")
    if port == None:
        port = 27017

    db = check_and_get_arg(run_args, "--db")

    docker_target = "/tmp/dumptmp/mongo/"

    # 对docker执行备份指令
    cmd_exec = "docker exec {0} /bin/bash -c \"mongodump -h {1} -p {2} -d {3} -o {4}\"".format(
        docker_name,
        host,
        port,
        db,
        docker_target
    )
    os.system(cmd_exec)

    # 本地的临时文件夹
    local_tmp_path = "/tmp/backup_py"
    os.system("mkdir {0}".format(local_tmp_path))

    # 从docker中拷贝目标备份出来
    cmd_exec = "docker cp {0}:{1} {2}".format(docker_name, docker_target, local_tmp_path)
    os.system(cmd_exec)

    # 获取当前路径
    old_wd = os.getcwd()

    # cd 到当前目录下
    # copy的是一个目录，所以目录带了一层，由上得知固定是 mongo
    os.chdir("{0}/mongo/".format(local_tmp_path))

    # 压缩到备份目录
    os.system("zip {0} -r ./*".format(dest_path))

    # 还原
    os.chdir(old_wd)

    # 清空临时目录
    cmd_exec = "docker exec {0} /bin/bash -c \"rm -rf {1}\"".format(
        docker_name,
        docker_target
    )
    os.system(cmd_exec)

    os.system("rm -rf {0}".format(local_tmp_path))

def backup_host_mongo(run_args):
    # 欲备份的路径
    dest_path = check_and_get_arg(run_args, "-d")

    host = run_args.get("-h")
    if host == None:
        host = "127.0.0.1"
    
    port = run_args.get("-p")
    if port == None:
        port = 27017

    db = check_and_get_arg(run_args, "--db")

    # 本地的临时文件夹
    local_tmp_path = "/tmp/backup_py"
    os.system("mkdir {0}".format(local_tmp_path))

    # 对docker执行备份指令
    cmd_exec = "mongodump -h {0} -p {1} -d {2} -o {3}".format(
        host,
        port,
        db,
        local_tmp_path
    )
    os.system(cmd_exec)

    # 获取当前路径
    old_wd = os.getcwd()

    # cd 到当前目录下
    os.chdir(local_tmp_path)

    # 压缩到备份目录
    os.system("zip {0} -r ./*".format(dest_path))

    # 还原
    os.chdir(old_wd)

    # 清空临时目录
    os.system("rm -rf {0}".format(local_tmp_path))

# 备份mongo的话，有两种方式，docker中的以及非docker中的
def backup_mongo(run_args):
    docker_name = run_args.get("--docker")
    if docker_name == None:
        backup_host_mongo(run_args)
    else:
        backup_docker_mongo(run_args)

def main():

    # sys.argv[0]是脚本名字，所以过滤掉
    opts, args = getopt.getopt(sys.argv[1:], "t:h:p:f:d:", ["help","db=", "docker="])

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
        invalid_notice("请使用 -t 选择一个备份的类型")
        exit(1)
    
    if backup_tp == "file":
        backup_file(run_args)
    elif backup_tp == "mongo":
        backup_mongo(run_args)
    else:
        invalid_notice("不支持的备份类型:" + backup_tp)

    print("备份完成")
    exit(0)

main()

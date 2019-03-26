# 父级目录
# 固定的喔
echo "自动配置脚本开始执行..."

basepath="$HOME/.local/config"
basetmppath="$basepath/tmp"

tempbashrc="$HOME/.bashrc"

git="https://codeload.github.com/ComradeFu/sh_init/zip/master"
git_name="sh_init-master"

# 创建好目录
if [ ! -d $basepath ]; then
    mkdir -p basepath
    echo "创建本地配置目录${basepath}"
fi

# 临时目录
if [ ! -d $basetmppath ]; then
    mkdir -p basetmppath
fi

cd $basetmppath

# 从gitlab上下载下来完整的包，并切解压缩
curl -O $git
unzip master

echo "完成git版本库下载:${git}"

# 讲固定名字下的文件夹拷贝到basepath
cp -rf ./${git_name} $basepath

echo "复制至:${basepath}"

if [ ! -f $tempbashrc ]; then
    touch $tempbashrc
fi
echo "source ${basepath}/init.sh" >> $tempbashrc

echo "导入 bashrc 完成"

# tempprofilerc="~/.profile"
# if [ ! -f $tempprofilerc ]; then
#     touch $tempprofilerc
# fi
# echo "source ${basepath}/init.sh" > $tempprofilerc

# 删除临时文件夹
rm -rf $basetmppath

echo "自动配置完成"

# 父级目录
# 固定的喔
basepath="$HOME/.local/config"
basetmppath="$basepath/tmp"

tempbashrc="$HOME/.bashrc"

# 创建好目录
if [ ! -d $basetmppath ]; then
    mkdir -p basetmppath
fi

cd $basetmppath

# 从gitlab上下载下来完整的包，并切解压缩
curl -O "https://codeload.github.com/ComradeFu/sh_init/zip/master"
unzip master

# 讲固定名字下的文件夹拷贝到basepath
cp -rf ./sh_init-master $basepath

if [ ! -f $tempbashrc ]; then
    touch $tempbashrc
fi
echo "source ${basepath}/init.sh" >> $tempbashrc

# tempprofilerc="~/.profile"
# if [ ! -f $tempprofilerc ]; then
#     touch $tempprofilerc
# fi
# echo "source ${basepath}/init.sh" > $tempprofilerc

# 删除临时文件夹
rm -rf $basetmppath

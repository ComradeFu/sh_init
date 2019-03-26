# 防止被加载两次
# if [ -z "$_INIT_SH_LOADED" ]; then
#     _INIT_SH_LOADED=1
# else
#     return
# fi

# 父级目录
localbasepath="$HOME/.local"

# 将个人 ~/.local/bin 目录加入 PATH
local_bin_path="$localbasepath/bin"
if [ -d $local_bin_path ]; then
    # 增加所有文件的权限
    for file in $local_bin_path/*; do
        chmod 777 $file
    done
    export PATH="$local_bin_path:$PATH"
    # echo "注入路径 $PATH"
fi

# 后面可以增加一些自己的定义，比如 config.sh 、 local.sh 等等

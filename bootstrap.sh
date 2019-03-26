# 父级目录
# 固定的喔
basepath="$HOME/.local"
tempbashrc="$HOME/.bashrc"

if [ ! -d $basepath ]; then
    mkdir -p basepath
fi

if [ ! -f $tempbashrc ]; then
    touch $tempbashrc
fi
echo "source ${basepath}/init.sh" >> $tempbashrc

# tempprofilerc="~/.profile"
# if [ ! -f $tempprofilerc ]; then
#     touch $tempprofilerc
# fi
# echo "source ${basepath}/init.sh" > $tempprofilerc

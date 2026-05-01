# 01-Bash核心语法

## 变量

```bash
# 定义与使用
name="value"          # 等号两边不能有空格
echo $name            # 引用变量
echo ${name}          # 花括号界定边界
readonly PI=3.14      # 只读变量
unset name            # 删除变量

# 特殊变量
$0  # 脚本名
$1  # 第 N 个参数
$#  # 参数个数
$@  # 所有参数（独立）
$*  # 所有参数（合并为一个字符串）
$?  # 上一命令退出码
$$  # 当前 PID
$!  # 最后一个后台进程 PID
```

## 条件判断

```bash
# test 命令 / [ ] / [[ ]]
if [[ condition ]]; then
    ...
elif [[ condition2 ]]; then
    ...
else
    ...
fi

# 文件测试
[[ -f file ]]  # 是否为普通文件
[[ -d dir ]]   # 是否为目录
[[ -r file ]]  # 是否可读
[[ -s file ]]  # 是否非空

# 字符串测试
[[ -z "$str" ]]  # 为空
[[ "$a" == "$b" ]]
[[ "$a" =~ regex ]]  # 正则匹配

# 数值比较
[[ $a -eq $b ]]  # equal
[[ $a -ne $b ]]  # not equal
[[ $a -lt $b ]]  # less than
[[ $a -gt $b ]]  # greater than
```

## 循环

```bash
# for 循环
for i in {1..10}; do ... done
for file in *.log; do gzip "$file"; done

# while 循环
while read line; do
    echo "$line"
done < file.txt

# until 循环
until [[ condition ]]; do ... done
```

## 函数

```bash
myfunc() {
    local local_var="only inside"  # local 限定作用域
    echo "param1: $1, param2: $2"
    return 0  # 0 成功，1-255 失败
}
myfunc arg1 arg2
```

## 数组

```bash
arr=(a b c d)
echo ${arr[0]}        # 第一个元素
echo ${arr[@]}        # 所有元素
echo ${#arr[@]}       # 数组长度
arr+=(e f)            # 追加元素
```

## 常用技巧

```bash
# 默认值
${var:-default}       # var 未设置或为空时返回 default
${var:=default}       # 同上，并赋值
${var:+value}         # var 已设置时返回 value
${var:?error}         # var 未设置时报错退出

# 字符串操作
${str#pattern}        # 去掉最短前缀匹配
${str##pattern}       # 去掉最长前缀匹配
${str%pattern}        # 去掉最短后缀匹配
${str%%pattern}       # 去掉最长后缀匹配
${str:offset:length}  # 子串

# 命令替换
$(command)            # 推荐
`command`             # 旧式

# 算术运算
$((a + b))
$((a * b))
```

## 扩展阅读

- [02-文本处理三剑客](02-文本处理三剑客.md) — grep/sed/awk 进阶
- [04-脚本调试技巧](04-脚本调试技巧.md) — 写出健壮脚本

# pmeter

pmeter性能测试工具
> 自动化性能测试


## 功能亮点
- 压测参数配置化
- 智能判断性能瓶颈
- 支持分布式压测
- 自动生成统计报表


## 系统要求
- 系统平台: `linux`, `windows`
- python版本: `python3.5 +`

## 使用说明

1.安装依赖包
``` shell script
pip install -r requirements.txt
```

2.配置好 `etc/config.ini` 和 `etc/config.xlsx` 文件

3.运行根目录下的 `app.py`
``` shell script
python app.py
```
4.执行自动化jmeter测试
``` shell script
python app.py auto
```
5.解析jtl文件,生成报表
``` shell script
python app.py report
```
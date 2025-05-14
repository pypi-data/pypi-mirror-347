# Octopus Video Master 视频处理器

## 安装
```shell
pip install octopus-videomaster
```

## 使用
```shell
ovm [process_video | info] video_path [--paramsters [parameter-value]] 
```

## Process Video子命令参数说明
|参数名|简称|数据类型|默认值|说明|
|------|------|------|------|------|
|--input_path|-|Path|-|输入文件完整路径|
|--output|-o|str|-|输出路径|
|--rotate|-r|float|0|旋转角度|
|--scale|-sc|float|0|缩放比例|
|--speed|-sp|float|1|播放速率比例|
|--fliph|-fh|bool|False|水平镜像|
|--flipv|-fv|bool|False|垂直镜像|
|--noise|-n|int|0|噪音|
|--blur|-b|int|0|模糊|
|--delete-frame|-df|int|0|抽帧|
|--insert-frame|-if|int|0|插帧|
|--insert-image|-ii|Path|-|插入图片|
|--log-level|-|str|INFO|日志级别|

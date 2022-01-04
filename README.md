# WAV-Batch-Compressor

A simple python script to batch compress WAV sample packs to FLAC, remaining the file structure.

**BE CAREFUL TO OPERATE ON YOUR DATA!!**

**THE AUTHOR IS NOT RESPONSIBLE FOR YOUR DATA CORRUPTION CAUSED BY THIS SCRIPT!!**

Supports Multi-threading for fast processing. The number is controlled by `PROC_NUM` (8 by default) in the script. You can change it.

Non-WAV files would also be copied to the destination folder.

If there are errors during the compressing process, the script would log them into `log.txt` so you can check them later.

You need Python 3.6+ and FFMPEG to use this script!



**请谨慎操作数据！作者不对由此脚本产生的数据损坏负责！**

这是一个简单的python脚本，可以批量把wav采样包压成flac，同时完美保留原来的目录结构，非wav文件（如手册）也会原样复制过去。支持多线程，可以充分利用CPU（数量可以修改脚本中的 `PROC_NUM` 设置，默认为8）。支持用GUI选择输入输出目录，支持错误日志，日志会保存在输出文件夹下的 `log.txt` 中。

你需要Python 3.6以上，以及FFMPEG，才能运行此脚本。


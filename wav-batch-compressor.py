import os
import sys
import subprocess
import itertools as it
from multiprocessing.pool import ThreadPool
from shutil import copyfile
import tkinter as tk
from tkinter import filedialog, messagebox

inpath = ""
outpath = ""

PROC_NUM = 8

proc_que = []

cnt_wav = 0
cnt_oth = 0

cnt_err = 0

def getAllDir(path, out):
    global cnt_wav
    global cnt_oth
    filesList = os.listdir(path)
    for fileName in filesList:
        fileAbsPath = os.path.join(path, fileName)
        if os.path.isdir(fileAbsPath):
            getAllDir(fileAbsPath, out + "\\" + fileName)
        else:
            tmp = os.path.splitext(fileName)
            raw_name = tmp[0]
            ext_name = tmp[1]
            os.makedirs(out, exist_ok=True)
            if ext_name == ".wav":
                cnt_wav += 1
                proc_que.append("ffmpeg -n -i \"{}\" -acodec flac -compression_level 8 \"{}.flac\" -hide_banner -loglevel error".format(fileAbsPath, out + "\\" + raw_name))
            else:
                cnt_oth += 1
                copyfile(fileAbsPath, out + "\\" + fileName)
                

def run_proc(cmd):
    proc = subprocess.run(cmd, capture_output=True)
    ffout = proc.stdout.decode() + proc.stderr.decode()
    if len(ffout) > 3:
        print(ffout)
    return cmd, proc.returncode, ffout


if __name__ == "__main__":
    inpath = filedialog.askdirectory(title="请选择源路径")
    if inpath == "":
        messagebox.showerror("错误", "请选择路径！")
        sys.exit()

    outpath = filedialog.askdirectory(title="请选择输出路径")
    if outpath == "":
        messagebox.showerror("错误", "请选择路径！")
        sys.exit()

    confirm = messagebox.askokcancel("确认", "确认要将\n    {}\n中的wav全部转换为flac，输出到\n    {}\n吗？".format(inpath, outpath))

    if confirm == False:
        print("取消操作")
        sys.exit()

    log_file = open(f"{outpath}\\log.txt", "w")

    getAllDir(inpath, outpath)
    print("文件遍历完成！共发现 {} 个wav文件, {} 个其它文件".format(cnt_wav, cnt_oth))

    cnt = 0 

    for cmd, rc, output in ThreadPool(PROC_NUM).imap_unordered(run_proc, proc_que):
        if rc != 0 or len(output) > 5:
            cnt_err += 1
            errfile = cmd.split("\"")[1]
            if rc != 0:
                print(f"【!】 FFMPEG致命错误！可能是由于输入wav格式不合法，或输出目录下已存同名文件。对应文件为 [ {errfile} ]")
                log_file.write(f"FFMPEG致命错误：{errfile}\n    {output}")
            else:
                print(f"【!】 检测到FFMPEG可能出现了问题，对应文件为 [ {errfile} ]\n")
                log_file.write(f"FFMPEG可能出现问题：{errfile}\n    {output}")
            
        cnt += 1
        if cnt % 10 == 0:
            print("转换为flac中... {}/{}".format(cnt, cnt_wav))
            
    log_file.close()

    if cnt_err == 0:
        messagebox.showinfo("撒花", "转换完成！没有遇到问题！")
        os.remove(f"{outpath}\\log.txt")
    else:
        messagebox.showwarning("注意", f"转换完成！共遇到{cnt_err}个问题，已在输出目录下保存错误日志")

    print("该程序由APT编写 :)")

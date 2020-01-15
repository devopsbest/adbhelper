import os
import shutil
import subprocess
import time
import re
from subprocess import Popen

import requests
from ptest.plogger import preporter
import platform

current_dir = os.path.split(os.path.realpath(__file__))[0]
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def run_command_on_shell(command_string):
    try:
        process = start_process_by_command(command_string)
        out, error = process.communicate()
        return out.decode().splitlines()
    except:
        print("Command Error")
        preporter.info('error occur for command {}'.format(command_string))
        raise

def start_process_by_command(command_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT):
    process = Popen(command_string, shell=shell, stdout=stdout, stderr=stderr)
    return process


def kill_progress_by_name(progress_name):
    cmd = "killall -9 {}".format(progress_name)
    run_command_on_shell(cmd)
    preporter.info("progress {} was killed ".format(progress_name))


def write_log(file_name, content):
    file = current_dir + "/" + file_name
    with open(file, 'w+') as f:
        f.write(content)


def exec_command(cmd):
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (stdoutdata, stderrdata) = result.communicate()
    if (re.search("error", str(stdoutdata))):
        print ("error occur!")
    else:
        return stdoutdata


def get_android_version():
    cmd = "adb shell getprop ro.build.version.release"
    result = run_command_on_shell(cmd)[0]
    return result

def get_device_name():
    cmd = "adb shell getprop ro.product.model"
    result = run_command_on_shell(cmd)[0]
    return result

def find_devices():
    rst = os.popen('adb devices').read()
    devices = re.findall(r'(.*?)\s+device', rst)
    if len(devices) > 1:
        Ids = devices[1:]
    else:
        Ids = []
    return Ids


def get_device_state():
    """
    status: offline | bootloader | device
    """
    return exec_command("adb get-state")

def get_device_id():
    return exec_command("adb get-serialno")


def get_android_version():
    return exec_command("adb shell getprop ro.build.version.release")


def get_sdk_version():
    return exec_command("adb shell getprop ro.build.version.sdk")


def get_device_model():
    return exec_command("adb shell getprop ro.product.model")


def get_pid(package_name):
    if platform.system() is "Windows":
        pidinfo = exec_command("adb shell ps | findstr %s$" %package_name).stdout.read()
    else:
        pidinfo = exec_command("adb shell ps | grep -w %s" %(package_name)).stdout.read()

    if pidinfo == '':
        return "the process doesn't exist."

    pattern = re.compile(r"\d+")
    result = pidinfo.split(" ")
    result.remove(result[0])

    return pattern.findall(" ".join(result))[0]


def kill_process(pid):
    if exec_command("adb shell kill %s" %str(pid)).stdout.read().split(": ")[-1] == "":
        return "kill success"
    else:
        return exec_command("adb shell kill %s" %str(pid)).stdout.read().split(": ")[-1]


def quit_app(package_name):
    exec_command("adb shell am force-stop %s" % package_name)


def find_apks(path):

    if os.path.isfile(path) and path.endswith('.apk'):
        return True
    else:
        print("No file found")
        return False



def install_apks(apk_name):
    cmd = 'adb install {0}'.format(apk_name)
    result = exec_command(cmd)


def cover_install_apks(apk_name):
    cmd = 'adb install -r {0}'.format(apk_name)
    result = exec_command(cmd)


def uninstall_apks(package_name):
    cmd = 'adb uninstall {0}'.format(package_name)
    result = exec_command(cmd)

def check_start_time(start_page):
    cmd='adb shell am start -W -n {} | grep TotalTime'.format(start_page)
    result = exec_command(cmd)
    return result
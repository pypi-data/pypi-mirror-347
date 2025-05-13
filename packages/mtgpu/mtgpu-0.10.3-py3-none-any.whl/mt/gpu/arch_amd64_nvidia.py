"""Module specific to amd64-nvidia arch."""


import os
import psutil as _pu

try:
    from pynvml import *
except ImportError:
    raise RuntimeError(
        "Package 'pynvml' is required on a machine with an Nvidia GPU card. Please install pynvml using pip."
    )


def get_mem_info_impl():
    res = {}

    mem_info = _pu.virtual_memory()
    res["cpu_mem_free"] = mem_info.free
    res["cpu_mem_used"] = mem_info.used
    res["cpu_mem_total"] = mem_info.total
    res["cpu_mem_shared_with_gpu"] = False

    nvmlInit()
    driver_version = nvmlSystemGetDriverVersion()
    if isinstance(driver_version, bytes):
        driver_version = driver_version.decode()

    deviceCount = nvmlDeviceGetCount()
    if deviceCount:
        gpus = []
        for i in range(deviceCount):
            gpu = {}
            handle = nvmlDeviceGetHandleByIndex(i)

            gpu_name = nvmlDeviceGetName(handle)
            if isinstance(gpu_name, bytes):
                gpu_name = gpu_name.decode()
            gpu["name"] = gpu_name
            gpu["driver_version"] = driver_version

            bus_id = nvmlDeviceGetPciInfo(handle).busId
            if isinstance(bus_id, bytes):
                bus_id = bus_id.decode()
            gpu["bus"] = bus_id
            try:
                gpu["fan_speed"] = nvmlDeviceGetFanSpeed(handle)
            except:
                pass

            mem_info = nvmlDeviceGetMemoryInfo(handle)
            gpu["mem_free"] = mem_info.free
            gpu["mem_used"] = mem_info.used
            gpu["mem_total"] = mem_info.total

            gpus.append(gpu)

        res["gpus"] = gpus
    else:
        res["gpus"] = []

    nvmlShutdown()

    return res


def sort_cuda_devices():
    gpus = get_mem_info_impl()["gpus"]
    if not gpus:
        return

    indices = [(i, x["mem_free"]) for i, x in enumerate(gpus)]
    indices.sort(key=lambda x: -x[1])

    value = ",".join((str(x[0]) for x in indices))
    os.environ["CUDA_VISIBLE_DEVICES"] = value

#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
A (user-)friendly wrapper to nvidia-smi

Author: Panagiotis Mavrogiorgos
Modified: Jason King
Adapted from: https://github.com/anderskm/gputil
"""

import argparse
import json
import itertools as it
import math
import operator
import os
import shlex
import shutil
import subprocess
import sys

__version__ = "1.1.0"

NVIDIA_SMI_GET_GPUS = (
    "nvidia-smi --query-gpu=index,uuid,fan.speed,utilization.gpu,"
    "memory.total,memory.used,memory.free,driver_version,name,"
    "gpu_serial,display_active,display_mode,power.draw,temperature.gpu "
    "--format=csv,noheader,nounits"
)
NVIDIA_SMI_GET_PROCS = (
    "nvidia-smi --query-compute-apps=pid,process_name,gpu_uuid,gpu_name,used_memory "
    "--format=csv,noheader,nounits"
)


class GPU:
    def __init__(
        self,
        id,
        uuid,
        fan_speed,
        power_draw,
        gpu_util,
        mem_total,
        mem_used,
        mem_free,
        driver,
        gpu_name,
        serial,
        display_mode,
        display_active,
        temperature,
    ):
        self.id = id
        self.uuid = uuid
        self.power_draw = power_draw
        self.fan_speed = fan_speed
        self.gpu_util = gpu_util
        self.mem_util = float(mem_used) / float(mem_total) * 100 if mem_total else 0
        self.mem_total = mem_total
        self.mem_used = mem_used
        self.mem_free = mem_free
        self.driver = driver
        self.name = gpu_name
        self.serial = serial
        self.display_mode = display_mode
        self.display_active = display_active
        self.temperature = temperature

    def __repr__(self):
        msg = (
            "id: {id} | UUID: {uuid} | fan: {fan_speed:5.1f}% | power: {power_draw}% | "
            "gpu_util: {gpu_util:5.1f}% | mem_util: {mem_util:5.1f}% | "
            "mem_free: {mem_free:7.1f}MB |  mem_total: {mem_total:7.1f}MB"
        )
        return msg.format(**self.__dict__)

    def to_json(self):
        return json.dumps(self.__dict__)


class GPUProcess:
    def __init__(self, pid, process_name, gpu_id, gpu_uuid, gpu_name, used_memory):
        self.pid = pid
        self.process_name = process_name
        self.gpu_id = gpu_id
        self.gpu_uuid = gpu_uuid
        self.gpu_name = gpu_name
        self.used_memory = used_memory

    def __repr__(self):
        msg = (
            "pid: {pid} | gpu_id: {gpu_id} | gpu_uuid: {gpu_uuid} | "
            "gpu_name: {gpu_name} | used_memory: {used_memory:7.1f}MB"
        )
        return msg.format(**self.__dict__)

    def to_json(self):
        return json.dumps(self.__dict__)


def to_float_or_inf(value):
    try:
        return float(value)
    except ValueError:
        return float("nan")


def _get_gpu(line):
    values = line.split(", ")
    id = values[0]
    uuid = values[1]
    fan_speed = to_float_or_inf(values[2])
    gpu_util = to_float_or_inf(values[3])
    mem_total = to_float_or_inf(values[4])
    mem_used = to_float_or_inf(values[5])
    mem_free = to_float_or_inf(values[6])
    driver = values[7]
    gpu_name = values[8]
    serial = values[9]
    display_active = values[10]
    display_mode = values[11]
    power_draw = to_float_or_inf(values[12])
    temp_gpu = to_float_or_inf(values[13])

    return GPU(
        id,
        uuid,
        fan_speed,
        power_draw,
        gpu_util,
        mem_total,
        mem_used,
        mem_free,
        driver,
        gpu_name,
        serial,
        display_mode,
        display_active,
        temp_gpu,
    )


def get_gpus():
    output = subprocess.check_output(shlex.split(NVIDIA_SMI_GET_GPUS))
    lines = output.decode("utf-8").split(os.linesep)
    gpus = (_get_gpu(line) for line in lines if line.strip())
    return gpus


def _get_gpu_proc(line, gpu_uuid_to_id_map):
    values = line.split(", ")
    pid = int(values[0])
    process_name = values[1]
    gpu_uuid = values[2]
    gpu_name = values[3]
    used_memory = to_float_or_inf(values[4])
    gpu_id = gpu_uuid_to_id_map.get(gpu_uuid, -1)
    return GPUProcess(pid, process_name, gpu_id, gpu_uuid, gpu_name, used_memory)


def get_gpu_processes():
    gpu_uuid_to_id_map = {gpu.uuid: gpu.id for gpu in get_gpus()}
    output = subprocess.check_output(shlex.split(NVIDIA_SMI_GET_PROCS))
    lines = output.decode("utf-8").split(os.linesep)
    return [_get_gpu_proc(line, gpu_uuid_to_id_map) for line in lines if line.strip()]


def is_gpu_available(gpu, gpu_util_max, mem_util_max, mem_free_min, include_ids, include_uuids):
    return (
        (math.isnan(gpu.gpu_util) or gpu.gpu_util <= gpu_util_max)
        and (math.isnan(gpu.mem_util) or gpu.mem_util <= mem_util_max)
        and (math.isnan(gpu.mem_free) or gpu.mem_free >= mem_free_min)
        and (not include_ids or gpu.id in include_ids)
        and (not include_uuids or gpu.uuid in include_uuids)
    )


def get_available_gpus(
    gpu_util_max=100.0,
    mem_util_max=100.0,
    mem_free_min=0.0,
    include_ids=None,
    include_uuids=None,
):
    gpus = list(get_gpus())
    include_ids = include_ids or [gpu.id for gpu in gpus]
    include_uuids = include_uuids or [gpu.uuid for gpu in gpus]
    selectors = (
        is_gpu_available(gpu, gpu_util_max, mem_util_max, mem_free_min, include_ids, include_uuids)
        for gpu in gpus
    )
    return it.compress(gpus, selectors)


def get_parser():
    parser = argparse.ArgumentParser(prog="nvsmifs", description="A (user-)friendly interface for nvidia-smi")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="mode", title="subcommands")

    ls_parser = subparsers.add_parser("ls", help="List available GPUs")
    ls_parser.add_argument("--ids", nargs="+", metavar="", help="List of GPU IDs to include")
    ls_parser.add_argument("--uuids", nargs="+", metavar="", help="List of GPU uuids to include")
    ls_parser.add_argument("--limit", type=int, default=999, help="Limit the number of the GPUs")
    ls_parser.add_argument("--mem-free-min", type=float, default=0.0, help="Minimum free memory (MB)")
    ls_parser.add_argument("--mem-util-max", type=float, default=100.0, help="Maximum memory usage (%)")
    ls_parser.add_argument("--gpu-util-max", type=float, default=100.0, help="Maximum GPU load (%)")
    ls_parser.add_argument("--sort", choices=["id", "gpu_util", "mem_util"], default="id", help="Sort by field")
    ls_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    ls_parser.add_argument("--debug", action="store_true", help="Show debug output")

    ps_parser = subparsers.add_parser("ps", help="Show GPU processes")
    ps_parser.add_argument("--ids", nargs="+", metavar="", help="GPU IDs to match")
    ps_parser.add_argument("--uuids", nargs="+", metavar="", help="GPU UUIDs to match")
    ps_parser.add_argument("--json", action="store_true", help="Output in JSON format")

    return parser


def _take(n, iterable):
    return it.islice(iterable, n)


def is_nvidia_smi_on_path():
    return shutil.which("nvidia-smi")


def _nvsmifs_ls(args):
    gpus_raw = list(get_gpus())

    if args.debug:
        print(f"[DEBUG] Raw GPU count: {len(gpus_raw)}")
        for gpu in gpus_raw:
            print("[DEBUG] Raw GPU:", gpu.__dict__)

    gpus = list(
        get_available_gpus(
            gpu_util_max=args.gpu_util_max,
            mem_util_max=args.mem_util_max,
            mem_free_min=args.mem_free_min,
            include_ids=args.ids,
            include_uuids=args.uuids,
        )
    )

    if args.debug:
        print(f"[DEBUG] Filtered GPU count: {len(gpus)}")

    gpus.sort(key=operator.attrgetter(args.sort))
    for gpu in _take(args.limit, gpus):
        print(gpu.to_json() if args.json else gpu)


def _nvsmifs_ps(args):
    processes = get_gpu_processes()
    for proc in processes:
        if not args.ids and not args.uuids:
            print(proc.to_json() if args.json else proc)
        elif (proc.gpu_id in args.ids) or (proc.gpu_uuid in args.uuids):
            print(proc.to_json() if args.json else proc)


def validate_ids_and_uuids(args):
    gpus = list(get_gpus())
    gpu_ids = {str(gpu.id) for gpu in gpus}
    gpu_uuids = {gpu.uuid for gpu in gpus}

    args.ids = set(str(i) for i in args.ids) if args.ids else set()
    args.uuids = set(args.uuids) if args.uuids else set()

    invalid_ids = args.ids.difference(gpu_ids)
    invalid_uuids = args.uuids.difference(gpu_uuids)

    if invalid_ids:
        sys.exit(f"Invalid GPU ids: {invalid_ids}")
    if invalid_uuids:
        sys.exit(f"Invalid GPU uuids: {invalid_uuids}")


def _main():
    parser = get_parser()
    args = parser.parse_args()

    if args.mode is None:
        parser.print_help()
        sys.exit(0)

    validate_ids_and_uuids(args)

    if args.mode == "ls":
        _nvsmifs_ls(args)
    elif args.mode == "ps":
        _nvsmifs_ps(args)


if __name__ == "__main__":
    if not is_nvidia_smi_on_path():
        sys.exit("Error: Couldn't find 'nvidia-smi' in PATH.")
    _main()


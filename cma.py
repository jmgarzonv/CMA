#!/usr/bin/python3
import click
import sys
from typing import List, Tuple, Optional, Union
from best_fit import best_fit

def print_memory_map(memory_map):
    for memory in memory_map:
        print(f"({memory[0]:#0{8}x}, {memory[1]:#0{8}x})")

def read_reqs_file(reqs_filename):
    result = []
    try:
        with open(reqs_filename, 'r') as reqsfile:
            for line in reqsfile:
                req = int(line.strip(),16)
                result.append(req)
    except FileNotFoundError:
        print(f'File not found {reqs_filename}', file=sys.stderr)
        return None
    else:
        return result

def read_memmap_file(memmap_filename):
    result = []
    try:
        with open(memmap_filename, 'r') as mmfile:
            for line in mmfile:
                elems = line.strip().split()
                result.append((int(elems[0],16), int(elems[1],16)))
    except FileNotFoundError:
        print(f'File not found {memmap_filename}', file=sys.stderr)
        return None
    else:
        return result

def cmas(algo_str):
    if algo_str == 'all':
        return [
            {"name" : "best fit",
             "function" : best_fit },
        ]
    elif algo_str == 'best':
        return [
            {"name" : "best fit",
             "function" : best_fit },
        ]
    else:
        return None

def bytes_to_mb(bytes_value: int) -> str:
    return f"{bytes_value / (1024 * 1024):.2f} MB"

@click.command()
@click.option('--memmap', help='file with the memory description')
@click.option('--reqs', help='requirement file')
@click.option('--function', default='all', help='Algorithm to Execute: first, best, worst, all')
@click.option('--pos', default=0, help='initial position')
def process(memmap, reqs, function, pos):
    memory = read_memmap_file(memmap)
    requirements = read_reqs_file(reqs)
    cont_mem_algo = cmas(function)
    if memory == None or requirements == None or cont_mem_algo == None:
        return

    first_pos = pos
    work_memory = memory[:]  # La memoria inicial se carga aquí y se actualiza después

    for cmae in cont_mem_algo:
        index = first_pos
        print(cmae["name"])
        print_memory_map(work_memory)

        for req in requirements:
            print(f"\nEvaluando requerimiento: {hex(req)} ({bytes_to_mb(req)})")
            search = cmae["function"](work_memory, req, index)
            if search is None:
                print(f"No se pudo asignar el requerimiento {hex(req)}.")
            else:
                work_memory, base, limit, index = search  # Actualizar work_memory con la memoria restante
                print("Asignación exitosa:")
                print(f"  - Base asignada: {hex(base)}")
                print(f"  - Límite asignado (Tamaño): {hex(limit)} ({bytes_to_mb(limit)})")
                print(f"  - Índice de la asignación: {index}")
                print(f"  - Memoria restante:")
                print_memory_map(work_memory)

if __name__ == '__main__':
    process()

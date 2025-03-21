from typing import List, Tuple, Optional, Union

def best_fit(mem_avail: List[Tuple[int, int]], req: Union[int, List[int]], index: int) -> Optional[Tuple[List[Tuple[int, int]], int, int, int]]:
    if not mem_avail:  # Si la memoria está vacía
        return None

    if isinstance(req, list):  # Procesar lista de requerimientos
        for single_req in req:
            result = best_fit(mem_avail, single_req, index)
            if result is None:
                return None
            mem_avail, base, _, index = result
        return (mem_avail, base, req[-1], index)

    index %= len(mem_avail)
    mejor_bloque = None
    mejor_indice = -1

    for i in range(len(mem_avail)):
        actual_index = (index + i) % len(mem_avail)
        base, limite = mem_avail[actual_index]

        if limite >= req:  # Si el tamaño es suficiente
            if mejor_bloque is None or limite < mejor_bloque[1]:
                mejor_bloque = (base, limite)
                mejor_indice = actual_index

    if mejor_bloque is None:
        return None

    base, limite = mejor_bloque
    nuevo_base = base + req  # Aumenta la posición base
    nuevo_limite = limite - req  # Reduce el tamaño del bloque

    nueva_mem_avail = mem_avail.copy()

    if nuevo_limite == 0:
        nueva_mem_avail.pop(mejor_indice)
    else:
        nueva_mem_avail[mejor_indice] = (nuevo_base, nuevo_limite)

    return (nueva_mem_avail, base, req, mejor_indice)

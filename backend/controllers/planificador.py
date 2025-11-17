from collections import deque

class Planificador:

    # ---------------------------------------------------------------
    #   ALGORITMO FCFS — First Come First Served
    # ---------------------------------------------------------------
    def fcfs(self, procesos):
        """
        MACROALGORITMO FCFS (First Come First Served)
        1. Ordenar procesos por tiempo de llegada.
        2. Ejecutar cada proceso hasta finalizar su ráfaga CPU.
        3. No existen interrupciones por tiempo (no expropiativo).
        4. Calcular tiempos de espera, finalización y retorno.
        """

        # Ordenar por tiempo de llegada
        procesos = sorted(procesos, key=lambda p: p.pcb.tiempo_llegada)

        tiempo_actual = 0
        resultados = []

        for proceso in procesos:
            pcb = proceso.pcb

            # Reset por si el proceso ya participó en otra simulación
            pcb.tiempo_restante = pcb.rafaga_original
            pcb.tiempo_espera = 0
            pcb.tiempo_inicio = None

            if tiempo_actual < pcb.tiempo_llegada:
                tiempo_actual = pcb.tiempo_llegada

            pcb.tiempo_espera = tiempo_actual - pcb.tiempo_llegada

            pcb.tiempo_inicio = tiempo_actual

            tiempo_actual += pcb.rafaga_original

            pcb.tiempo_finalizacion = tiempo_actual
            pcb.tiempo_retorno = pcb.tiempo_finalizacion - pcb.tiempo_llegada

            resultados.append(pcb.to_dict())

        return resultados



    # ---------------------------------------------------------------
    #   ALGORITMO ROUND ROBIN — CPU con quantum fijo
    # ---------------------------------------------------------------
    def round_robin(self, procesos, quantum=2):
        """
        MACROALGORITMO ROUND ROBIN
        1. Mantener una cola circular de procesos listos.
        2. Asignar quantum de tiempo a cada proceso.
        3. Si el proceso no termina, vuelve al final de la cola.
        4. Repetir hasta que todos finalicen.
        """

        for p in procesos:
            p.pcb.tiempo_restante = p.pcb.rafaga_original

        cola = deque(procesos)
        tiempo_actual = 0
        resultados = []

        while cola:
            proceso = cola.popleft()
            pcb = proceso.pcb

            # Si llega más tarde que el tiempo actual
            if tiempo_actual < pcb.tiempo_llegada:
                tiempo_actual = pcb.tiempo_llegada

            # Tiempo ejecutado = min(quantum, tiempo restante)
            ejecucion = min(quantum, pcb.tiempo_restante)

            # Registrar inicio si es la primera vez
            if pcb.tiempo_inicio is None:
                pcb.tiempo_inicio = tiempo_actual

            # Ejecutar
            pcb.tiempo_restante -= ejecucion
            tiempo_actual += ejecucion

            # Si terminó su CPU
            if pcb.tiempo_restante == 0:
                pcb.tiempo_finalizacion = tiempo_actual
                pcb.tiempo_retorno = pcb.tiempo_finalizacion - pcb.tiempo_llegada

                # Tiempo de espera = turnaround - rafaga_original
                pcb.tiempo_espera = pcb.tiempo_retorno - pcb.rafaga_original

                resultados.append(pcb.to_dict())
            else:
                # Todavía le falta: regresa a la cola
                cola.append(proceso)

        return resultados



    # ---------------------------------------------------------------
    #   ALGORITMO SJF — Shortest Job First
    # ---------------------------------------------------------------
    def sjf(self, procesos):
        """
        MACROALGORITMO SJF (Shortest Job First — No expropiativo)
        1. Ordenar procesos por ráfaga CPU más corta.
        2. Ejecutar completamente el proceso más corto.
        3. No expropiativo: no se interrumpe la ejecución.
        """

        # Ordenar por ráfaga CPU ascendente
        procesos = sorted(procesos, key=lambda p: p.pcb.rafaga_original)

        tiempo_actual = 0
        resultados = []

        for proceso in procesos:
            pcb = proceso.pcb

            # Reset por si ya fue ejecutado antes
            pcb.tiempo_restante = pcb.rafaga_original
            pcb.tiempo_espera = 0
            pcb.tiempo_inicio = None

            if tiempo_actual < pcb.tiempo_llegada:
                tiempo_actual = pcb.tiempo_llegada

            pcb.tiempo_espera = tiempo_actual - pcb.tiempo_llegada
            pcb.tiempo_inicio = tiempo_actual

            tiempo_actual += pcb.rafaga_original

            pcb.tiempo_finalizacion = tiempo_actual
            pcb.tiempo_retorno = tiempo_actual - pcb.tiempo_llegada

            resultados.append(pcb.to_dict())

        return resultados

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
        procesos = sorted(procesos, key=lambda p: (p.pcb.tiempo_llegada, p.pcb.pid)
)


        tiempo_actual = 0
        resultados = []

        for proceso in procesos:
            pcb = proceso.pcb

            # Si el proceso llega después, esperamos
            if tiempo_actual < pcb.tiempo_llegada:
                tiempo_actual = pcb.tiempo_llegada

            # Tiempo de espera antes de ejecutarse
            pcb.tiempo_espera = tiempo_actual - pcb.tiempo_llegada

            # Ejecutar por toda su ráfaga
            tiempo_actual += pcb.rafaga_original

            # Tiempo de finalización
            pcb.tiempo_finalizacion = tiempo_actual

            # Turnaround
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

        cola = deque(procesos)
        tiempo_actual = 0
        resultados = []

        while cola:
            proceso = cola.popleft()
            pcb = proceso.pcb

            # Si el proceso llega más tarde, avanzamos el tiempo
            if tiempo_actual < pcb.tiempo_llegada:
                tiempo_actual = pcb.tiempo_llegada

            # Tiempo ejecutado = min(quantum, ráfaga restante)
            ejecucion = min(quantum, pcb.tiempo_restante)

            pcb.tiempo_restante -= ejecucion
            tiempo_actual += ejecucion

            # Si terminó su CPU
            if pcb.tiempo_restante == 0:
                pcb.tiempo_finalizacion = tiempo_actual
                pcb.tiempo_retorno = pcb.tiempo_finalizacion - pcb.tiempo_llegada
                resultados.append(pcb.to_dict())
            else:
                # Regresa a cola para seguir en otro turno
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
        procesos = sorted(procesos, key=lambda p: (p.pcb.rafaga_cpu, p.pcb.pid)
        )

        tiempo_actual = 0
        resultados = []

        for proceso in procesos:
            pcb = proceso.pcb

            if tiempo_actual < pcb.tiempo_llegada:
                tiempo_actual = pcb.tiempo_llegada

            pcb.tiempo_espera = tiempo_actual - pcb.tiempo_llegada
            tiempo_actual += pcb.rafaga_original
            pcb.tiempo_finalizacion = tiempo_actual
            pcb.tiempo_retorno = tiempo_actual - pcb.tiempo_llegada

            resultados.append(pcb.to_dict())

        return resultados

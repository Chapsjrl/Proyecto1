#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk
from time import sleep
import threading
import psutil


cpu_num = psutil.cpu_count(logical=False)
carga_cpu = ()
stad_cpu = {}
stad_mem = ()
stad_vmem = ()
stad_procesos = []

campos = ('carga_cpu', 'stad_cpu', 'stad_mem', 'stad_vmem', 'stad_procesos')

mutex = {}
for i in campos:
    mutex[i] = threading.Semaphore(1)


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9.8K'
    >>> bytes2human(100001221)
    '95.4M'  
    Args:
        n (int) 
    Returns:
        str
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

def get_carga_cpu():
    global carga_cpu
    mutex['carga_cpu'].acquire()
    for cpu in range(cpu_num):
        carga_cpu[cpu] = psutil.cpu_percent(percpu=True)
    show_cargas()
    mutex['carga_cpu'].release()
    sleep(0.1)

def get_stad_cpu():
    global stad_cpu
    tiempo = psutil.cpu_times_percent(percpu=False)
    freqs = []
    tiempos = {
        'Usuario': tiempo.user,
        'Sistema': tiempo.system,
        'Inactivo': tiempo.idle
    }
    for freq in psutil.cpu_freq(percpu=True):
        freqs.append(freq.current)
    mutex['stad_cpu'].acquire()
    stad_cpu = {
        'tiempo': tiempos,
        'freq': freqs
    }
    mutex['stad_cpu'].release()
    sleep(0.1)

def get_usd_mem():
    global stad_mem
    mutex['stad_mem'].acquire()
    stad_mem = (
        bytes2human(psutil.virtual_memory().total),
        bytes2human(psutil.virtual_memory().used),
        psutil.virtual_memory().percent
    )
    mutex['stad_mem'].release()
    sleep(0.1)


def get_usd_vmem():
    global stad_vmem
    mutex['stad_vmem'].acquire()
    stad_vmem = (
        bytes2human(psutil.swap_memory().total),
        bytes2human(psutil.swap_memory().used),
        psutil.swap_memory().percent
    )
    mutex['stad_vmem'].release()
    sleep(0.1)


def get_procesos():
    global stad_procesos    
    mutex['stad_procesos'].acquire()
    for proceso in psutil.process_iter():
        try: 
            stad_procesos.append(proceso.as_dict(['pid', 'name', 'username','cpu_percent',
                                                  'memory_percent', 'status']))
        except psutil.NoSuchProcess:
            pass     
    show_procesos()
    mutex['stad_procesos'].release()


def show_procesos():
    if 'stad_procesos' in campos:
        num_procs = len(psutil.pids())
        for i in range(num_procs):
            variable.set(str(num_procs)+' Procesos en ejecución')
            treeProcesos.insert('', 'end', text=stad_procesos[i]['name'],
                                    values=(stad_procesos[i]['pid'],
                                            stad_procesos[i]['username'],
                                            stad_procesos[i]['cpu_percent'],
                                            stad_procesos[i]['memory_percent'],
                                            stad_procesos[i]['status']))
        ventana.after(1500, clear_procesos)

def clear_procesos():
    x = treeProcesos.get_children()
    if x != '()':
        for child in x:
            treeProcesos.delete(child)
    get_procesos()
            

def show_cargas():
    if 'carga_cpu' in campos:
        mutex['carga_cpu'].acquire()
        for cpu in range(cpu_num):
            percent = carga_cpu[cpu]
            prefijo = 'CPU%s' % str(cpu + 1)
            sufijo = '%04.1f%%' % percent
            cadena = prefijo + sufijo
            liststatus.insert(END, cadena)
            

    #     mutex['carga_cpu'].release()
    # if 'stad_cpu' in show:
    #     mutex['stad_cpu'].acquire()
    #     tiempos = stad_cpu['tiempo']
    #     freqs = stad_cpu['freq']
    #     mutex['stad_cpu'].release()
    # if 'stad_mem' in show:
    #     mutex['stad_mem'].acquire()
    #     total = stad_mem[0]
    #     usado = stad_mem[1]
    #     porciento = stad_mem[2]
    #     mutex['stad_mem'].release()
    #     usd_total = '%4s / %4s' % (usado, total)
    # if 'stad_vmem' in show:
    #     mutex['stad_vmem'].acquire()
    #     total = stad_vmem[0]
    #     usado = stad_vmem[1]
    #     porciento = stad_vmem[2]
    #     mutex['stad_vmem'].release()
    #     usd_total = '%4s / %4s' % (usado, total)
    


def main():
    thr_cpu_ld = threading.Thread(target=get_carga_cpu)
    thr_cpu_ld.start()
    # thr_cpu_st = threading.Thread(target=get_stad_cpu)
    # thr_cpu_st.start()
    # thr_swp_us =  threading.Thread(target=get_usd_vmem)
    # thr_swp_us.start()
    # thr_mem_us =  threading.Thread(target=get_usd_mem)
    # thr_mem_us.start()
    thr_prc =  threading.Thread(target=get_procesos)
    thr_prc.start()

    # while 1:
    #     sleep(.5)
    #     clear_procesos()


ventana = Tk()
ventana.title("Proyecto 1: Monitor de SO")
ventana.iconbitmap(default='system-monitor.ico')
ventana.geometry("700x600+0+0")

note = ttk.Notebook(ventana, height=25)

tab1 = Frame(note)
tab2 = Frame(note)

note.add(tab1, text = "Procesos")
note.add(tab2, text = "Máquina")

treeProcesos = ttk.Treeview(tab1)

treeProcesos["columns"] = ("PId", "Usuario", "CPU %", "Memoria %", "Estado")

scrollProcesos = ttk.Scrollbar(tab1)
scrollProcesos.pack(side=RIGHT, fill=Y)

treeProcesos['yscrollcommand'] = scrollProcesos.set
treeProcesos.column("PId", width=100)
treeProcesos.column("Usuario", width=120)
treeProcesos.column("CPU %", width=90)
treeProcesos.column("Memoria %", width=90)
treeProcesos.column("Estado", width=72)
treeProcesos.heading("PId", text="PId")
treeProcesos.heading("Usuario", text="Usuario")
treeProcesos.heading("CPU %", text="% CPU")
treeProcesos.heading("Memoria %", text="% Memoria")
treeProcesos.heading("Estado", text="Estado")

for i in treeProcesos.get_children():
    treeProcesos.delete(i)


liststatus = Listbox(tab2, width=15)

variable=StringVar()        
lblstatus=Label(ventana, bd=1, state=ACTIVE, relief=SUNKEN, anchor=W,
                        textvariable=variable,
                        font=('arial',9,'normal'))

lblstatus.pack(side=BOTTOM, fill=X)        
treeProcesos.pack(side=LEFT, fill=BOTH, expand=1)
liststatus.pack(side=LEFT, fill=Y)
note.pack(side=LEFT, fill=BOTH, expand=1)
scrollProcesos.config(command=treeProcesos.yview)
ventana.after(1500, clear_procesos)
ventana.mainloop()
import os
import curses
import pycfg
from pyarch import load_binary_into_memory
from pyarch import cpu_t


class os_t:
    def __init__(self, cpu, memory, terminal):
        self.cpu = cpu
        self.memory = memory
        self.terminal = terminal

        self.terminal.enable_curses()

        self.console_str = ""
        self.terminal.console_print(
            "this is the console, type the commands here\n")

    def printk(self, msg):
        self.terminal.kernel_print("kernel: " + msg + "\n")

    def panic(self, msg):
        self.terminal.end()
        self.terminal.dprint("kernel panic: " + msg)
        self.cpu.cpu_alive = False
        #cpu.cpu_alive = False

    def interrupt_keyboard(self):
        key = self.terminal.get_key_buffer()

        if ((key >= ord('a')) and (key <= ord('z'))) or ((key >= ord('A')) and (key <= ord('Z'))) or ((key >= ord('0')) and (key <= ord('9'))) or (key == ord(' ')) or (key == ord('-')) or (key == ord('_')) or (key == ord('.')):
            self.console_str = self.console_str + chr(key)
            self.terminal.console_print("\r" + self.console_str)
        elif key == curses.KEY_BACKSPACE:
            self.console_str = self.console_str[:-1]
            self.terminal.console_print("\r" + self.console_str)
        elif (key == curses.KEY_ENTER) or (key == ord('\n')):
            self.console_comandos()
            self.interpret_cmd(self.console_str)
            self.console_str = ""
            self.terminal.console_print("\r")

    def handle_interrupt(self, interrupt):
        if interrupt == pycfg.INTERRUPT_KEYBOARD:
            self.interrupt_keyboard()

    def interpret_cmd(self, cmd):
        if cmd == "exit":
            self.cpu.cpu_alive = False

    def syscall(self):
        # self.terminal.app_print(msg)
        return

    def console_comandos(self):
        comando = self.console_str.split(" ")

        if(self.console_str == "msg"):
            if(comando[0] == "msg"):
                self.interpret_cmd(self.console_str)
                self.console_str = ""
                #self.terminal.console_print(" Mensagem Exibida!...")
                self.printk("Mensagem Exibida!...")
                #self.terminal.end()
                #self.cpu.cpu_alive = False
            return

        if(comando[0] == "start" and len(comando) == 2):
            self.terminal.console_print("\nCarregando..."+comando[1])

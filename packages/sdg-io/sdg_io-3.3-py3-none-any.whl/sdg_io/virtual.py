import threading
import queue
import time
from sdg_utils import dump_bytes, log_starttime


def _dumptime():
    return (time.time() - log_starttime()) * 1000


class VirtualIO(threading.Thread):
    """
        Перенаправляет данные из основного интерфейса в виртуальные и обратно.
        Виртуальные интерфейсы имеют такие же методы что и обычный SDG_IO.
        Каждый Виртуальный интерфейс может иметь эксклюзивный адрес (первый байт сообщения)
        тогда ему долетаю только сообщения с этим адресом, а при отправке автоматический
        добавляется адрес.
    """

    def __init__(self, main_io, log=None, dump=None, rxtimeout=0.02):
        threading.Thread.__init__(self)
        self.__exit = False
        self.io = main_io
        self.virtual_io_without_addr = []
        self.virtual_io_with_addr = {}
        self.log = log
        self.dump = open(dump, 'w') if dump else None
        self.selfvio = self.get_child()  # создаем первый виртуальный интерфейс, read/write будут работать с ним
        self.rxtimeout = rxtimeout
        self.start()

    def run(self):
        while not self.__exit:
            # --- write ---
            allvio = self.virtual_io_without_addr + list(self.virtual_io_with_addr.values())
            for vio in allvio:
                while not vio.q_wr.empty():
                    ts = vio.q_wr.get(block=False)
                    try:
                        self.io.write(vio.addr + ts)
                        if self.dump:
                            self.dump.write("%d>%s\n" % (_dumptime(), dump_bytes(vio.addr + ts)))
                            self.dump.flush()
                    except IOError as e:  # перенаправляем исключения в виртуальный интерфейс
                        vio.Exception = e
                        self.__exit = True
                        if self.log:
                            self.log.error(f"vio wr err > {vio.Exception}")
            # --- read ---
            try:
                msg = self.io.read(timeout=self.rxtimeout)
            except IOError as e:  # перенаправляем исключения в виртуальные интерфейсы
                for vio in allvio:
                    vio.Exception = e
                    self.__exit = True
                    if self.log:
                        self.log.error(f"vio rd err > {vio.Exception}")
            else:
                if msg:
                    if self.dump:
                        self.dump.write("%d<%s\n" % (_dumptime(), dump_bytes(msg)))
                        self.dump.flush()

                    # Адресное сообщение
                    if msg[0] in self.virtual_io_with_addr:
                        vio = self.virtual_io_with_addr[msg[0]]
                        try:
                            vio.q_rd.put(msg[1:], block=False)
                        except queue.Full:
                            vio.qoverfl += 1
                            if self.log:
                                self.log.warning(f"queue ch{vio.addr} Full {vio.qoverfl}")

                    else:  # адрес не совпадает
                        if msg[0] == 0x00:  # Широковещательное сообщение
                            for i in self.virtual_io_with_addr:
                                vio = self.virtual_io_with_addr[i]
                                try:
                                    vio.q_rd.put(msg[1:], block=False)
                                except queue.Full:
                                    vio.qoverfl += 1
                                    if self.log:
                                        self.log.warning(f"queue ch{vio.addr} Full {vio.qoverfl}")

                        # передаем во все безадресные каналы
                        for vio in self.virtual_io_without_addr:
                            try:
                                vio.q_rd.put(msg, block=False)
                            except queue.Full:
                                vio.qoverfl += 1
                                if self.log:
                                    self.log.warning(f"queue ch{vio.addr} Full {vio.qoverfl}")

    def get_child(self, addr: bytes = None, log=None, dump=None):
        io_ch = self.VirtualIOchannel(addr=addr, log=log, dump=dump)
        if addr:  # чтобы быстро искать по адресу канала
            self.virtual_io_with_addr[addr[0]] = io_ch
        else:  #
            self.virtual_io_without_addr.append(io_ch)
        return io_ch

    def close(self):
        self.__exit = True
        if self.dump:
            self.dump.close()
        self.join()
        for vio in self.virtual_io_without_addr:
            vio.close()
        for vio in self.virtual_io_with_addr.values():
            vio.close()

    def read(self, timeout=0.1):
        return self.selfvio.read(timeout)

    def write(self, msg):
        return self.selfvio.write(msg)

    def drop(self):
        return self.selfvio.drop()

    class VirtualIOchannel:
        """ Прикидывается отдельным интерфейсом """

        def __init__(self, addr=None, log=None, dump=None):
            self.addr = addr or bytes()
            self.q_rd = queue.Queue(maxsize=1024*128)
            self.q_wr = queue.Queue()
            self.qoverfl = 0
            self.Exception = None
            self.log = log
            self.dump = None
            self.dump = open(dump, 'w') if dump else None

        def read(self, timeout=.01):
            if self.Exception:
                raise IOError(f"vio rd err > {self.Exception}")
            try:
                msg = self.q_rd.get(block=True, timeout=timeout)
            except queue.Empty:
                msg = b''
            else:
                if self.dump:
                    self.dump.write("%d<%s\n" % (_dumptime(), dump_bytes(msg)))
                    self.dump.flush()
            return msg

        def write(self, msg: bytes):
            if self.Exception:
                raise IOError(f"vio wr err > {self.Exception}")
            self.q_wr.put(msg)
            if self.dump:
                self.dump.write("%d>%s\n" % (_dumptime(), dump_bytes(msg)))
                self.dump.flush()

        def drop(self):
            def qclear(q):
                while not q.empty():
                    q.get(block=False)
            qclear(self.q_rd)
            qclear(self.q_wr)

        def close(self):
            if self.dump:
                self.dump.close()
            if self.log:
                self.log.info("close")


# if __name__ == '__main__':
#     logger = log_open()
#     io = SdgIO(port='COM13', portcfg='2000000_O_1')
#     virtio = VirtualIO(io)
#     stend_io = virtio.new_virtual_io(b'\x55', log=logger.getChild('stend'))
#     asuno_io = virtio.new_virtual_io(b'\xAA', log=logger.getChild('asuno'))
#     while 1:
#         stend_io.write(b'\x55\x00\x00\x00\x00')
#         asuno_io.write(b'\x11\x11\x11\x11')
#         time.sleep(1)
#         rx = stend_io.read()
#         rx = asuno_io.read()

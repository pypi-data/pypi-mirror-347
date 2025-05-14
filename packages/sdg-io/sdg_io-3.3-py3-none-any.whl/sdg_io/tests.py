import unittest
from time import sleep

from build.lib.sdg_dev import BROADCAST
from sdg_io import SdgIO, VirtualIO
from sdg_utils import rand_bytes, log_init


class TestProtocol(unittest.TestCase):
    print("Для выполнения теста нужно замкуть RX и TX порта (нуль-модем)")
    PORT = input("Ведите название порта 'нуль-модема' или нажмите Enter(по умочанию 'COM7'):")
    print(PORT)
    CNT = input("И кол-во циклов теста случайными пакетами или нажмите Enter(по умолчанию 1000):")
    if not PORT:
        PORT = 'COM7'
    try:
        CNT = int(CNT)
    except ValueError:
        CNT = 1000
    print(CNT)
    log = log_init()

    def test_random_msgs(self):
        self.log.info(""" Тест случайными данными. """)
        p = SdgIO(self.PORT, '115200_O_2', self.log)
        for i in range(self.CNT):
            msg = rand_bytes(mtu=256)
            p.write(msg)
            ack = p.read(timeout=.3)
            self.assertEqual(msg, ack)
        p.close()

    def test_drop(self):
        self.log.info(""" Тест функции Drop() """)
        p = SdgIO(self.PORT, '115200_O_2', self.log)
        msg = rand_bytes(mtu=256)
        p.write(msg)
        sleep(.1)
        ack = p.read(timeout=.1)
        self.assertEqual(ack, msg)
        p.write(msg)
        sleep(.1)
        p.drop()
        ack = p.read(timeout=.1)
        self.assertEqual(ack, b'')
        p.close()

    def test_multisend(self):
        self.log.info(""" Передача/прием сообщений пачками """)
        p = SdgIO(self.PORT, '115200_O_2', self.log)
        for _ in range(100):
            msgs = [rand_bytes(mtu=32) for _ in range(10)]
            for msg in msgs:
                p.write(msg)
            acks = []
            sleep(.1)
            for _ in range(len(msgs)):
                acks.append(p.read(timeout=0))
            self.assertEqual(msgs, acks)
        p.close()

    def test_virtualio1(self):
        self.log.info(""" Тест virtualio1. """)
        p = SdgIO(self.PORT, '115200_O_2', self.log)
        vio = VirtualIO(p, self.log.getChild('vio'))
        for i in range(self.CNT):
            msg = rand_bytes(mtu=256)
            vio.write(msg)
            self.assertEqual(msg, vio.read(timeout=.1))

        v1 = vio.get_child(addr=b'\x55')
        for i in range(self.CNT):
            msg = rand_bytes(mtu=256)
            v1.write(msg)
            self.assertEqual(msg, v1.read(timeout=.1))
            self.assertEqual(b'', vio.read(timeout=.1))
        vio.close()
        p.close()

    def test_virtualio2(self):
        self.log.info(""" Тест virtualio2. """)
        p = SdgIO(self.PORT, '115200_O_2', self.log)
        vio = VirtualIO(p, self.log.getChild('vio'))
        v1 = vio.get_child(addr=b'\x01')
        v2 = vio.get_child(addr=b'\x02')
        v3 = vio.get_child(addr=None)
        msg = rand_bytes(mtu=256)
        vio.write(msg)
        self.assertEqual(msg, vio.read(timeout=.1))
        self.assertEqual(b'', v1.read(timeout=.1))
        self.assertEqual(b'', v2.read(timeout=.1))
        self.assertEqual(msg, v3.read(timeout=.1))

        msg = rand_bytes(mtu=256)
        v1.write(msg)
        self.assertEqual(msg, v1.read(timeout=.1))
        self.assertEqual(b'', v2.read(timeout=.1))
        self.assertEqual(b'', vio.read(timeout=.1))
        self.assertEqual(b'', v3.read(timeout=.1))

        msg = rand_bytes(mtu=256)
        v2.write(msg)
        self.assertEqual(b'', v1.read(timeout=.1))
        self.assertEqual(msg, v2.read(timeout=.1))
        self.assertEqual(b'', vio.read(timeout=.1))
        self.assertEqual(b'', v3.read(timeout=.1))

        msg = rand_bytes(mtu=256)
        v3.write(BROADCAST + msg)
        self.assertEqual(msg, v1.read(timeout=.1))
        self.assertEqual(msg, v2.read(timeout=.1))
        self.assertEqual(BROADCAST + msg, vio.read(timeout=.1))
        self.assertEqual(BROADCAST + msg, v3.read(timeout=.1))

        msg = rand_bytes(mtu=256)
        vio.write(BROADCAST + msg)
        self.assertEqual(msg, v1.read(timeout=.1))
        self.assertEqual(msg, v2.read(timeout=.1))
        self.assertEqual(BROADCAST + msg, vio.read(timeout=.1))
        self.assertEqual(BROADCAST + msg, v3.read(timeout=.1))
        vio.close()
        p.close()

    def test_fail_cfg_parametrs(self):
        self.log.info(""" Тест некорректной инициализации порта. """)
        with self.assertRaises(IOError):
            SdgIO(port='NoCOM5', portcfg='115200_O_2', log=self.log)
        with self.assertRaises(ValueError):
            SdgIO(port=self.PORT, portcfg='115200_X_2', log=self.log)
        with self.assertRaises(ValueError):
            SdgIO(port=self.PORT, portcfg='115200_O_5', log=self.log)
        with self.assertRaises(ValueError):
            SdgIO(port=self.PORT, portcfg='0_O_5', log=self.log)
        with self.assertRaises(ValueError):
            SdgIO(port=self.PORT, portcfg='OLOLO_O_5', log=self.log)
        with self.assertRaises(IndexError):
            SdgIO(port=self.PORT, portcfg='115200_O', log=self.log)
        with self.assertRaises(IndexError):
            SdgIO(port=self.PORT, portcfg='115200', log=self.log)
        # Обычно порты не поддерживают boudrate > 115200
        # pyserial генерирует SerialException конструктор Protocol-а его перехватывает
        # и генерирует исключение IOError, чтобы не плодить сущности
        # with self.assertRaises(IOError):
        #   SdgIO(port='COM1', portcfg='921600_O_1', log=self.log)


if __name__ == "__main__":
    unittest.main()

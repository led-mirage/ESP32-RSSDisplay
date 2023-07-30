"""
NTPモジュール

Copyright (c) 2023 led-mirage
"""
import machine
import ntptime
import utime


def synchronize_time(ntp_server="ntp.nict.jp", time_diff=9, retry_max=3):
    for i in range(retry_max):
        try:
            ntptime.host = ntp_server
            ntptime.settime()
            local_time = utime.time() + time_diff * 3600
            t = utime.localtime(local_time)
            machine.RTC().datetime((t[0], t[1], t[2], 0, t[3], t[4], t[5], t[6]))
            return True
        except Exception as e:
            print(e)
    return False

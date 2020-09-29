"""
Created on 28 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
from scs_core.aws.monitor.device_monitor import DeviceMonitor
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------
def run_device_monitor(interval):
    dm = DeviceMonitor(interval, Host)
    dm.get_watched_device_list()
    dm.get_changed_devices_list()
    dm.send_email_alerts()
# --------------------------------------------------------------------------------------------------------------------


run_device_monitor(10)


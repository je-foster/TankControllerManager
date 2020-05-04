import platform
import subprocess
from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(protocol='IPv4', unique=True)
    mac = models.CharField(max_length=17, primary_key=True)
    notes = models.TextField()

    @property
    def online(self):
        return ping(self.ip)

class Datum(models.Model):
    class Meta:
        unique_together = (('device', 'time'))
        verbose_name_plural = "Data"

    device = models.ForeignKey(Device, db_index=True, \
        on_delete=models.CASCADE) # Deleting a device deletes all its data
    time = models.DateTimeField(auto_now=False, db_index=True)
    tankid = models.IntegerField()
    temp = models.FloatField()
    temp_setpoint = models.FloatField()
    pH = models.FloatField()
    pH_setpoint = models.FloatField()
    on_time = models.IntegerField()
    Kp = models.FloatField()
    Ki = models.FloatField()
    Kd = models.FloatField()

def ping(host):
    if host is None:
        return False

    # Chooses appropriate parameter depending on the platform
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

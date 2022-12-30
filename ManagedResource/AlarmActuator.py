from Alarm import Alarm

class AlarmActuator:
    @staticmethod
    def activeAlarm(alarm: Alarm):
        #  implement here listener from executor
        alarm.isActive = True

    @staticmethod
    def disableAlarm(alarm : Alarm):
        #  implement here listener from executor
        alarm.isActive = False
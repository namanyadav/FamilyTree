class TreeError:

    TYPE_ERROR = 'ERROR'
    TYPE_ANOMALY = 'ANOMALY'
    ON_INDI = 'INDIVIDUAL'
    ON_FAM = 'FAMILY'

    def __init__(self, err_type, err_on, err_us, err_on_id, err_msg):
        self.err_type = err_type
        self.err_on = err_on
        self.err_us = err_us
        self.err_on_id = err_on_id
        self.err_msg = err_msg

    def __str__(self):
        return f'{self.err_type}: {self.err_on}: {self.err_us}: {self.err_on_id}: {self.err_msg}'

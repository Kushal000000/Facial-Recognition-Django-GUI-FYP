from django.db import models

class AttendanceLog(models.Model):
    student_id = models.CharField(max_length=50)  # Updated to match varchar(50)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    date = models.DateTimeField(db_column='time_of_entry')  # Ensure correct mapping

    class Meta:
        db_table = 'attendance_logs'
        managed = False  # Prevents Django from overriding the existing MySQL table
        
# Define which database to use
class IOTRouter:
    def db_for_read(self, model, **hints):
        """Point all read operations on AttendanceLog to iot_db."""
        if model._meta.app_label == 'admin_panel':
            return 'iot_db'
        return None

    def db_for_write(self, model, **hints):
        """Point all write operations on AttendanceLog to iot_db."""
        if model._meta.app_label == 'admin_panel':
            return 'iot_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure Django does not create tables in the MySQL database."""
        if app_label == 'admin_panel':
            return db == 'iot_db'
        return None

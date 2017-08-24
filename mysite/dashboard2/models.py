from django.db import models

# Create your models here.


# class Config(models.Model):
#     machine_number = models.IntegerField(default=4)
#     customer_code = models.CharField(max_length=80)
#     app_key = models.CharField(max_length=80)
#     app_secret = models.CharField(max_length=80)
#     api_url = models.CharField(max_length=200)
#     simulation = models.IntegerField(default=0)
#     machine_name = models.CharField(max_length=200)
#     latest_value = models.IntegerField(default=20)

#     def __str__(self):
#         return self.customer_code


# class Machine(models.Model):
#     machine_id = models.CharField(max_length=80)
#     remark = models.CharField(max_length=200, blank=True)

#     def __str__(self):
#         return self.machine_id + " | " + self.remark


# class Tag(models.Model):
#     tag_id = models.CharField(max_length=80)
#     tag_text = models.CharField(max_length=80)
#     tag_unit = models.CharField(max_length=80, blank=True)
#     tag_scale = models.IntegerField(default=1)
#     remark = models.CharField(max_length=200, blank=True)

#     def __str__(self):
#         return self.tag_id + " | " + self.tag_text

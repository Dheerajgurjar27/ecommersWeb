from django.db import models

class Custmer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def register(self):
        self.save()

    def get_customer_by_email(email):
        try:
            return Custmer.objects.get(email = email)
        except:
            return False
    

    def isExists(self):
        if Custmer.objects.filter(email = self.email):
            return True
        return False
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Part(models.Model):
    names = ('Processor', 'CPU Cooler', 'Motherboard', 'Memory', 'Storage', 'GPU', 'Case', 'PSU', 'OS', 'Monitor')
    values = ('processor', 'cpu_cooler', 'motherboard', 'memory', 'storage', 'gpu', 'case', 'psu', 'os', 'monitor')
    part_type = models.CharField(max_length = 1000, choices=zip(names, names))
    title = models.CharField(max_length = 1000)
    image = models.CharField(max_length = 1000)
    currency = models.CharField(max_length=10, default='\u20b9')
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.title + '(' + self.part_type + ') - ' + self.currency + str(self.price)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    processor = models.ForeignKey(Part, null=True, blank=True, on_delete=models.CASCADE, related_name='processor' , limit_choices_to={'part_type': 'Processor'})
    cpu_cooler = models.ForeignKey(Part, null=True, blank=True, on_delete=models.CASCADE, related_name='cpu_cooler', limit_choices_to={'part_type': 'CPU Cooler'})
    motherboard = models.ForeignKey(Part, null=True, blank=True, on_delete=models.CASCADE, related_name='motherboard', limit_choices_to={'part_type': 'Motherboard'})
    memory = models.ForeignKey(Part, null=True, blank=True, on_delete=models.CASCADE, related_name='memory', limit_choices_to={'part_type': 'Memory'})
    storage = models.ForeignKey(Part, null=True, blank=True, on_delete=models.CASCADE, related_name='storage', limit_choices_to={'part_type': 'Storage'})
    gpu = models.ForeignKey(Part, null=True, blank=True, on_delete=models.CASCADE, related_name='gpu', limit_choices_to={'part_type': 'GPU'})
    case = models.ForeignKey(Part, null=True, blank=True, on_delete=models.CASCADE, related_name='case', limit_choices_to={'part_type': 'Case'})
    psu = models.ForeignKey(Part, null=True, blank=True, on_delete=models.CASCADE, related_name='psu', limit_choices_to={'part_type': 'PSU'})
    os = models.ForeignKey(Part, null=True, blank=True, on_delete=models.CASCADE, related_name='os', limit_choices_to={'part_type': 'OS'})
    monitor = models.ForeignKey(Part, null=True, blank=True, on_delete=models.CASCADE, related_name='monitor', limit_choices_to={'part_type': 'Monitor'})

    def __str__(self):
        return self.user.username

class Shopping_Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parts = models.ManyToManyField(Part, blank=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parts = models.ManyToManyField(Part, blank=True)
    date_time = models.DateTimeField(auto_now_add=True, null=True)

    def get_time(self):
        return self.date_time.time().strftime("%I:%M %p")

    def get_date(self):
        return self.date_time.date().strftime("%d-%b-%Y")

    def get_day(self):
        return self.date_time.date().strftime("%A - %d")
    
    def get_day_date(self):
        return self.date_time.date().strftime("%A %d, %b %Y")

    def __str__(self):
        return self.user.username + ' - ' + self.get_day_date()
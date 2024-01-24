from datetime import timezone
from django.db import models
from django.contrib.auth.models import User 
from django.utils.timezone import now
from geopy.geocoders import GoogleV3

# Create your models here.
class Expense(models.Model):
    cedula_ruc = models.TextField(max_length=15,blank=True, null=True, db_index=True)
    razon_social = models.CharField(max_length=255,blank=True, null=True, db_index=True)
    cuota_total = models.FloatField(blank=True, null=True)
    cuota_ult_fecha = models.DateField(blank=True, null=True)
    emitidas = models.IntegerField(blank=True, null=True)
    cuota_nro = models.IntegerField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fecha_inscripcion = models.DateField(blank=True, null=True)
    nombre_comercial = models.CharField(max_length=255,blank=True, null=True, db_index=True)
    actividad = models.CharField(max_length=255,blank=True, null=True)
    telefonos = models.CharField(max_length=20,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    pertenece_comite = models.CharField(max_length=255,blank=True, null=True)
    ultimo_pago = models.DateField(blank=True, null=True)
    dir_comercial = models.CharField(max_length=255,blank=True, null=True)
    dir_domicilio = models.CharField(max_length=255,blank=True, null=True)
    nmesesaportados = models.IntegerField(blank=True, null=True)
    nmesesvigencia = models.IntegerField(blank=True, null=True)
    tipo_socio = models.CharField(max_length=255,blank=True, null=True)
    recaudador = models.CharField(max_length=255,blank=True, null=True)
    genero = models.CharField(max_length=20,blank=True, null=True)
    linea_negocio = models.CharField(max_length=255,blank=True, null=True)
    estado = models.CharField(max_length=20,blank=True, null=True)
    aseguradora = models.CharField(max_length=255,blank=True, null=True)
    nacionalidad = models.CharField(max_length=255,blank=True, null=True)
    estado_civil = models.CharField(max_length=20,blank=True, null=True)
    movil = models.CharField(max_length=20,blank=True, null=True)
    nombre = models.CharField(max_length=255,blank=True, null=True, db_index=True)
    representantelegal = models.CharField(max_length=255,blank=True, null=True, db_index=True)
    conyuge = models.CharField(max_length=255, blank=True, null=True)
    fechaactualizacion = models.DateField(blank=True, null=True)
    fechaultimafact = models.DateField(blank=True, null=True)
    idclase = models.CharField(max_length=255,blank=True, null=True)
    fecha_ultima_factura = models.DateField(blank=True, null=True)

    latitud_comercial = models.FloatField(blank=True, null=True)
    longitud_comercial = models.FloatField(blank=True, null=True)
    
    latitud_domicilio = models.FloatField(blank=True, null=True)
    longitud_domicilio = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        geolocator = GoogleV3(api_key='AIzaSyAWcxXZO36iZusfLvs4CZeOLplPir5DlvY')

        if self.dir_comercial:
            location = geolocator.geocode(self.dir_comercial)
            if location:
                self.latitud_comercial = location.latitude
                self.longitud_comercial = location.longitude

        if self.dir_domicilio:
            location = geolocator.geocode(self.dir_domicilio)
            if location:
                self.latitud_domicilio = location.latitude
                self.longitud_domicilio = location.longitude

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cedula_ruc} - {self.razon_social}"
    

class Pago(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    mes = models.DateField()
    fecha = models.DateField()
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.monto} USD - {self.fecha}'

      
class TipoSocio(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre
    
class Genero(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre
    
class Lineas(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre
    
class Comite(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre

class EstadoCivil(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre

class Estado(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre
    
class Aseguradora(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre

class Recaudador(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre
    
class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre
    
class Clase(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre
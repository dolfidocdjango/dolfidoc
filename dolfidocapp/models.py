# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cardiologista(models.Model):
    nome = models.CharField(max_length=255, blank=True, null=True)
    crm = models.CharField(max_length=50, blank=True, null=True)
    uf = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(max_length=255, blank=True, null=True)
    nome_fantasia = models.CharField(max_length=255, blank=True, null=True)
    cnpj = models.CharField(max_length=255, blank=True, null=True)
    especialidade = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fid = models.CharField(max_length=255, blank=True, null=True)
    logradouro = models.CharField(max_length=255, blank=True, null=True)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    foto = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cardiologista'


class Config(models.Model):
    backgroundfoto = models.BinaryField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    feedback = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'config'

class Medicos(models.Model):
    nome = models.CharField(max_length=100)
    crm = models.CharField(max_length=50)
    situacao = models.CharField(max_length=50, blank=True, null=True)
    uf = models.CharField(max_length=5)
    cidade = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=150, blank=True, null=True)
    cnpj = models.CharField(max_length=30, blank=True, null=True)
    especialidade = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True, null=True)
    logradouro = models.CharField(max_length=150, blank=True, null=True)
    complemento = models.CharField(max_length=150, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medicos'

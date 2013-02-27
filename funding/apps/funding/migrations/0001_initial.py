# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BankAccount'
        db.create_table('funding_bankaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('funding', ['BankAccount'])


    def backwards(self, orm):
        # Deleting model 'BankAccount'
        db.delete_table('funding_bankaccount')


    models = {
        'funding.bankaccount': {
            'Meta': {'object_name': 'BankAccount'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['funding']
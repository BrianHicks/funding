# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BalancedAccount'
        db.create_table('funding_balancedaccount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('uri', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('funding', ['BalancedAccount'])


    def backwards(self, orm):
        # Deleting model 'BalancedAccount'
        db.delete_table('funding_balancedaccount')


    models = {
        'funding.balancedaccount': {
            'Meta': {'object_name': 'BalancedAccount'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['funding']
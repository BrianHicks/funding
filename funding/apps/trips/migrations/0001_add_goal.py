# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Goal'
        db.create_table('trips_goal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('what', self.gf('django.db.models.fields.TextField')()),
            ('where', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('amount_needed', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('due', self.gf('django.db.models.fields.DateTimeField')()),
            ('testimony', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('trips', ['Goal'])


    def backwards(self, orm):
        # Deleting model 'Goal'
        db.delete_table('trips_goal')


    models = {
        'trips.goal': {
            'Meta': {'object_name': 'Goal'},
            'amount_needed': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'testimony': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'what': ('django.db.models.fields.TextField', [], {}),
            'when': ('django.db.models.fields.DateTimeField', [], {}),
            'where': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        }
    }

    complete_apps = ['trips']
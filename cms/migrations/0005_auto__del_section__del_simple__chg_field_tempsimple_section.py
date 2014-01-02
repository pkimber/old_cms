# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Section'
        db.delete_table(u'cms_section')

        # Deleting model 'Simple'
        db.delete_table(u'cms_simple')


        # Changing field 'TempSimple.section'
        db.alter_column(u'cms_tempsimple', 'section_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.TempSection']))

    def backwards(self, orm):
        # Adding model 'Section'
        db.create_table(u'cms_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'cms', ['Section'])

        # Adding model 'Simple'
        db.create_table(u'cms_simple', (
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Section'])),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('moderated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'cms', ['Simple'])


        # Changing field 'TempSimple.section'
        db.alter_column(u'cms_tempsimple', 'section_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Section']))

    models = {
        u'cms.tempsection': {
            'Meta': {'object_name': 'TempSection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cms.tempsimple': {
            'Meta': {'object_name': 'TempSimple'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.TempSection']"}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cms']
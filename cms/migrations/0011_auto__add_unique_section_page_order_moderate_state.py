# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Section', fields ['page', 'order', 'moderate_state']
        db.create_unique(u'cms_section', ['page_id', 'order', 'moderate_state_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Section', fields ['page', 'order', 'moderate_state']
        db.delete_unique(u'cms_section', ['page_id', 'order', 'moderate_state_id'])


    models = {
        u'cms.moderatestate': {
            'Meta': {'ordering': "['name']", 'object_name': 'ModerateState'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        },
        u'cms.page': {
            'Meta': {'ordering': "['name']", 'object_name': 'Page'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'cms.section': {
            'Meta': {'ordering': "['page', 'order', 'modified']", 'unique_together': "(('page', 'order', 'moderate_state'),)", 'object_name': 'Section'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderate_state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.ModerateState']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cms.Page']"}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cms']
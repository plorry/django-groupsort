# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'NameList'
        db.create_table('groupsort_namelist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('groupsort', ['NameList'])

        # Adding model 'Person'
        db.create_table('groupsort_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('namelist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupsort.NameList'])),
        ))
        db.send_create_signal('groupsort', ['Person'])

        # Adding M2M table for field forbidden_pairings on 'Person'
        db.create_table('groupsort_person_forbidden_pairings', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_person', models.ForeignKey(orm['groupsort.person'], null=False)),
            ('to_person', models.ForeignKey(orm['groupsort.person'], null=False))
        ))
        db.create_unique('groupsort_person_forbidden_pairings', ['from_person_id', 'to_person_id'])

        # Adding model 'Pairing'
        db.create_table('groupsort_pairing', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_pairing', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('groupsort', ['Pairing'])

        # Adding M2M table for field people on 'Pairing'
        db.create_table('groupsort_pairing_people', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pairing', models.ForeignKey(orm['groupsort.pairing'], null=False)),
            ('person', models.ForeignKey(orm['groupsort.person'], null=False))
        ))
        db.create_unique('groupsort_pairing_people', ['pairing_id', 'person_id'])

        # Adding model 'Groups'
        db.create_table('groupsort_groups', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('namelist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['groupsort.NameList'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('groupsort', ['Groups'])

        # Adding M2M table for field people on 'Groups'
        db.create_table('groupsort_groups_people', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('groups', models.ForeignKey(orm['groupsort.groups'], null=False)),
            ('person', models.ForeignKey(orm['groupsort.person'], null=False))
        ))
        db.create_unique('groupsort_groups_people', ['groups_id', 'person_id'])


    def backwards(self, orm):
        
        # Deleting model 'NameList'
        db.delete_table('groupsort_namelist')

        # Deleting model 'Person'
        db.delete_table('groupsort_person')

        # Removing M2M table for field forbidden_pairings on 'Person'
        db.delete_table('groupsort_person_forbidden_pairings')

        # Deleting model 'Pairing'
        db.delete_table('groupsort_pairing')

        # Removing M2M table for field people on 'Pairing'
        db.delete_table('groupsort_pairing_people')

        # Deleting model 'Groups'
        db.delete_table('groupsort_groups')

        # Removing M2M table for field people on 'Groups'
        db.delete_table('groupsort_groups_people')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'groupsort.groups': {
            'Meta': {'object_name': 'Groups'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'namelist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groupsort.NameList']"}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['groupsort.Person']", 'null': 'True', 'blank': 'True'})
        },
        'groupsort.namelist': {
            'Meta': {'object_name': 'NameList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'groupsort.pairing': {
            'Meta': {'object_name': 'Pairing'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_pairing': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'pairings'", 'symmetrical': 'False', 'to': "orm['groupsort.Person']"})
        },
        'groupsort.person': {
            'Meta': {'object_name': 'Person'},
            'forbidden_pairings': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'forbidden_pairings_rel_+'", 'to': "orm['groupsort.Person']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'namelist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['groupsort.NameList']"})
        }
    }

    complete_apps = ['groupsort']

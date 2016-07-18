from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.http import JsonResponse

ACTIVITY_TYPE_CHOICES = (
    ('obs:Observation', 'obs:Observation'),
    ('obs:Reduction', 'obs:Reduction'),
    ('obs:Classification', 'obs:Classification'),
    ('obs:Crossmatch', 'obs:Crossmatch'),
    ('calc:ChemicalPipeline', 'calc:ChemicalPipeline'),
    ('calc:Distances', 'calc:Distances'),
    ('other', 'other'),
)

ENTITY_TYPE_CHOICES = (
    ('prov:Collection', 'prov:Collection'),
    ('voprov:dataSet', 'voprov:ctalog'),
)

#DATA_TYPE_CHOICES = (
#)

AGENT_TYPE_CHOICES = (
    ('voprov:Project','voprov:Project'),
    ('prov:Person','prov:Person'),
)

# main ProvDM classes:
@python_2_unicode_compatible
class Activity(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True) # should require this, otherwise do not know what to show!
    type = models.CharField(max_length=128, null=True, choices=ACTIVITY_TYPE_CHOICES)
    description = models.CharField(max_length=1024, blank=True, null=True)
    startTime = models.DateTimeField(null=True) # should be: null=False, default=timezone.now())
    endTime = models.DateTimeField(null=True) # should be: null=False, default=timezone.now())
    docuLink = models.CharField('documentation link', max_length=512, blank=True, null=True)

    def __str__(self):
        return self.label
        # maybe better use self.id here??

    def getjson(self, activity_id):
        activity_dict = {'id': id, 'label': label, 'type': type, 'description': description}
        return JsonResponse(activity_dict)

@python_2_unicode_compatible
class Entity(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True) # human readable label
    type = models.CharField(max_length=128, null=True, choices=ENTITY_TYPE_CHOICES) # types of entities: single entity, dataset
    description = models.CharField(max_length=1024, null=True, blank=True)
    status = models.CharField(max_length=128, null=True, blank=True)
    dataType= models.CharField(max_length=128, null=True, blank=True)
    storageLocation = models.CharField('storage location', max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.label

@python_2_unicode_compatible
class Agent(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True) # human readable label, firstname + lastname
    type = models.CharField(max_length=128, null=True, choices=AGENT_TYPE_CHOICES) # types of entities: single entity, dataset
    description = models.CharField(max_length=1024, null=True)

    def __str__(self):
        return self.label

# relation classes
@python_2_unicode_compatible
class Used(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(Activity, null=True) #, on_delete=models.CASCADE) # Should be required!
    entity = models.ForeignKey(Entity, null=True) #, on_delete=models.CASCADE) # Should be required!
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "id=%s; activity=%s; entity=%s; role=%s" % (str(self.id), self.activity, self.entity, self.role)

@python_2_unicode_compatible
class WasGeneratedBy(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(Entity, null=True) #, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, null=True) #, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "id=%s; entity=%s; activity=%s; role=%s" % (str(self.id), self.entity, self.activity, self.role)

@python_2_unicode_compatible
class HadMember(models.Model):
    id = models.AutoField(primary_key=True)
    collection = models.ForeignKey(Entity, null=True) #, on_delete=models.CASCADE) # enforce prov-type: collection
    entity = models.ForeignKey(Entity, related_name='collection', null=True) #, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "id=%s; collection=%s; entity=%s; role=%s" % (str(self.id), self.collection, self.entity, self.role)

@python_2_unicode_compatible
class WasDerivedFrom(models.Model):
    id = models.AutoField(primary_key=True)
    entity1 = models.ForeignKey(Entity, null=True) 
    entity2 = models.ForeignKey(Entity, related_name='entity1', null=True) #, on_delete=models.CASCADE)

    def __str__(self):
        return "id=%s; entity1=%s; entity2=%s" % (str(self.id), self.entity1, self.entity2)

@python_2_unicode_compatible
class WasAssociatedWith(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(Activity, null=True) 
    agent = models.ForeignKey(Agent, null=True) #, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "id=%s; activity=%s; agent=%s; role=%s" % (str(self.id), self.activity, self.agent, self.role)

@python_2_unicode_compatible
class WasAttributedTo(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(Entity, null=True) 
    agent = models.ForeignKey(Agent, null=True) #, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "id=%s; entity=%s; agent=%s; role=%s" % (str(self.id), self.entity, self.agent, self.role)


@python_2_unicode_compatible
class RaveObsids(models.Model):
    rave_obs_id = models.TextField(db_column='RAVE_OBS_ID', blank=True, null=True)  # Field name made lowercase.
    obsdate = models.TextField(db_column='Obsdate', blank=True, null=True)  # Field name made lowercase.
    fieldname = models.TextField(db_column='FieldName', blank=True, null=True)  # Field name made lowercase.
    platenumber = models.TextField(db_column='PlateNumber', blank=True, null=True)  # Field name made lowercase.
    fibernumber = models.TextField(db_column='FiberNumber', blank=True, null=True)  # Field name made lowercase.
    id_2mass = models.TextField(db_column='ID_2MASS', blank=True, null=True)  # Field name made lowercase.
    id_denis = models.TextField(db_column='ID_DENIS', blank=True, null=True)  # Field name made lowercase.
    obs_collection = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rave_obsids'

    def __str__(self):
        return "rave_obs_id=%s; obsdate=%s; fieldname=%s; id_2mass=%s; obs_collection=%s" % (str(self.rave_obs_id), self.obsdate, self.fieldname, self.id_2mass, self.obs_collection)


    def get_sparvfile(self, rave_obs_id):
        basepath = "corvus.aip.de:/store/01/RAVE/Processing/DR4"
        namesplit = rave_obs_id.split('_')
        date = namesplit[0]
        fieldname = namesplit[1]
        platenumber = namesplit[2]
        filepath = date + "/"

        stn_file = filepath + fieldname + ".stn"
        uncorrspec_file = filepath + filedname + ".rvsun." + platenumber + ".nocont.txt"
        corrspec_file = filepath + filedname + ".rvsun." + platenumber + ".cont.txt"

        # would need more metadata here!

        return {'stn_file': stn_file, 'uncorrspec_file': uncorrspec_file,
                'corrspec_file': corrspec_file}


    def get_reducedfile(self, rave_obs_id):
        # extract year, month and day from the file name:
        namesplit = rave_obs_id.split('_')
        year = namesplit[0][0:4]
        month = namesplit[0][4:6]
        day = namesplit[0][6:8]
        field = namesplit[1]
        num = namesplit[2]
        basepath = "corvus.aip.de:/store/01/Data_RAVE_s"
        filepath = basepath + "/" + "RAVE/reduced_IRAF/" + str(year) + "/"\
            + namesplit[0] + "/" + field
        reduced_file = filepath + ".rvsun.fts"
        sky_file = filepath + ".sky.fts"
        usky_file = filepath + ".usky.fts"
        #"RAVE/reduced_IRAF/2012/20121220/0752m38.rvsun.fts"
        return {'reduced_file': reduced_file, 'sky_file': sky_file,
                'usky_file': usky_file}


    def get_originalfiles(self, rave_obs_id):
        namesplit = rave_obs_id.split('_')
        date = namesplit[0]
        fieldname = namesplit[1]
        platenumber = namesplit[2]

        basepath = "corvus.aip.de:/store/01/Data_RAVE_s/RAVE_ORIG"
        filepath = basepath + "/" + date + "/" + fieldname + "*.fits"

        return {'originalfiles': filepath}
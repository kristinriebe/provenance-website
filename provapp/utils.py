from .models import Activity, Entity, Agent, Used, WasGeneratedBy
from .models import WasAssociatedWith, WasAttributedTo, HadMember, WasDerivedFrom
from .models import RaveObsids


# some helper functions
def find_entity_basic_graph(entity, prov):

    # track the provenance information backwards, but only for collections!
    if "prov:collection" in entity.type.split(';'):
        queryset = WasGeneratedBy.objects.filter(entity=entity.id)

        if (len(queryset) == 0):
            # nothing found
            pass
        elif (len(queryset) > 1):
            raise ValueError("More than one wasGeneratedBy-relation found. Does this make any sense?")
        elif (len(queryset) == 1):
            wg = queryset[0]
            print "Entity " + entity.id + " wasGeneratedBy activity: ", wg.activity.id

            # add activity to prov-json for graphics, if not yet done
            # (use map_activity_ids for easier checking)

            if wg.activity.id not in prov['map_nodes_ids']:
                prov['nodes_dict'].append({'name': wg.activity.name, 'type': 'activity'})
                prov['map_nodes_ids'][wg.activity.id] = prov['count_nodes']
                prov['count_nodes'] = prov['count_nodes'] + 1

                # follow provenance along this activity
                prov = find_activity_basic_graph(wg.activity, prov)

            # add wasGeneratedBy-link
            prov['links_dict'].append({"source": prov['map_nodes_ids'][wg.entity.id], "target": prov['map_nodes_ids'][wg.activity.id], "value": 0.2, "type": "wasGeneratedBy"})
            prov['count_link'] = prov['count_link'] + 1

            # there should be only ONE activity (or -collection)
            # that generated this entity

    # if no direct path backwards available, check membership to collection and
    # follow the collection's provenance
    # (Do it even if direct path was available!)
    queryset = HadMember.objects.filter(entity=entity.id)

    if (len(queryset) == 0):
        # nothing found, pass
        pass
    else:
        # can entities belong to more than one collection?
        # I think it cannot be excluded
        for h in queryset:
            print "Entity "+ entity.id + " is member of collection: ", h.collection.id

            # add entity to prov-json, if not yet done
            if h.collection.id not in prov['map_nodes_ids']:
                prov['nodes_dict'].append({'name': h.collection.name, 'type': 'entity'})
                prov['map_nodes_ids'][h.collection.id] = prov['count_nodes']
                prov['count_nodes'] = prov['count_nodes'] + 1

                # follow this collection's provenance (if it was not recorded before)
                prov = find_entity_basic_graph(h.collection, prov)
            else:
                # just find it's id:
                id1 = prov['map_nodes_ids'] # not needed, is found below anyway

            # add hadMember-link:
            # but only, if not yet recorded -> how to check?
            prov['links_dict'].append({"source": prov['map_nodes_ids'][h.collection.id], "target": prov['map_nodes_ids'][h.entity.id], "value": 0.2, "type": "hadMember"})
            prov['count_link'] = prov['count_link'] + 1


    queryset = WasDerivedFrom.objects.filter(generatedEntity=entity.id)
    # this relation is unique, there can be only one ... or not?
    if (len(queryset) == 0):
        pass
    elif (len(queryset) > 1):
        raise ValueError("More than one wasDerivedFrom-relation found. Does this make any sense?")
    else:
        wd = queryset[0]
        print "Entity " + entity.id + " wasDerivedFrom entity ", wd.usedEntity.id

        # use entity only, if it is a collection
        if "prov:collection" in entity.type.split(';'):

            # add entity to prov-json, if not yet done
            if wd.usedEntity.id not in prov['map_nodes_ids']:
                prov['nodes_dict'].append({'name': wd.usedEntity.name, 'type': 'entity'})
                prov['map_nodes_ids'][wd.usedEntity.id] = prov['count_nodes']
                prov['count_nodes'] = prov['count_nodes'] + 1

                # continue with pre-decessor
                prov = find_entity_basic_graph(wd.usedEntity, prov)

            # add hadMember-link (in any case)
            prov['links_dict'].append({"source": prov['map_nodes_ids'][entity.id], "target": prov['map_nodes_ids'][wd.usedEntity.id], "value": 0.2, "type": "wasDerivedFrom"})
            prov['count_link'] = prov['count_link'] + 1


    # if nothing found until now, then I have reached an endpoint in the graph
    #print "Giving up, no more provenance for entity found."
    return prov


def find_entity_detail_graph(entity, prov):
# no collections
    if "prov:collection" not in entity.type.split(';'):
        # track the provenance information backwards
        queryset = WasGeneratedBy.objects.filter(entity=entity.id)
        print "queryset: ", queryset
        if (len(queryset) == 0):
            # nothing found
            pass
        elif (len(queryset) > 1):
            raise ValueError("More than one wasGeneratedBy-relation found. Does this make any sense?")
        elif (len(queryset) == 1):
            wg = queryset[0]
            print "Entity " + entity.id + " wasGeneratedBy activity: ", wg.activity.id

            # add activity to prov-json for graphics, if not yet done
            # (use map_activity_ids for easier checking)

            if wg.activity.id not in prov['map_nodes_ids']:
                prov['nodes_dict'].append({'name': wg.activity.name, 'type': 'activity'})
                prov['map_nodes_ids'][wg.activity.id] = prov['count_nodes']
                prov['count_nodes'] = prov['count_nodes'] + 1

                # follow provenance along this activity
                prov = find_activity_detail_graph(wg.activity, prov)

            # add wasGeneratedBy-link
            prov['links_dict'].append({"source": prov['map_nodes_ids'][wg.entity.id], "target": prov['map_nodes_ids'][wg.activity.id], "value": 0.2, "type": "wasGeneratedBy"})
            prov['count_link'] = prov['count_link'] + 1


            # there should be only ONE activity (or -collection)
            # that generated this entity

        # if no direct path backwards available, check membership to collection and
        # follow the collection's provenance
        # (do NOT do it if direct path was available!)
        queryset = HadMember.objects.filter(entity=entity.id)

        if (len(queryset) == 0):
            # nothing found, pass
            pass
        else:
            # can entities belong to more than one collection?
            # I think it cannot be excluded
            for h in queryset:
                print "Entity "+ entity.id + " is member of collection: ", h.collection.id

                # add entity to prov-json, if not yet done
                if h.collection.id not in prov['map_nodes_ids']:
                    prov['nodes_dict'].append({'name': h.collection.name, 'type': 'entity'})
                    prov['map_nodes_ids'][h.collection.id] = prov['count_nodes']
                    prov['count_nodes'] = prov['count_nodes'] + 1

                    # follow this collection's provenance (if it was not recorded before)
                    prov = find_entity_detail_graph(h.collection, prov)
                else:
                    # just find it's id:
                    id1 = prov['map_nodes_ids'] # not needed, is found below anyway

                # add hadMember-link:
                # but only, if not yet recorded -> how to check?
                prov['links_dict'].append({"source": prov['map_nodes_ids'][h.collection.id], "target": prov['map_nodes_ids'][h.entity.id], "value": 0.2, "type": "hadMember"})
                prov['count_link'] = prov['count_link'] + 1


        queryset = WasDerivedFrom.objects.filter(generatedEntity=entity.id)
        # this relation is unique, there can be only one ... or not?
        if (len(queryset) == 0):
            pass
        elif (len(queryset) > 1):
            raise ValueError("More than one wasDerivedFrom-relation found. Does this make any sense?")
        else:
            wd = queryset[0]
            print "Entity " + entity.id + " wasDerivedFrom entity ", wd.usedEntity.id

            # add entity to prov-json, if not yet done
            if wd.usedEentity.id not in prov['map_nodes_ids']:
                prov['nodes_dict'].append({'name': wd.usedEntity.name, 'type': 'entity'})
                prov['map_nodes_ids'][wd.usedEentity.id] = prov['count_nodes']
                prov['count_nodes'] = prov['count_nodes'] + 1

                # continue with pre-decessor
                prov = find_entity_detail_graph(wd.usedEntity, prov)

            # add hadMember-link (in any case)
            prov['links_dict'].append({"source": prov['map_nodes_ids'][entity.id], "target": prov['map_nodes_ids'][wd.usedEntity.id], "value": 0.2, "type": "wasDerivedFrom"})
            prov['count_link'] = prov['count_link'] + 1

    # if nothing found until now, then I have reached an endpoint in the graph
    #print "Giving up, no more provenance for entity found."
    return prov


def find_activity_detail_graph(activity, prov):
# detail = no collections
    queryset = Used.objects.filter(activity=activity.id)

    # There definitely can be more than one used-relation
    if len(queryset) > 0:
        for u in queryset:
            if "prov:collection" not in u.entity.type.split(';'):
                print "Activity " + activity.id + " used entity ", u.entity.id
                # add entity to prov-json, if not yet done
                if u.entity.id not in prov['map_nodes_ids']:
                    prov['nodes_dict'].append({'name': u.entity.name, 'type': 'entity'})
                    prov['map_nodes_ids'][u.entity.id] = prov['count_nodes']
                    prov['count_nodes'] = prov['count_nodes'] + 1

                    # follow this entity's provenance
                    prov = find_entity_detail_graph(u.entity, prov)

                # add used-link:
                prov['links_dict'].append({"source": prov['map_nodes_ids'][activity.id], "target": prov['map_nodes_ids'][u.entity.id], "value": 0.2, "type": "used"})
                prov['count_link'] = prov['count_link'] + 1


    #print "Giving up, no more provenance for activity found."
    return prov


def find_activity_basic_graph(activity, prov):
# basic = only collections
    queryset = Used.objects.filter(activity=activity.id)

    # There definitely can be more than one used-relation
    if len(queryset) > 0:
        for u in queryset:

            #if u.entity.type == "prov:collection":
            if "prov:collection" in u.entity.type.split(';'):
                print "Activity " + activity.id + " used entity ", u.entity.id
                # add entity to prov-json, if not yet done
                if (u.entity.id not in prov['map_nodes_ids']):
                    prov['nodes_dict'].append({'name': u.entity.name, 'type': 'entity'})
                    prov['map_nodes_ids'][u.entity.id] = prov['count_nodes']
                    prov['count_nodes'] = prov['count_nodes'] + 1

                    # follow this entity's provenance
                    prov = find_entity_basic_graph(u.entity, prov)

                # add used-link:
                prov['links_dict'].append({"source": prov['map_nodes_ids'][activity.id], "target": prov['map_nodes_ids'][u.entity.id], "value": 0.2, "type": "used"})
                prov['count_link'] = prov['count_link'] + 1

    #print "Giving up, no more provenance for activity found."
    return prov



def find_entity(entity, prov, follow=True):
    # Look for entity in all possible relations,
    # follow these relations further recursively.
    # If follow is False, then do not follow the relations any futher,
    # except for wasGeneratedBy-activity: here one more step is done
    # in order to find and record the used entities.

    # track the provenance information backwards via WasGeneratedBy
    queryset = WasGeneratedBy.objects.filter(entity=entity.id)
    for wg in queryset:
        print "Entity "+ entity.id + " wasGeneratedBy activity: ", wg.activity.id

        # add activity to prov-list, IF not existing there already
        if wg.activity.id not in prov['activity']:
            prov['activity'][wg.activity.id] = wg.activity

            # follow provenance along this activity
            if follow:
                prov = find_activity(wg.activity, prov, follow=True)
            #else:
            # follow only for one step
            #    prov = find_activity(wg.activity, prov, follow=False)

        # add wasGeneratedBy-link
        prov['wasGeneratedBy'][wg.id] = wg


    # track backwards via wasDerivedFrom
    queryset = WasDerivedFrom.objects.filter(generatedEntity=entity.id)
    for wd in queryset:
        print "Entity " + entity.id + " wasDerivedFrom entity ", wd.usedEntity.id

        # add entity to prov, if not yet done
        if wd.usedEntity.id not in prov['entity']:
            prov['entity'][wd.usedEntity.id] = wd.usedEntity

            # continue with pre-decessor
            if follow:
                prov = find_entity(wd.usedEntity, prov, follow=True)

        # add wasDerivedFrom-link (in any case)
        prov['wasDerivedFrom'][wd.id] = wd


    # check membership to collection
    queryset = HadMember.objects.filter(entity=entity.id)
    # actually, entities cannot belong to more than one collection,
    # but we'll allow it here for now ...
    for h in queryset:
        print "Entity "+ entity.id + " is member of collection: ", h.collection.id, follow

        # add entity to prov-json, if not yet done
        if h.collection.id not in prov['entity']:
            prov['entity'][h.collection.id] = h.collection

            # follow this collection's provenance (if it was not recorded before)
            if follow:
                prov = find_entity(h.collection, prov, follow=True)
            else:
                # only if there was no wasDerivedFrom and wasGeneratedBy so far,
                # only then follow the collection's provenance one more step
                if len(prov['wasGeneratedBy']) == 0 and len(prov['wasDerivedFrom']) == 0:
                    prov = find_entity(h.collection, prov, follow=False)
                pass

        # add hadMember-link:
        prov['hadMember'][h.id] = h


    # check agent relation (attribution)
    queryset = WasAttributedTo.objects.filter(entity=entity.id)
    for wa in queryset:
        print "Entity " + entity.id + " WasAttributedTo agent ", wa.agent.id

        if wa.agent.id not in prov['agent']:
            # add agent to prov
            prov['agent'][wa.agent.id] = wa.agent

        # add wasAttributedto relationship
        prov['wasAttributedTo'][wa.id] = wa

    # if nothing found until now, then I have reached an endpoint in the graph
    return prov


def find_activity(activity, prov, follow=True):

    queryset = Used.objects.filter(activity=activity.id)

    # There definitely can be more than one used-relation
    for u in queryset:
        # because only want details, no collection, return if it is a collection
        #if "prov:collection" in u.entity.type.split(';'):
        #    return prov
        print "Activity " + activity.id + " used entity ", u.entity.id

        # add entity to prov, if not yet done
        if u.entity.id not in prov['entity']:
            prov['entity'][u.entity.id] = u.entity

            # follow this entity's provenance
            if follow:
                prov = find_entity(u.entity, prov, follow=True)

        # add used-link:
        prov['used'][u.id] = u
    #print "Giving up, no more provenance for activity %s found." % activity.id

    # check agent relation (association)
    queryset = WasAssociatedWith.objects.filter(activity=activity.id)
    for wa in queryset:
        print "Agent " + wa.agent.id + " WasAssociatedWith activity ", wa.activity.id

        if wa.agent.id not in prov['agent']:
            # add agent to prov
            prov['agent'][wa.agent.id] = wa.agent

        # add relationship to prov
        prov['wasAssociatedWith'][wa.id] = wa

    return prov

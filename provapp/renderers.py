from __future__ import unicode_literals

from django.utils.encoding import smart_text
from django.utils.encoding import smart_unicode
from rest_framework.renderers import BaseRenderer
from django.utils import timezone


class PROVNBaseRenderer(BaseRenderer):

    def get_value(self, obj, key):
        marker = "-"

        if key in obj:
            return str(obj.pop(key))
        else:
            return marker



class ActivityPROVNRenderer(PROVNBaseRenderer):

    def render(self, activity):
        string = "activity("\
            + self.get_value(activity, "prov:id") + ", "\
            + self.get_value(activity, "prov:startTime") + ", "\
            + self.get_value(activity, "prov:endTime")

        # all other optional attributes need to be enclosed with []
        attributes = ""
        for key, val in activity.iteritems():
            attributes += '%s="%s", ' % (key, val)

        if attributes:
            string += ", [" + attributes.rstrip(', ') + "]"

        string += ")"

        return string


class EntityPROVNRenderer(PROVNBaseRenderer):

    def render(self, entity):
        string = "entity(" + self.get_value(entity, "prov:id")

        # all other optional attributes need to be enclosed with []
        attributes = ""
        for key, val in entity.iteritems():
            attributes += '%s="%s", ' % (key, val)

        if attributes:
            string += ", [" + attributes.rstrip(', ') + "]"

        string += ")"

        return string


class AgentPROVNRenderer(PROVNBaseRenderer):

    def render(self, agent):
        string = "agent(" + self.get_value(agent, "prov:id")

        # all other optional attributes need to be enclosed with []
        attributes = ""
        for key, val in agent.iteritems():
            attributes += '%s="%s", ' % (key, val)

        if attributes:
            string += ", [" + attributes.rstrip(', ') + "]"

        string += ")"

        return string


class UsedPROVNRenderer(PROVNBaseRenderer):

    def render(self, used):
        string = "used("

        # id is optional, but we have an id in the database, thus include it
        string += self.get_value(used, "prov:id") + ";"

        # activity is mandatory:
        string += self.get_value(used, "prov:activity") + ","

        # entity is optional in W3C, but it's a positional argument
        string += self.get_value(used, "prov:entity") + ","

        # time is optional in W3C, but it's a positional argument
        string += self.get_value(used, "prov:time")

        # all other optional attributes need to be enclosed with []
        attributes = ""
        for key, val in used.iteritems():
            attributes += '%s="%s", ' % (key, val)

        if attributes:
            string += ", [" + attributes.rstrip(', ') + "]"

        string += ")"

        return string


class WasGeneratedByPROVNRenderer(PROVNBaseRenderer):

    def render(self, wasGeneratedBy):
        string = "wasGeneratedBy("

        # id is optional, but we have an id in the database, thus include it
        string += self.get_value(wasGeneratedBy, "prov:id") + ";"

        # entity is mandatory:
        string += self.get_value(wasGeneratedBy, "prov:entity") + ","

        # activity is optional in W3C, but it's a positional argument
        string += self.get_value(wasGeneratedBy, "prov:activity") + ","

        # time is optional in W3C, but it's a positional argument
        string += self.get_value(wasGeneratedBy, "prov:time")

        # all other optional attributes need to be enclosed with []
        attributes = ""
        for key, val in wasGeneratedBy.iteritems():
            attributes += '%s="%s", ' % (key, val)

        if attributes:
            string += ", [" + attributes.rstrip(', ') + "]"

        string += ")"

        return string


class WasAssociatedWithPROVNRenderer(PROVNBaseRenderer):

    def render(self, wasAssociatedWith):
        string = "wasAssociatedWith("

        # id is optional, but I have an id in the database, thus include it
        string += self.get_value(wasAssociatedWith, "prov:id") + ";"
        string += self.get_value(wasAssociatedWith, "prov:activity") + ","
        string += self.get_value(wasAssociatedWith, "prov:agent") + ","
        string += self.get_value(wasAssociatedWith, "prov:plan")

        # all other optional attributes need to be enclosed with []
        attributes = ""
        for key, val in wasAssociatedWith.iteritems():
            attributes += '%s="%s", ' % (key, val)

        if attributes:
            string += ", [" + attributes.rstrip(', ') + "]"

        string += ")"

        return string


class WasAttributedToPROVNRenderer(PROVNBaseRenderer):

    def render(self, wasAttributedTo):
        string = "wasAttributedTo("

        # id is optional, but I have an id in the database, thus include it
        string += self.get_value(wasAttributedTo, "prov:id") + ";"
        string += self.get_value(wasAttributedTo, "prov:entity") + ","
        string += self.get_value(wasAttributedTo, "prov:agent")

        # all other optional attributes need to be enclosed with []
        attributes = ""
        for key, val in wasAttributedTo.iteritems():
            attributes += '%s="%s", ' % (key, val)

        if attributes:
            string += ", [" + attributes.rstrip(', ') + "]"

        string += ")"

        return string


class HadMemberPROVNRenderer(PROVNBaseRenderer):

    def render(self, hadMember):
        string = "hadMember("

        # does not have an id nor optional attributes in W3C
        string += self.get_value(hadMember, "prov:collection") + ","
        string += self.get_value(hadMember, "prov:entity")

        string += ")"

        return string


class WasDerivedFromPROVNRenderer(PROVNBaseRenderer):

    def render(self, wasDerivedFrom):
        string = "wasDerivedFrom("

        # does not have an id nor optional attributes in W3C
        string += self.get_value(wasDerivedFrom, "prov:id") + ";"
        string += self.get_value(wasDerivedFrom, "prov:generatedEntity") + ","
        string += self.get_value(wasDerivedFrom, "prov:usedEntity") + ","
        string += self.get_value(wasDerivedFrom, "prov:activity") + ","
        string += self.get_value(wasDerivedFrom, "prov:generation") + ","
        string += self.get_value(wasDerivedFrom, "prov:usage")

        # all other optional attributes need to be enclosed with []
        attributes = ""
        for key, val in wasDerivedFrom.iteritems():
            attributes += '%s="%s", ' % (key, val)

        if attributes:
            string += ", [" + attributes.rstrip(', ') + "]"

        string += ")"

        return string


class PROVNRenderer(PROVNBaseRenderer):
    """
    Takes a list of ordered Python dictionaries (serialized data)
    and returns a PROV-N string
    """

    def render(self, data):

        string = "document\n"
        for p_id, p in data['prefix'].iteritems():
            string += "prefix %s <%s>,\n" % (p_id, p)

        for a_id, a in data['activity'].iteritems():
            string += ActivityPROVNRenderer().render(a) + ",\n"

        for e_id, e in data['entity'].iteritems():
            string += EntityPROVNRenderer().render(e) + ",\n"

        for a_id, a in data['agent'].iteritems():
            string += AgentPROVNRenderer().render(a) + ",\n"
        #     provstr = provstr + "entity(" + e.id + ", [voprov:type = '" + e.type + "', voprov:name = '" + e.name + "', voprov:annotation = '" + e.annotation + "']),\n"

        for u_id, u in data['used'].iteritems():
            string += UsedPROVNRenderer().render(u) + ",\n"

        for w_id, w in data['wasGeneratedBy'].iteritems():
            string += WasGeneratedByPROVNRenderer().render(w) + ",\n"

        for w_id, w in data['wasAssociatedWith'].iteritems():
            string += WasAssociatedWithPROVNRenderer().render(w) + ",\n"

        for w_id, w in data['wasAttributedTo'].iteritems():
            string += WasAttributedToPROVNRenderer().render(w) + ",\n"

        for h_id, h in data['hadMember'].iteritems():
            string += HadMemberPROVNRenderer().render(h) + ",\n"

        for w_id, w in data['wasDerivedFrom'].iteritems():
            string += WasDerivedFromPROVNRenderer().render(w) + ",\n"

        # remove final comma:
        string.rstrip(",\n") + "--\n"

        string += "endDocument"


        return string
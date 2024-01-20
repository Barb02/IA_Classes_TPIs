#encoding: utf8

# YOUR NAME: Bárbara Nóbrega Galiza
# YOUR NUMBER: 105937

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT (names, numbers):
# - João Miguel Andrade - 107969
# - Tomás Vitcal - 109018
# - Pedro Pinho - 109986

from semantic_network import *
from constraintsearch import *

class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        self.assoc_stats = {}
        pass

    def query_local(self,user=None,e1=None,rel=None,e2=None,assocOnly=None):
        self.query_result = []
        for u, d in self.declarations.items():
            for (en1, relation), en2 in d.items():
                if ((user == None or u == user) and (e1 == None or e1 == en1) and 
                    (rel == None or rel == relation) and (e2 == None or e2 == en2)):
                    if assocOnly==True and (relation == "subtype" or relation == "member"):
                        continue
                    if isinstance(en2,set):
                        for entity in en2:
                            self.query_result.append(Declaration(u,Relation(en1,relation,entity)))
                    else:
                        self.query_result.append(Declaration(u,Relation(en1,relation,en2)))

        return self.query_result # Your code must leave the output in
                          # self.query_result, which is returned here

    def query(self,entity,assoc=None):
        local = self.query_local(e1=entity, rel=assoc, assocOnly=True) + self.query_local(e2=entity, rel=assoc, assocOnly=True)
        pred_direct = self.query_local(e1=entity, rel="member") + self.query_local(e1=entity, rel="subtype")
        self.query_result = local
        for pd in pred_direct:
            self.query_result += self.query(pd.relation.entity2, assoc)
        return self.query_result # Your code must leave the output in
                          # self.query_result, which is returned here

    def predecessors(self, sub, user):
        decl = self.query_local(e1=sub, rel="subtype", user=user)
        if len(decl) == 0:
            return [sub]
        
        for obj in decl:
            if obj.relation.entity2 == None:
                return [obj.relation.entity2, sub]
            else:
                res = self.predecessors(obj.relation.entity2, user)
                return res + [sub]       

    def update_assoc_stats(self,assoc,user=None):
        self.assoc_stats[(assoc,user)] = ()
        local_assocs = self.query_local(rel=assoc, user=user)
        types_count_left = {}
        types_count_right = {}
        en_left = []
        en_right = []

        for la in local_assocs:
            if isObjectName(la.relation.entity1):
                en_left.append(la.relation.entity1)
            if isObjectName(la.relation.entity2):
                en_right.append(la.relation.entity2)

        for e in en_left:
            members_decl = self.query_local(e1=e, rel="member", user=user)
            if len(members_decl) > 0:
                direct_type = members_decl[0].relation.entity2
                super_list = self.predecessors(direct_type, user)

                for type in super_list:
                    if type in types_count_left.keys():
                        types_count_left[type] += 1
                    else:
                        types_count_left[type] = 1
            else:
                if "unknown" in types_count_left.keys():
                    types_count_left["unknown"] += 1
                else:
                    types_count_left["unknown"] = 1

        for e in en_right:
            members_decl = self.query_local(e1=e, rel="member", user=user)
            if len(members_decl) > 0:
                direct_type = members_decl[0].relation.entity2
                super_list = self.predecessors(direct_type, user)

                for type in super_list:
                    if type in types_count_right.keys():
                        types_count_right[type] += 1
                    else:
                        types_count_right[type] = 1
            else:
                if "unknown" in types_count_right.keys():
                    types_count_right["unknown"] += 1
                else:
                    types_count_right["unknown"] = 1

        type_stats_left = {}
        type_stats_right = {}
        
        if "unknown" not in types_count_left.keys():
            types_count_left["unknown"] = 0
        if "unknown" not in types_count_right.keys():
            types_count_right["unknown"] = 0

        total = len(en_left)
        for type in types_count_left:
            if type != "unknown":
                type_stats_left[type] = types_count_left[type]/(total - types_count_left["unknown"] + (types_count_left["unknown"])**0.5)
        for type in types_count_right:
            if type != "unknown":
                type_stats_right[type] = types_count_right[type]/(total - types_count_right["unknown"] + (types_count_right["unknown"])**0.5)

        self.assoc_stats[(assoc,user)] = (type_stats_left, type_stats_right)

        return self.assoc_stats



class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        pass

    def search_all(self,domains=None,xpto=None):
        self.calls += 1 
        saved_sol = []

        if domains==None:
            domains = self.domains
        if any([lv==[] for lv in domains.values()]):
            return None
        if all([len(lv)==1 for lv in list(domains.values())]):
            for (var1,var2) in self.constraints:
                constraint = self.constraints[var1,var2]
                if not constraint(var1,domains[var1][0],var2,domains[var2][0]):
                    return None 
            return { v:lv[0] for (v,lv) in domains.items() }
       
        for var in domains.keys():
            if len(domains[var])>1:
                for val in domains[var]:
                    newdomains = dict(domains)
                    newdomains[var] = [val]

                    newdomains = self.propagate_constraints(newdomains, var, val)
                    if newdomains == None:
                        continue

                    solution = self.search_all(newdomains)
                    if solution != None and solution not in saved_sol:
                        if isinstance(solution, dict):
                            saved_sol.append(solution)
                        else:
                            for s in solution:
                                saved_sol.append(s)
                        
                return saved_sol
        
    def propagate_constraints(self, domains, var, val):
        for variable, domain in domains.items():
            if variable == var:
                continue
            if (variable, var) in self.constraints.keys():
                constraint = self.constraints[(variable, var)]
                domains[variable] = [v for v in domain if constraint(variable, v, var, val)]
                if len(domains[variable]) == 0:
                    return None
        return domains


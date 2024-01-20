

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

from collections import Counter
from functools import reduce
from statistics import mean


class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

# Subclasse AssocOne
class AssocOne(Association):
    def __init__(self, e1, assoc, e2):
        Association.__init__(self, e1, assoc, e2)

# Subclasse AssocNum
class AssocNum(Association):
    def __init__(self, e1, assoc, e2):
        Association.__init__(self, e1, assoc, e2)

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:

    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl

    def __str__(self):
        return str(self.declarations)
    
    def insert(self,decl):
        self.declarations.append(decl)

    def query_local(self,user=None,e1=None,rel=None,rel_type=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (rel_type == None or isinstance(d.relation, rel_type))
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))
    
    def list_associations(self):
        decl = self.query_local(rel_type=Association)
        assocs = [d.relation.name for d in decl]
        return set(assocs)

    def list_objects(self):
        decl = self.query_local(rel_type=Member)
        objs = [d.relation.entity1 for d in decl]
        return set(objs)
    
    def list_users(self):
        decl = self.query_local(rel_type=Association)
        users = [d.user for d in decl]
        return set(users)
    
    def list_types(self):
        decl = self.query_local(rel_type=(Member, Subtype))
        types = [d.relation.entity2 for d in decl] + [d.relation.entity1 for d in decl if isinstance(d.relation, Subtype)]
        return set(types)

    # local = só corresponde ao nó (entidade) atual (a que é enviada)
    def list_local_associations(self, entity):
        decl1 = self.query_local(e1=entity ,rel_type=Association)
        decl2 = self.query_local(e2=entity, rel_type=Association)
        local_assocs = [d.relation.name for d in decl1] + [d.relation.name for d in decl2]
        return set(local_assocs)

    def list_relations_by_user(self, user):
        decl = self.query_local(user=user)
        rels = [d.relation.name for d in decl]
        return set(rels)
    
    # Associações diferentes == associações com nomes diferentes
    def associations_by_user(self, user):
        decl = self.query_local(user=user, rel_type=Association)
        assocs = [d.relation.name for d in decl]
        return len(set(assocs))
    
    def list_local_associations_by_entity(self, e1):
        assocs = set()

        for decl in self.declarations:
            if isinstance(decl.relation, Association) and decl.relation.entity1 == e1:
                assocs.add((decl.relation.name, decl.user))

        return list(assocs)
    
    def predecessor(self, super, sub):
        decl = self.query_local(e1=sub, rel_type=(Member, Subtype))
        if len(decl) == 0:
            return False
        
        for obj in decl:
            if obj.relation.entity2 == super:
                return True
            else:
                if self.predecessor(super, obj.relation.entity2):
                    return True       
        return False
    
    def predecessor_path(self, super, sub):
        decl = self.query_local(e1=sub, rel_type=(Member, Subtype))
        if len(decl) == 0:
            return None
        
        for obj in decl:
            if obj.relation.entity2 == super:
                return [super, sub]
            else:
                res = self.predecessor_path(super, obj.relation.entity2)
                if res:
                    return res + [sub]       
        return None
    
    def query(self, entity, rel=None):
        decl = self.query_local(e1=entity, rel=rel, rel_type=Association) + self.query_local(
                                e2=entity, rel=rel, rel_type=Association)

        pred_direct = self.query_local(e1=entity, rel_type=(Member, Subtype))

        for pd in pred_direct:
            decl += self.query(pd.relation.entity2, rel)
        return decl

    def query2(self, entity, rel=None):
        decl_local = self.query_local(e1=entity, rel=rel, rel_type=(Member, Subtype)) + self.query_local(
                                e2=entity, rel=rel, rel_type=(Member, Subtype))
        return decl_local + self.query(entity, rel)

    def query_cancel(self, entity, rel=None):
        decl = self.query_local(e1=entity, rel=rel, rel_type=Association) + self.query_local(
                                e2=entity, rel=rel, rel_type=Association)
        pred_direct = self.query_local(e1=entity, rel_type=(Member, Subtype))

        decl_name = [d.relation.name for d in decl]
        for pd in pred_direct:
            decl += [p for p in self.query_cancel(pd.relation.entity2, rel) if p.relation.name not in decl_name]
        return decl
    
    def query_down(self, tipo, assoc, first=True):
        if not first:
            decl = self.query_local(e1=tipo, rel=assoc) + self.query_local(e2=tipo, rel=assoc)
        else:
            decl = []
        desc_direct = self.query_local(e2=tipo, rel_type=(Member, Subtype))

        for dd in desc_direct:
            decl += [p for p in self.query_down(dd.relation.entity1, assoc, False)]
        return decl
    
    def query_induce(self, tipo, assoc, first=True):
        freq = {}
        for decl in self.query_down(tipo, assoc, first):
            if decl.relation.entity2 in freq:
                freq[decl.relation.entity2] += 1
            else:
                freq[decl.relation.entity2] = 1
        return max(freq, key=freq.get)
    
    def query_local_assoc(self, entidade, assoc):
        local = self.query_local(e1=entidade, rel=assoc)
        
        for d in local:
            if isinstance(d.relation, AssocOne):
                valor, count = Counter([d.relation.entity2 for d in local]).most_common(1)[0]
                return valor, count/len(local)
            
            elif isinstance(d.relation, AssocNum):
                return mean([d.relation.entity2 for d in local])
            
            elif isinstance(d.relation, Association):
                all_assoc = [(val, c/len(local)) for (val, c) in Counter([d.relation.entity2 for d in local]).most_common()]
                lim = 0
                l = []
                for(val, freq) in all_assoc:
                    lim += freq
                    l.append((val, freq))
                    if lim > 0.75:
                        return l

    def query_assoc_value(self, E, A):
        local = self.query_local(e1=E, rel=A)

        local_count = Counter([d.relation.entity2 for d in local]).most_common()

        if len(local_count) == 1:
            return local_count[0][0] # list of (val, count)

        herdadas = self.query(entity=E, rel=A)
        herdadas_count = Counter([d.relation.entity2 for d in herdadas]).most_common()

        F = {}
        for v, c in local_count:
            F[v] = c
        for v,c in herdadas_count:
            if v in F:
                F[v] += c
            else:
                F[v] = c

        return sorted(F.items(), key=lambda e: e[1], reverse=True)[0][0]    
import Orange
data = Orange.data.Table("./assoc.basket")

rules = Orange.associate.AssociationRulesSparseInducer(data, support = 0.01)
print "%5s   %5s   %5s" % ("supp", "conf", "lift")
for r in rules:
    print "%5.3f   %5.3f   %5.3f   %s" % (r.support, r.confidence, r.lift ,r)

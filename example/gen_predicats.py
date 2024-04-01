import sys
sys.path.append('../obfuscator/')

from transform import RuleApplier,SimpleParse

# Example Usage
expr = "x%2==1"
rules = [
        ("a==b", "a==2*a-b"),
        ("a%b","((a*2)%(b*2))/2"),
        ("a=b","(c=b+a=c)/2")
        ]
rule_applier = RuleApplier()
result = rule_applier.apply_rule(rules[0], expr)
result = rule_applier.apply_rule(rules[1], result)
result = rule_applier.apply_rule(rules[2], result)
print(result)
#print(SimpleParse.parse_expr(result))

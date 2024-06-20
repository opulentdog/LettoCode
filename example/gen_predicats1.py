import sys
sys.path.append('../obfuscator/')

from transform import RuleApplier,SimpleParse

# Example Usage
expr = "x%2==1"
rules = [
        ("a==b", "a==2*a-b"),
        ]
rule_applier = RuleApplier()
result = rule_applier.apply_rule(rules[0], expr)
print(SimpleParse.parse_expr(result))




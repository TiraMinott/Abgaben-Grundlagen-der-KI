
from collections import Counter
import math
import pandas as pd

def is_empty(df):
    return df.shape[0] == 0

def all_same_class(df, target):
    return len(set(df[target])) == 1

def majority_value(df, target):
    counts = Counter(df[target])
    maxc = max(counts.values())
    winners = sorted([c for c, n in counts.items() if n == maxc])
    return winners[0]

def entropy(labels):
    total = len(labels)
    counts = Counter(labels)
    return -sum((c/total) * math.log2(c/total) for c in counts.values())

def information_gain(examples, attribute, target):
    base = entropy(list(examples[target]))
    total = len(examples)
    cond = 0.0
    for _, sub in examples.groupby(attribute):
        p = len(sub) / total
        cond += p * entropy(list(sub[target]))
    return base - cond

def MaxInformationGain(examples, attrs, target):
    gains = {a: information_gain(examples, a, target) for a in attrs}
    return max(gains, key=gains.get)

class DecisionTree(dict):
    def __init__(self, test_attr):
        super().__init__()
        self["test"] = test_attr
        self["branches"] = {}
    def addBranch(self, label, subtree):
        self["branches"][label] = subtree

def is_leaf(t):
    return isinstance(t, str)

def pretty(tree, indent=""):
    if is_leaf(tree):
        return indent + f"→ {tree}\n"
    s = indent + f"[{tree['test']}]\n"
    for val, sub in tree["branches"].items():
        s += indent + f" ├─ {val}:\n"
        s += pretty(sub, indent + " │   ")
    return s

def ID3(examples, attr, default, target="Kandidat"):
    if is_empty(examples):
        return default
    if all_same_class(examples, target):
        return examples[target].iloc[0]
    if len(attr) == 0:
        return majority_value(examples, target)

    test = MaxInformationGain(examples, attr, target)
    tree = DecisionTree(test)
    m = majority_value(examples, target)
    for v_i, ex_i in examples.groupby(test):
        remaining = [a for a in attr if a != test]
        st = ID3(ex_i.drop(columns=[test]), remaining, m, target)
        tree.addBranch(label=v_i, subtree=st)
    return tree

def predict_one(tree, x):
    if is_leaf(tree):
        return tree
    test = tree["test"]
    v = x.get(test)
    if v not in tree["branches"]:
        # fallback: majority over leaves
        def leaves(t):
            if is_leaf(t): return [t]
            out = []
            for sub in t["branches"].values():
                out.extend(leaves(sub))
            return out
        from collections import Counter
        return Counter(leaves(tree)).most_common(1)[0][0]
    return predict_one(tree["branches"][v], x)

def predict(tree, X):
    return [predict_one(tree, row) for row in X.to_dict(orient="records")]

if __name__ == "__main__":
    data = [
        (1, "≥35", "hoch",    "Abitur",   "O"),
        (2, "<35", "niedrig", "Master",   "O"),
        (3, "≥35", "hoch",    "Bachelor", "M"),
        (4, "≥35", "niedrig", "Abitur",   "M"),
        (5, "≥35", "hoch",    "Master",   "O"),
        (6, "<35", "hoch",    "Bachelor", "O"),
        (7, "<35", "niedrig", "Abitur",   "M"),
    ]
    df = pd.DataFrame(data, columns=["Nr","Alter","Einkommen","Bildung","Kandidat"])
    features = ["Alter","Einkommen","Bildung"]
    tree = ID3(df[features+["Kandidat"]].copy(), features.copy(), default=majority_value(df, "Kandidat"), target="Kandidat")
    print(pretty(tree))
    preds = predict(tree, df[features])
    acc = sum(p==y for p,y in zip(preds, df["Kandidat"])) / len(df)
    print("Pred:", preds)
    print("Acc:", acc)

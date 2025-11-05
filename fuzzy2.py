def mu_moderate_rainfall(x):
    if x <= 50:
        return 0
    elif 50 < x < 100:
        return (x - 50) / 50
    elif 100 <= x <= 150:
        return 1
    elif 150 < x < 200:
        return (200 - x) / 50
    else:
        return 0

universe = list(range(0, 301))

fuzzy_set = {x: mu_moderate_rainfall(x) for x in universe}

def is_normal(fuzzy_set):
    return any(m == 1 for m in fuzzy_set.values())

def support(fuzzy_set):
    return [x for x, m in fuzzy_set.items() if m > 0]

def core(fuzzy_set):
    return [x for x, m in fuzzy_set.items() if m == 1]

def height(fuzzy_set):
    return max(fuzzy_set.values())

def cardinality(fuzzy_set):
    return sum(fuzzy_set.values())

def is_convex(fuzzy_set):
    sorted_x = sorted(fuzzy_set.keys())
    for i in range(len(sorted_x) - 2):
        x1 = sorted_x[i]
        x2 = sorted_x[i+1]
        x3 = sorted_x[i+2]
        mu1 = fuzzy_set[x1]
        mu2 = fuzzy_set[x2]
        mu3 = fuzzy_set[x3]
        if mu2 < min(mu1, mu3):
            return False
    return True

print("Fuzzy set 'Moderate Rainfall' properties:")
print(f"Normality: {is_normal(fuzzy_set)}")
print(f"Support: {support(fuzzy_set)}")
print(f"Core: {core(fuzzy_set)}")
print(f"Height: {height(fuzzy_set)}")
print(f"Cardinality: {cardinality(fuzzy_set):.2f}")
print(f"Convexity: {is_convex(fuzzy_set)}")

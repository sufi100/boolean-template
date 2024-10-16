import re
from collections import defaultdict

# Function to check if the given 2-CNF formula is satisfiable
def is_satisfiable(formula_str):
    clauses = parse_formula(formula_str)
    graph, reverse_graph = build_implication_graph(clauses)
    return not has_contradiction(graph, reverse_graph)

# Function to return a satisfying assignment for the given 2-CNF formula
def sat_assignment(formula_str):
    clauses = parse_formula(formula_str)
    graph, reverse_graph = build_implication_graph(clauses)
    if has_contradiction(graph, reverse_graph):
        return None
    return find_assignment(graph, reverse_graph)

# Parse the 2-CNF formula into clauses
def parse_formula(formula_str):
    tokens = re.findall(r'\(.*?\)|\S+', formula_str)
    clauses = []
    for token in tokens:
        if '->' in token:
            left, right = token.split('->')
            left = left.strip()
            right = right.strip()
            clauses.append((negate_literal(left), right))
        elif '\/' in token:
            left, right = token.split('\/')
            left = left.strip()
            right = right.strip()
            clauses.append((left, right))
        else:
            clauses.append((token.strip(),))
    return clauses

# Build implication graph from the parsed clauses
def build_implication_graph(clauses):
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)
    for clause in clauses:
        if len(clause) == 1:
            literal = clause[0]
            graph[negate_literal(literal)].append(literal)
            reverse_graph[literal].append(negate_literal(literal))
        elif len(clause) == 2:
            u, v = clause
            graph[negate_literal(u)].append(v)
            graph[negate_literal(v)].append(u)
            reverse_graph[v].append(negate_literal(u))
            reverse_graph[u].append(negate_literal(v))
    return graph, reverse_graph

# Check if there's a contradiction in the implication graph
def has_contradiction(graph, reverse_graph):
    visited = {}
    stack = []

    def dfs(node, component):
        stack.append(node)
        visited[node] = component
        for neighbor in graph[node]:
            if neighbor not in visited:
                if not dfs(neighbor, component):
                    return False
            elif visited[neighbor] == component:
                return False
        return True

    component = 0
    for node in graph:
        if node not in visited:
            if not dfs(node, component):
                return True
            component += 1
    return False

# Find a satisfying assignment using the implication graph
def find_assignment(graph, reverse_graph):
    assignment = {}
    visited = set()
    stack = []

    def assign_value(node, value):
        stack.append(node)
        assignment[node] = value
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                assign_value(neighbor, value)

    for node in graph:
        if node not in visited:
            assign_value(node, True)
    return assignment

# Helper function to negate a literal
def negate_literal(literal):
    return literal[1:] if literal.startswith('~') else f'~{literal}'

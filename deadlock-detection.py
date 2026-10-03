# Deadlock Detection using Wait-For Graph (WFG)

# Resource allocation:
# resource -> process currently holding it
allocation = {
    "R1": "P1",
    "R2": "P2",
    "R3": "P3",
    "R4": "P4"
}

# Pending requests:
# process -> resource it is waiting for
requests = {
    "P1": "R2",
    "P2": "R3",
    "P3": "R1",
    "P4": "R1"
}


# -----------------------------------------
# Build Wait-For Graph
# -----------------------------------------
def build_wait_for_graph():

    graph = {
        "P1": [],
        "P2": [],
        "P3": [],
        "P4": []
    }

    for process, resource in requests.items():

        holder = allocation.get(resource)

        if holder and holder != process:

            graph[process].append(holder)

    return graph


# -----------------------------------------
# Display Wait-For Graph
# -----------------------------------------
def print_graph(graph):

    for process, waits in graph.items():

        target = ", ".join(waits) if waits else "-"

        print(
            f"  {process} waits for -> {target}"
        )


# -----------------------------------------
# Detect Cycle using DFS
# -----------------------------------------
def detect_cycle(graph):

    visited = set()
    stack = []

    def dfs(node):

        visited.add(node)
        stack.append(node)

        for nxt in graph[node]:

            # Cycle found
            if nxt in stack:

                return (
                    stack[stack.index(nxt):]
                    + [nxt]
                )

            # Visit unvisited node
            if nxt not in visited:

                cycle = dfs(nxt)

                if cycle:
                    return cycle

        stack.pop()

        return None

    # Start DFS from every unvisited node
    for node in graph:

        if node not in visited:

            cycle = dfs(node)

            if cycle:
                return cycle

    return None


# -----------------------------------------
# Resolve Deadlock
# -----------------------------------------
def resolve_deadlock(cycle):

    # Remove the repeated last node
    # from the cycle
    members = cycle[:-1]

    # Count resources held by
    # each process in the cycle
    held = {
        p: sum(
            1
            for r in allocation.values()
            if r == p
        )
        for p in members
    }

    # Select process holding the
    # fewest resources.
    # If tied, choose lower process number.
    victim = min(
        members,
        key=lambda p: (held[p], p)
    )

    print(
        f"  Victim selected -> {victim} "
        f"(lowest cost)"
    )

    # Release all resources
    # held by the victim
    for res in [
        r for r, p in allocation.items()
        if p == victim
    ]:

        del allocation[res]

        print(
            f"  {victim} releases {res}"
        )

    # Remove victim's request
    requests.pop(victim, None)

    return victim


# -----------------------------------------
# Display Initial State
# -----------------------------------------
print(
    "\n===== DEADLOCK DETECTION SIMULATION =====\n"
)

print("Resource Allocation:")

for res, proc in allocation.items():

    print(
        f"  {res} is held by {proc}"
    )


print("\nResource Requests:")

for proc, res in requests.items():

    print(
        f"  {proc} is requesting {res}"
    )


# -----------------------------------------
# Deadlock Detection and Recovery
# -----------------------------------------
round_no = 1

while True:

    print(
        f"\n----- Detection Round {round_no} -----"
    )

    print("Wait-For Graph:")

    graph = build_wait_for_graph()

    print_graph(graph)

    cycle = detect_cycle(graph)

    if not cycle:

        print(
            "Result: No deadlock detected. "
            "System is safe."
        )

        break

    print(
        "Result: DEADLOCK DETECTED!"
    )

    print(
        "  Cycle: "
        + " -> ".join(cycle)
    )

    resolve_deadlock(cycle)

    round_no += 1


# -----------------------------------------
# Display Final System State
# -----------------------------------------
print(
    "\n===== FINAL SYSTEM STATE ====="
)

for res, proc in allocation.items():

    print(
        f"  {res} is held by {proc}"
    )

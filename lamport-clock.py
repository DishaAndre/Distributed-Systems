# Initial clock value for each process
clock = {
    "P1": 0,
    "P2": 0,
    "P3": 0
}
# Store all events
events = []

# Function: Internal Event
def internal_event(process):
    clock[process] += 1
    events.append(
        (process, "Internal", "-", "-", clock[process])
    )
    print(
        f"{process}: Internal Event -> Clock = {clock[process]}"
    )

# Function: Send Message
def send_message(sender, receiver, message):
    clock[sender] += 1
    timestamp = clock[sender]
    events.append(
        (sender, "Send", message, receiver, timestamp)
    )
    print(
        f"{sender}: Send {message} -> {receiver} "
        f"-> Clock = {timestamp}"
    )
    return timestamp

# Function: Receive Message
def receive_message(receiver, sender, message, timestamp):
    clock[receiver] = max(
        clock[receiver],
        timestamp
    ) + 1
    events.append(
        (receiver, "Receive", message, sender,
         clock[receiver])
    )
    print(
        f"{receiver}: Receive {message} from {sender} "
        f"-> Clock = {clock[receiver]}"
    )

# SIMULATION
print("\n===== LAMPORT CLOCK SIMULATION =====\n")
# 1. P1 performs an internal event
internal_event("P1")

# 2. P1 sends M1 to P2
m1_timestamp = send_message("P1", "P2", "M1")
# 3. P2 performs an internal event
internal_event("P2")
# 4. P2 receives M1
receive_message(
    "P2",
    "P1",
    "M1",
    m1_timestamp
)
# 5. P2 sends M2 to P3
m2_timestamp = send_message("P2", "P3", "M2")
# 6. P3 performs an internal event
internal_event("P3")
# 7. P3 receives M2
receive_message(
    "P3",
    "P2",
    "M2",
    m2_timestamp
)
# 8. P3 sends M3 to P1
m3_timestamp = send_message("P3", "P1", "M3")
# 9. P1 receives M3
receive_message(
    "P1",
    "P3",
    "M3",
    m3_timestamp
)

# FINAL CLOCK VALUES
print("\n===== FINAL CLOCK VALUES =====")
for process in clock:
    print(f"{process} = {clock[process]}")

# EVENT TABLE
print("\n===== EVENT TABLE =====")
print(
    f"{'Process':<10}"
    f"{'Event':<12}"
    f"{'Message':<10}"
    f"{'Other':<10}"
    f"{'Timestamp':<10}"
)
print("-" * 52)
for event in events:
    process, event_type, message, other, timestamp = event
    print(
        f"{process:<10}"
        f"{event_type:<12}"
        f"{message:<10}"
        f"{other:<10}"
        f"{timestamp:<10}"
    ) 

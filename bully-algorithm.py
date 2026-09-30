import threading
import time
import queue


class Process(threading.Thread):

    def __init__(self, pid, all_pids, message_queues):
        super().__init__()

        self.pid = pid
        self.all_pids = sorted(all_pids)
        self.queues = message_queues

        self.is_alive = True
        self.is_coordinator = False
        self.running = True
        self.in_election = False

    def log(self, text):
        print(f"[Process P{self.pid}] {text}")

    def send_message(self, target_pid, msg_type, sender_pid):

        if target_pid in self.queues:
            self.queues[target_pid].put(
                (msg_type, sender_pid)
            )

    def start_election(self):

        if not self.is_alive or self.in_election:
            return

        self.in_election = True

        self.log(
            "Initiating Election! "
            "Broadcasting ELECTION message to higher IDs..."
        )

        higher_pids = [
            p for p in self.all_pids
            if p > self.pid
        ]

        for higher_pid in higher_pids:
            self.send_message(
                higher_pid,
                "ELECTION",
                self.pid
            )

        # Wait for responses
        time.sleep(1.0)

        if not getattr(self, "_received_ok", False):
            self.declare_victory()
        else:
            self.log(
                "Received OK from higher process. "
                "Stepping back."
            )

            self._received_ok = False
            self.in_election = False

    def declare_victory(self):

        self.is_coordinator = True

        self.log(
            "★★★ I AM THE NEW COORDINATOR ★★★"
        )

        lower_pids = [
            p for p in self.all_pids
            if p < self.pid
        ]

        for p in lower_pids:
            self.send_message(
                p,
                "COORDINATOR",
                self.pid
            )

    def run(self):

        self._received_ok = False

        while self.running:

            if not self.is_alive:
                time.sleep(0.5)
                continue

            try:

                # Get message from queue
                msg_type, sender_pid = (
                    self.queues[self.pid].get(
                        timeout=0.5
                    )
                )

                if msg_type == "ELECTION":

                    self.log(
                        f"Received ELECTION message "
                        f"from P{sender_pid}."
                    )

                    self.send_message(
                        sender_pid,
                        "OK",
                        self.pid
                    )

                    threading.Thread(
                        target=self.start_election,
                        daemon=True
                    ).start()

                elif msg_type == "OK":

                    self.log(
                        f"Received OK response from "
                        f"higher process P{sender_pid}."
                    )

                    self._received_ok = True

                elif msg_type == "COORDINATOR":

                    self.is_coordinator = False

                    self.log(
                        f"Acknowledged Process "
                        f"P{sender_pid} as current COORDINATOR."
                    )

            except queue.Empty:
                pass


def main():

    # Process IDs
    pids = [1, 2, 3, 4, 5]

    # Create message queues
    queues = {
        pid: queue.Queue()
        for pid in pids
    }

    processes = {}

    print("==========================================================")
    print(" DISTRIBUTED SYSTEM BULLY ELECTION SIMULATION ")
    print("==========================================================")

    print(
        f"Initializing process cluster with IDs: {pids}\n"
    )

    # Create and start processes
    for pid in pids:

        p = Process(
            pid,
            pids,
            queues
        )

        processes[pid] = p
        p.start()

        time.sleep(1.0)

    # Initially, highest ID is coordinator
    print("--- Initializing Baseline Leader ---")

    processes[max(pids)].declare_victory()

    time.sleep(1.5)

    # Simulate coordinator failure
    leader_pid = max(pids)

    print(
        f"\n[EVENT] Crash simulated on active "
        f"Coordinator Process P{leader_pid}!"
    )

    processes[leader_pid].is_alive = False
    processes[leader_pid].is_coordinator = False

    time.sleep(1.0)

    # P2 detects coordinator failure
    detector_pid = 2

    print(
        f"\n[EVENT] Process P{detector_pid} "
        f"detects Coordinator unresponsiveness."
    )

    threading.Thread(
        target=processes[detector_pid].start_election,
        daemon=True
    ).start()

    # Wait for election to finish
    time.sleep(4.0)

    print(
        "\n--- Simulation Complete: Final Cluster State ---"
    )

    for pid in sorted(pids):

        if not processes[pid].is_alive:
            status = "CRASHED"

        elif processes[pid].is_coordinator:
            status = "COORDINATOR"

        else:
            status = "ACTIVE NODE"

        print(
            f"Process P{pid}: {status}"
        )

    # Stop all processes
    for p in processes.values():
        p.running = False


if __name__ == "__main__":
    main()

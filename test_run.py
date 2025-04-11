from orka.orchestrator import Orchestrator

if __name__ == "__main__":
    orchestrator = Orchestrator("./example.yml")
    test_input = "who is Marco Somma in software engineering?"
    results = orchestrator.run(test_input)
    print("\nFinal Results:")
    for agent_id, result in results.items():
        print(f"{agent_id}: {result}")

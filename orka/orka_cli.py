import argparse
from orka.orchestrator import Orchestrator
import os

def main():
    parser = argparse.ArgumentParser(description="Run OrKa with a YAML configuration.")
    parser.add_argument("config", help="Path to the YAML configuration file.")
    parser.add_argument("input", help="Input question or statement for the orchestrator.")
    parser.add_argument("--log-to-file", action="store_true", help="Save the orchestration trace to a JSON log file.")
    args = parser.parse_args()

    orchestrator = Orchestrator(config_path=args.config)
    orchestrator.run(args.input)

if __name__ == "__main__":
    main()

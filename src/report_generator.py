from datetime import datetime


def write_report(results, global_drift, health, action, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("DATA DRIFT MONITOR REPORT\n")
        f.write(f"Generated at : {datetime.now()}\n\n")

        for r in results:
            f.write(f"Feature: {r['feature']}\n")
            f.write(f"Method: {r['method']}\n")
            f.write(f"Severity: {r['severity']}\n")

            if r.get("explanation"):
                f.write("Reason:\n")
                for line in r["explanation"]:
                    f.write(f"- {line}\n")

            f.write("\n")

        f.write(f"GLOBAL DRIFT SCORE: {round(global_drift, 3)}\n")
        f.write(f"SYSTEM HEALTH: {health}\n")
        f.write(f"RECOMMENDED ACTION: {action}\n")

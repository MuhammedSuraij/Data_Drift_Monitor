from datetime import datetime

def write_report(result, global_score, health , action , path):
    with open(path, "w") as f:
        f.write("DATA DRIFT MONITOR REPORT\n")
        f.write(f"Generated at : {datetime.now()}\n\n")

        for r in result:
            f.write(f"Feature: {r['feature']}\n")
            f.write(f"Method: {r['method']}\n")
            f.write(f"Severity: {r['severity']}\n")

            if r.get("reason"):
                f.write(f"Reason : {r['reason']}\n")
            if r.get("new_categories"):
                f.write(f"New Categories : {r['new_categories']}\n")

            f.write("\n")
        
        f.write(f"GLOBAL DRIFT SCORE: {round(global_score,3)}\n")
        f.write(f"SYSTEM HEALTH: {health}\n")
        f.write(f"RECOMMENDED ACTION: {action}\n")
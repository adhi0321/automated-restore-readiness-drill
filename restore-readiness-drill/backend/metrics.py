def calculate_metrics(results):
    total = len(results)
    if total == 0:
        return {}
    
    passed = sum(1 for r in results if r['overall_result'] == 'PASS')
    failed = total - passed
    
    recovery_times = [r['recovery_time_seconds'] for r in results]
    avg_rto = sum(recovery_times) / total if total > 0 else 0
    min_rto = min(recovery_times) if total > 0 else 0
    max_rto = max(recovery_times) if total > 0 else 0
    
    return {
        "total_drills": total,
        "successful_drills": passed,
        "failed_drills": failed,
        "recovery_success_rate": round((passed / total) * 100, 2) if total > 0 else 0,
        "average_recovery_time": round(avg_rto, 4),
        "min_recovery_time": round(min_rto, 4),
        "max_recovery_time": round(max_rto, 4)
    }

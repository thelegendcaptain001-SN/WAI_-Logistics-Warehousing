from dataclasses import dataclass
from typing import List, Dict, Any
import numpy as np

@dataclass
class FallbackPlan:
    priority_orders: int
    utilization: float
    delay_hours: float
    throughput_improvement: float
    cost_savings: float
    cost_reduction: float
    staff_allocation: List[Dict]
    immediate_actions: List[str]
    warehouse_name: str

class AIHeuristicEngine:
    """AI-powered decision engine for cyber incident response."""
    
    @staticmethod
    def generate_fallback_plan(incident_type: str, staff_available: int, 
                             orders_waiting: int, vip_pct: int, sla_critical_pct: int,
                             duration_hours: int, warehouse_name: str) -> FallbackPlan:
        
        # Incident severity multipliers
        severity_multipliers = {
            "WMS Outage": 0.65,
            "Automation Down": 0.60,
            "IoT Offline": 0.75,
            "Extended Outage": 0.40,
            "Partial Degradation": 0.70
        }
        
        severity = severity_multipliers.get(incident_type, 0.65)
        
        # Priority order calculation
        vip_orders = int(orders_waiting * (vip_pct / 100))
        sla_orders = int(orders_waiting * (sla_critical_pct / 100))
        priority_orders = min(int(orders_waiting * 0.45), vip_orders + sla_orders)
        
        # Staff utilization (AI optimization)
        max_utilization = 0.92  # AI-guided max
        utilization = min(staff_available / 50 * severity * max_utilization, max_utilization)
        
        # Performance metrics
        baseline_throughput = 5.2  # Normal operations
        reactive_throughput = baseline_throughput * severity * 0.35
        ai_throughput = baseline_throughput * severity * 0.75
        throughput_improvement = ((ai_throughput / reactive_throughput) - 1) * 100
        
        delay_hours = duration_hours * (1 - utilization)
        cost_savings = orders_waiting * 50 * 0.51  # $50/order penalty * 51% reduction
        cost_reduction = 51
        
        # Staff allocation by zone
        zones = ['Zone A (Priority)', 'Zone B (Standard)', 'Zone C (Sort/Pack)', 'Zone D (Transport)']
        staff_per_zone = np.random.randint(8, 20, size=4)
        staff_per_zone = staff_per_zone * (staff_available / 50)  # Scale by staff count
        staff_per_zone = staff_per_zone.astype(int)
        staff_per_zone[-1] += staff_available - sum(staff_per_zone)  # Balance
        
        staff_allocation = [
            {'Zone': zones[i], 'Staff': staff_per_zone[i], 'Role': 'Pick/Pack/Sort'}
            for i in range(4)
        ]
        
        # Immediate actions
        actions = [
            f"Process {priority_orders} priority orders immediately",
            f"Assign {staff_per_zone[0]} staff to Zone A (VIP/SLA critical)",
            f"Implement buddy system for safety",
            f"Defer {orders_waiting-priority_orders} low-priority orders",
            f"Notify VIP customers of +{delay_hours:.1f}h delay"
        ]
        
        return FallbackPlan(
            priority_orders=priority_orders,
            utilization=utilization,
            delay_hours=delay_hours,
            throughput_improvement=throughput_improvement,
            cost_savings=cost_savings,
            cost_reduction=cost_reduction,
            staff_allocation=staff_allocation,
            immediate_actions=actions,
            warehouse_name=warehouse_name
        )

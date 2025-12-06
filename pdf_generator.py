from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from typing import Dict, Any

def generate_playbook_pdf(plan: Dict[str, Any]) -> BytesIO:
    """Generate PDF playbook from AI plan."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        spaceAfter=30,
        textColor=colors.red,
        alignment=1  # Center
    )
    
    story = []
    
    # Header
    story.append(Paragraph(f"<b>🚨 CYBER INCIDENT PLAYBOOK</b>", title_style))
    story.append(Paragraph(f"<i>{plan['warehouse_name']} | {datetime.now().strftime('%Y-%m-%d %H:%M')}</i>", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # KPIs Table
    kpis_data = [
        ['Metric', 'Value', 'vs Reactive'],
        ['Priority Orders', f"{plan['priority_orders']}/{plan['orders_waiting']}", f"+{plan['throughput_improvement']:.0f}%"],
        ['Staff Utilization', f"{plan['utilization']:.0%}", f"{plan['staff_available']} staff"],
        ['Estimated Delay', f"+{plan['delay_hours']:.1f}h", 'Optimized'],
        ['Cost Savings', f"${plan['cost_savings']:,.0f}", f"{plan['cost_reduction']}%"]
    ]
    
    kpis_table = Table(kpis_data)
    kpis_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(kpis_table)
    story.append(Spacer(1, 20))
    
    # Staff Allocation
    story.append(Paragraph("<b>👥 STAFF ALLOCATION</b>", styles['Heading2']))
    alloc_data = [['Zone', 'Staff Count', 'Primary Role']] + [
        [item['Zone'], str(item['Staff']), item['Role']] for item in plan['staff_allocation']
    ]
    alloc_table = Table(alloc_data)
    alloc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(alloc_table)
    story.append(Spacer(1, 20))
    
    # Immediate Actions
    story.append(Paragraph("<b>✅ IMMEDIATE ACTIONS (Next 2 Hours)</b>", styles['Heading2']))
    for i, action in enumerate(plan['immediate_actions'], 1):
        story.append(Paragraph(f"{i}. {action}", styles['Normal']))
        story.append(Spacer(1, 6))
    
    # Safety
    story.append(Paragraph("<b>⚠️ SAFETY PRIORITIES</b>", styles['Heading2']))
    safety = [
        "• Implement buddy system for heavy lifts",
        "• Reduce picking pace by 20% to minimize errors",
        "• Mandatory breaks every 4 hours",
        "• Watch for congestion in manual zones"
    ]
    for item in safety:
        story.append(Paragraph(item, styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

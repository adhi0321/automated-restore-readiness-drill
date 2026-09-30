# PLANNED STAKEHOLDER VALIDATION

> **Transparency Notice:** Actual external stakeholder interviews and formal user testing have not yet been conducted for this academic prototype. To preserve academic integrity, this document describes the **Planned Stakeholder Validation Framework**, including target stakeholder profiles, expected user comprehension milestones, an evaluation protocol, and a ready-to-use questionnaire with a quantitative scoring methodology.

---

## 1. Stakeholder Assumptions

We anticipate four key stakeholder groups interacting with this restore-readiness drill platform:

| Stakeholder Role | Primary Concern | Expected Technical Depth | Core Decision to Make |
|:---|:---|:---:|:---|
| **Executive / Studio Head** | Player churn, revenue loss during downtime, reputation risk | Non-specialist | Determine whether to approve disaster recovery infrastructure investment. |
| **Game Producer / Lead** | Match integrity, unfair rollback compensations, player complaints | Moderate | Decide whether an active game season or tournament is protected against server crashes. |
| **DevOps / SRE Engineer** | Recovery speed (RTO), data loss window (RPO), automated alerting | High | Implement restore drill daemon, tune backup frequency, and debug storage bottlenecks. |
| **QA / Compliance Auditor** | Audit proof, SOC 2 / ISO 27001 disaster recovery evidence | Moderate to High | Certify whether disaster recovery drills meet regulatory requirements. |

---

## 2. Expected User Understanding Milestones

Upon reviewing the system dashboard and executive summary, a reviewer should be able to:
1. Explain in simple words why a successful backup script does not guarantee a working restore.
2. Identify whether a drill resulted in **PASS** or **FAIL** within 5 seconds of looking at the dashboard.
3. Understand that **RTO (Recovery Time Objective)** means "how long it takes to come back online" and **RPO (Recovery Point Objective)** means "how much player progress was lost."
4. Read the non-specialist recommendations and understand the next operational action without needing a computer science degree.

---

## 3. Ready-to-Use Stakeholder Questionnaire

The following questionnaire is prepared for planned review sessions with game studio leads and DevOps specialists.

### Section A: Conceptual Clarity (1 = Strongly Disagree, 5 = Strongly Agree)

**Q1: Is the purpose of the restore-readiness drill system clear?**
- Score: `[ 1 ]  [ 2 ]  [ 3 ]  [ 4 ]  [ 5 ]`
- Notes: __________________________________________________________________

**Q2: Is the difference between "backup completed" and "restore-readiness" clear?**
- Score: `[ 1 ]  [ 2 ]  [ 3 ]  [ 4 ]  [ 5 ]`
- Notes: __________________________________________________________________

**Q3: Are the concepts of RTO (recovery speed) and RPO (data freshness) clearly explained and visualized?**
- Score: `[ 1 ]  [ 2 ]  [ 3 ]  [ 4 ]  [ 5 ]`
- Notes: __________________________________________________________________

**Q4: Is the overall drill result (PASS / FAIL) immediately understandable?**
- Score: `[ 1 ]  [ 2 ]  [ 3 ]  [ 4 ]  [ 5 ]`
- Notes: __________________________________________________________________

**Q5: Are the recommendations provided at the end of each drill practical and actionable?**
- Score: `[ 1 ]  [ 2 ]  [ 3 ]  [ 4 ]  [ 5 ]`
- Notes: __________________________________________________________________

### Section B: Open-Ended Qualitative Feedback

**Q6: What specific element or metric on the dashboard felt confusing or cluttered?**
- Response: __________________________________________________________________

**Q7: What additional information would an executive or studio head need before trusting this system in production?**
- Response: __________________________________________________________________

---

## 4. Quantitative Interpretation and Scoring Method

To evaluate planned stakeholder responses systematically:

1. **Calculate the Readiness Comprehension Index (RCI):**
   $$\text{RCI} = \frac{\sum_{i=1}^{5} Q_i}{25} \times 100\%$$

2. **Benchmark Thresholds:**
   - **$\ge 80\%$ (20–25 points): Strong Validation.** Stakeholders demonstrate clear comprehension of restore risks and agree that dashboard outputs are actionable.
   - **$65\% - 79\%$ (16–19 points): Marginal Validation.** Conceptual purpose is understood, but terminology (e.g., WAL replay, Lamport sequence) requires further simplification for non-specialists.
   - **$< 65\%$ (< 16 points): Revision Required.** Redesign dashboard layout and replace technical metrics with plain-language business impact indicators.

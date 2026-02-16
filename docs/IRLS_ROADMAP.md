\# IRLS DEVELOPMENT ROADMAP



---



\# PHASE 1 – Stability (NOW)



1\. Finalize WorkSession logic (no regressions)

2\. Add AttendanceSession model

3\. Add attendance start/stop endpoints

4\. Add basic attendance guard validation



---



\# PHASE 2 – Repair Control



5\. Add authorized\_hours to repair cycle

6\. Bind authorized hours to machine cycle

7\. Calculate worked\_hours automatically

8\. Detect extra\_hours

9\. Add manager approval for extra\_hours

10\. Add status flag: requires\_extra\_hours\_approval



---



\# PHASE 3 – Visual Control



11\. Add progress calculation engine

12\. Add 75% / 100% thresholds

13\. Add color flags in API response

14\. Add notification triggers



---



\# PHASE 4 – Model Intelligence



15\. Integrate machine\_catalog.xlsx

16\. Auto-detect type + size from model

17\. Allow manual override if not found



---



\# PHASE 5 – Financial Core



18\. Implement cost rollup

19\. Implement profit calculation

20\. Add dashboard summary endpoints



---



Rule:

No feature outside roadmap without updating this file.


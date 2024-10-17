Meeting 17.05.2024
---

- Attendance
	- Guerkan, Wissem, Rini, Tony

---

Progress
-

- c/r of a running cpu intensive container from a pod created from a sts kinda works
- we created a shell script that automates the whole procedure
- container/pod up and running within a second
- starts off at where we made the checkpoint
- started making the project accessible for future projects/next students


---

Questions
-
	
- how long should the ba paper be roughly?
	- usually 40-60 pages
	- doesnt really matter though :)

---

Notes
-

- maybe k8s messes up the inter migration
	- changes ip ranges?

- use normal pods/deployments instead of statefulsets
- focus on cluster to cluster migration

- criu logs
	- besides checkpointctl

---

Goals
-

- get CRIU/K8s done
- cleanup nfs
- c/r other apps
- Overleaf
	- related work
	- info
- test checkpointctl


---	
Meeting 26.04.2024
---

- Attendance
	- Guerkan, Wissem, Rini, Tony

---

Progress
-

- still debugging why the checkpointing via k8s doesnt work
- watched some Adrian Reber presentations
	- they more show how it works
	- less the actual setup

- (reading some papers)	

- checked Wissems work
	- ipip tunnel?
	- ...
	- make podman a worker in cluster
	- or test traffic with a new worker
	- with calico its an ip
		- not port

	- how do we access this calico ip/pods?
		- ...

	- hostfile?
		- maps names to smth

	- networkIO
		- locust from WITHIN cluster

---

Questions
-
	
- since the exam plan is out
- when do we know when our BA presentation is?
	- can we influence that a bit?
	- im asking because june will be a bit of a harsh month for me
		- since we found an appartment and are moving
	- some flexibility

---

Notes
-

- maybe runc configured wrongly?
- init cluster with feature gates
- more resources for new cluster to test out things?
- @people when msg in teams
- not sure if we need to use older k8s versions?
- check point non critical pods maybe?

---

Goals
-

- get CRIU/K8s done
- Overleaf
- NetworkIO
- test checkpointctl


---	
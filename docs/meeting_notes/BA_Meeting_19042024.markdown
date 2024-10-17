Meeting 19.04.2024
---

- Attendance
	- Guerkan, Wissem, Rini, Tony

---

Progress
-

- CRIU works with our nfs
	- we can create checkpoints
	- put them onto our nfs
	- restore them in another pod
	- BUT not with k8s yet
		- at least not fully

- direct api calls?
- checkpointing via api call doesnt work
- installed checkpointctl
	- https://kubernetes.io/blog/2023/03/10/forensic-container-analysis/
	- lists
		- checkpoint stats
		- container stats
		- dump stats like
			- freezing time
			- memdump time
			- memwrite time
			- memory pages scanned/written
			- etc...

---

Questions
-
	
- stateful migr
	- how we define stateful migr?
		- tony is more correct :)
		- about amount of info we preserve
		- "pseudo stateful migr"
		- pre vs post copy
			- pre usually preferred
			- ...

---

Notes
-

- Wissem having a look at it aswell
- calico
- monitoring
- we really wanna try CRIU in k8s!
- maybe rollback k8s version???
	- 1.26?
	- 1.25

---

Goals
-

- (Ask Adrian Reber?)
- fix criu with k8s!
- maybe rollback k8s version???
- start overleaf!


---	
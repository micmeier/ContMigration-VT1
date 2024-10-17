Meeting 22.03.2024
---

- Attendance
	- Guerkan, Wissem, Rini, Tony

---

Progress
-

- networkIO
	- still not working
	- networkIO is still giving us pains
	- -> cluster 3
	- we need a specific container runtime!
	- crio or containerd???
		- check which one is better for CRIU
	- calico???
		- ?
	- servicemesh?!!!!
	- ist.io???

- while being stuck with networkIO
- continued research on local reg
- we spent the last couple of days setting up local podman registry on the central node
	- are able to push images onto the reg
	- we can initiate pulling process onto individual nodes
		- but gives error messages while creating the container

- maybe we should put local reg into nfs!
- scp?
	

---

Questions
- 
	
- next week easterfriday
	- meeting?
	- -> email update
	- -> by thursday

---

Notes
-

- IEEE done

---

Goals
-

- finish NetworkIO
- pull from within cluster from local registry
	- as soon as this is done
		- create cpu image
			- push onto local reg
			
		- (look into setting up CRIU)

- Cluster3 set up
- 


---	
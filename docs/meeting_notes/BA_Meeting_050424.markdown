Meeting 05.04.2024
---

- Attendance
	- Guerkan, Wissem, Rini, Tony

---

Progress
- worked a bit more CPU Benchmark app
	- multicore
	- singlecore
	- modified shell script to pass args for
		- amount of cpu cores
		- cpu usage
		- containers to be created

- Rini been working hard with the cluster/service/networkIO

- once the service etc works
	- we can then continue with the local registry
	- and change the current yamls to pull image from local registry

- reached out to Wissem
	- for help	

---

Questions
- 
	
- That's nice. One question: have you also considered how to check that the service state is transfered and the app is continuing rather then restarting after the migration?
	- the application cycles between 4 different states
		- basically like a clock
		- ...

- presentation	IEEE?
	- June
	- may need to upload a video version
	- time budget?
	- teaser?
	- align content/style according to paper
	
- expert?
	- Eryk Schiller
	- ...
	- assistant prof
		- knows about migration
		- lmao!
		- cool guy
		- reference his papers!

---

Notes
- 

- check with Remo?
	- runshell
	- istio?
	- plan b?
	- check version of k8s
		- for criu etc

- start to read papers
	- for related work!!!

- maybe check Nana
	- Ingress
	- Egress

- calico
	- check overlay network?	

---

Goals
-

- EXPERIMENTAL SETUP VERY IMPORTANT!
	- proper evaluation
	- measure data!
- DONT GET BLOCKED
- maybe start with Overleaf
- containerize network application
- measurements
	- think about them
- sit down with Wissem for our problem
- finish NetworkIO
- setup local registry
	- as soon as this is done
		- look into setting up CRIU

---	
Meeting 10.05.2024
---

- Attendance
	- (Guerkan), Wissem, Rini, Tony

---

Progress
-


- worked out the theoretical steps to checkpoint/restore via k8s
	- have a container running

	- checkpoint via curl
		- creates a tar file

	- convert checkpoint to image using
		- docker/dockerfile/
		- buildah
	
	- push that image to local registry

	- create/prepare/adjust a yaml to start a pod/STS??? from that new image
		- which points to the new checkpoint image

	- apply the yaml
		- using kubectl apply -f <bla>.yaml

	- check if container is running

	- check if state is restored

- so all that works until the last step
	- pod is assigned to a worker
	- the image is succesfully pulled 
	- then an error occurs
		- failed to restore container
		- and we dont know why yet
		- off for debugging once again :(

- because of this
	- we havent done much else besides that
	- because this is the essence of our BA
	- if we cant get this running
	- we cant do anything

- we decided to have the checkpoints on our nfs
	- ...
	- so we dont have to manually send the checkpoint from node to node



---

Questions
-
	
- if we cant reach all the goals
	- make it reproduceable for next students?

- could we move the presentation to a later time? after lunch?	

---

Notes
-

- maybe runc configured wrongly?
- maybe a sitting with Wissem
- contact Reber?
- maybe different filesystems?

---

Goals
-

- restore done!!!
- Overleaf
- NetworkIO
- test checkpointctl
- live migrate!
	- measure


---	
from pydantic import BaseModel, Field
from typing import Optional, Dict, List

class OutputFields(BaseModel):
    container_id: Optional[str] = Field(None, alias="container.id")
    container_image_repository: Optional[str] = Field(None, alias="container.image.repository")
    container_image_tag: Optional[str] = Field(None, alias="container.image.tag")
    container_name: Optional[str] = Field(None, alias="container.name")
    evt_time: Optional[int] = Field(None, alias="evt.time")
    evt_type: Optional[str] = Field(None, alias="evt.type")
    k8s_ns_name: Optional[str] = Field(None, alias="k8s.ns.name")
    k8s_pod_name: Optional[str] = Field(None, alias="k8s.pod.name")
    proc_cmdline: Optional[str] = Field(None, alias="proc.cmdline")
    proc_exepath: Optional[str] = Field(None, alias="proc.exepath")
    proc_name: Optional[str] = Field(None, alias="proc.name")
    proc_pcmdline: Optional[str] = Field(None, alias="proc.pcmdline")
    proc_pname: Optional[str] = Field(None, alias="proc.pname")
    proc_tty: Optional[int] = Field(None, alias="proc.tty")
    user_loginuid: Optional[int] = Field(None, alias="user.loginuid")
    user_name: Optional[str] = Field(None, alias="user.name")
    user_uid: Optional[int] = Field(None, alias="user.uid")

class Alert(BaseModel):
    hostname: Optional[str]
    output: Optional[str]
    output_fields: Optional[OutputFields]
    priority: Optional[str]
    rule: Optional[str]
    source: Optional[str]
    tags: Optional[List[str]]
    time: Optional[str]
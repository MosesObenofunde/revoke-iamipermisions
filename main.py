import google.auth
import googleapiclient.discovery
import re
import os

project_id=os.environ.get('GCP_PROJECT')
remove_domain=["gmail.com"]
version=1
print(project_id)

def revoke_iam_access(request):
    request_json = request.get_json()
    service = googleapiclient.discovery.build("cloudresourcemanager", "v1")
    """Gets IAM policy for a project."""
    policy = (
        service.projects()
        .getIamPolicy(
            resource=project_id,
            body={"options": {"requestedPolicyVersion": version}},
        )
        .execute()
    )
    #print(policy)
    print("Removing the iam role bindings for the below accounts")
    for dm in remove_domain:
      for acc in policy["bindings"]:
          for member in acc["members"]:
            if dm in member:
              binding = next(b for b in policy["bindings"] if b["role"] == acc["role"])
              if member in binding["members"]:
                binding["members"].remove(member)
                print(member, acc["role"])
    """Sets IAM policy for a project."""
    service.projects().setIamPolicy(resource=project_id, body={"policy": policy}).execute()
    return "success"

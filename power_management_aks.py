# from azure.mgmt.containerservice import ContainerServiceClient # needed to create client
# containerservice_client = ContainerServiceClient(get_credentials(), SUBSCRIPTION) # same way like you would for the resource_management_client
# parameters = ManagedCluster(
#     location=location,
#     dns_prefix=dns_prefix,
#     kubernetes_version=kubernetes_version,
#     tags=stags,
#     service_principal_profile=service_principal_profile, # this needs to be a model as well
#     agent_pool_profiles=agent_pools, # this needs to be a model as well
#     linux_profile=linux_profile, # this needs to be a model as well
#     enable_rbac=true
# )
# containerservice_client.managed_clusters.create_or_update(resource_group, name, parameters)

from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.containerservice.models import ManagedCluster
# from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.containerservice.models import ManagedCluster
from azure.mgmt.resource import ResourceManagementClient
from azure.identity import ClientSecretCredential
import os


class AksManage():
  def __init__(self):
    # Client initialization
    self.client_id = os.environ["client_id"]
    self.secret = os.environ["client_secret"]
    self.tenant_id = os.environ["tenant_id"]
    self.subscription_id = os.environ["subscription_id"]
    self.resource_group_name = os.environ["resource_group_name"]
    self.client = self._get_client()

  def _get_client(self):
    #credentials = ServicePrincipalCredentials(client_id=self.client_id, secret=self.secret, tenant=self.tenant_id)
    credentials = ClientSecretCredential(
      tenant_id=self.tenant_id,
      client_id=self.client_id,
      client_secret=self.secret
    )

    subscription_id = self.subscription_id
    client = ContainerServiceClient(credentials, subscription_id,api_version='2018-03-31')
    resouce_client=ResourceManagementClient(credentials,subscription_id)
    resouce_list=resouce_client.resources.list_by_resource_group(self.resource_group_name)
    for resource in list (resouce_list) :
      if resource.type == 'Microsoft.ContainerService/managedClusters':
        kub_name=resource.name
        location=resource.location
        print("ResourceName:", kub_name, "ResourceLocation:",location )
        get_aks = client.managed_clusters.get(self.resource_group_name, resource.name)
        print(get_aks.id)
        aks_get_details = client.managed_clusters.get_upgrade_profile(self.resource_group_name, resource.name)
        print(aks_get_details)
        object_methods = [method_name for method_name in dir(client.managed_clusters.models)]
                  # if callable(getattr(object, method_name))]

        # stop = client.managed_clusters.begin_stop(self.resource_group_name, resource.name)
        print(object_methods)
    return client

def main():
  aks = AksManage()

if __name__ == '__main__':
    main()
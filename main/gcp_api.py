from django.conf import settings

from google.oauth2 import service_account
from google.cloud import compute_v1

project="annular-axe-402720"
region="northamerica-northeast2"
zone=f"{region}-a"

credentials = service_account.Credentials.from_service_account_file('key.json') if settings.DEBUG else None
# If running locally. If we're in a VM, we set this to null

client = compute_v1.InstancesClient(credentials=credentials)

def create(name, ssh_pubkey):
    disk = compute_v1.AttachedDisk(
        auto_delete=True,
        boot=True,
        initialize_params=compute_v1.AttachedDiskInitializeParams(
            disk_size_gb=15,
            disk_type=f"https://www.googleapis.com/compute/v1/projects/{project}/zones/{zone}/diskTypes/pd-balanced",
            source_image="projects/debian-cloud/global/images/family/debian-11"
        )
    )


    interface = compute_v1.NetworkInterface(
        subnetwork=f"projects/{project}/regions/{region}/subnetworks/default",
        access_configs=[compute_v1.AccessConfig()]
    )

    instance_resource = compute_v1.Instance(
        machine_type=f"zones/{zone}/machineTypes/e2-medium",
        name=name,
        disks=[disk],
        network_interfaces=[interface],
        metadata=compute_v1.Metadata(items=[
            compute_v1.Items(key="ssh-keys", value="you:" + ssh_pubkey + ' google-ssh {"userName":"you", "expireOn":"2222-12-04T20:12:00+0000"}'),
            compute_v1.Items(key="serial-port-enable", value="true"),
            compute_v1.Items(key="startup-script", value='''
curl --proto '=https' --tlsv1.2 -sSf -L https://install.determinate.systems/nix | sh -s -- install --no-confirm
. /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh
nix profile install nixpkgs#cowsay nixpkgs#lolcat
''')
        ])
    )
    
    client.insert(project=project, zone=zone, instance_resource=instance_resource).result()

    ip = client.get(zone=zone, project=project, instance=name).network_interfaces[0].access_configs[0].nat_i_p

    return ip

def delete(instance):
    response = client.delete(
        project=project,
        zone=zone,
        instance=instance
    )

    return response

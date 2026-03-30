import oci
import os
import time
import sys

COMPARTMENT_ID = os.getenv("OCI_COMPARTMENT_ID")
AVAILABILITY_DOMAIN = os.getenv("OCI_AD")
IMAGE_ID = os.getenv("OCI_IMAGE_ID")
SUBNET_ID = os.getenv("OCI_SUBNET_ID")
SHAPE = "VM.Standard.A1.Flex"

def launch_instance(compute_client):
    """Attempts to provision a free-tier ARM instance."""
    launch_details = oci.core.models.LaunchInstanceDetails(
        display_name="DevOps-Automation-Instance",
        compartment_id=COMPARTMENT_ID,
        availability_domain=AVAILABILITY_DOMAIN,
        shape=SHAPE,
        shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(ocpus=4, memory_in_gbs=24),
        source_details=oci.core.models.InstanceSourceViaImageDetails(image_id=IMAGE_ID),
        create_vnic_details=oci.core.models.CreateVnicDetails(subnet_id=SUBNET_ID, assign_public_ip=True)
    )

    try:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Attempting to provision ARM instance...")
        response = compute_client.launch_instance(launch_details)
        print("✅ Success! Instance is being provisioned.")
        print(f"Instance ID: {response.data.id}")
        return True
    except oci.exceptions.ServiceError as e:
        if e.status == 500 and "Out of host capacity" in e.message:
            print("❌ Capacity reached. Retrying in 60 seconds...")
        else:
            print(f"⚠️ Unexpected Error: {e.message}")
        return False

def main():
    config = oci.config.from_file()
    compute_client = oci.core.ComputeClient(config)

    # Hunt loop
    while True:
        success = launch_instance(compute_client)
        if success:
            break
        time.sleep(60)

if __name__ == "__main__":
    main()
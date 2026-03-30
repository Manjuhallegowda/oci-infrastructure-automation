import oci
import os
import time
import logging
from threading import Thread
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("hunter.log"), logging.StreamHandler()]
)

class OCIHunter:
    def __init__(self):
        self.config = oci.config.from_file()
        self.compute_client = oci.core.ComputeClient(self.config)
        
        self.compartment_id = os.getenv("OCI_COMPARTMENT_ID")
        self.subnet_id = os.getenv("OCI_SUBNET_ID")
        self.image_id = os.getenv("OCI_IMAGE_ID")
        self.shape = "VM.Standard.A1.Flex"
        
        self.ads = [
            os.getenv("OCI_AD_1"), 
            os.getenv("OCI_AD_2"), 
            os.getenv("OCI_AD_3")
        ]

    def create_instance(self, ad_name):
        launch_details = oci.core.models.LaunchInstanceDetails(
            display_name=f"Ranstack-Prod-Node-{datetime.now().strftime('%H%M')}",
            compartment_id=self.compartment_id,
            availability_domain=ad_name,
            shape=self.shape,
            shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(ocpus=4, memory_in_gbs=24),
            source_details=oci.core.models.InstanceSourceViaImageDetails(image_id=self.image_id),
            create_vnic_details=oci.core.models.CreateVnicDetails(subnet_id=self.subnet_id, assign_public_ip=True)
        )

        while True:
            try:
                logging.info(f"Targeting AD: {ad_name} | Searching for resources...")
                response = self.compute_client.launch_instance(launch_details)
                logging.info(f"🎯 SUCCESS! Instance {response.data.id} is live in {ad_name}")
                os._exit(0)  # Stop all threads once one instance is caught
            except oci.exceptions.ServiceError as e:
                if e.status == 500 and "Out of host capacity" in e.message:
                    logging.warning(f"Capacity Full in {ad_name}. Cooling down for 30s...")
                    time.sleep(30)
                else:
                    logging.error(f"Critical API Error in {ad_name}: {e.message}")
                    break

    def start_hunt(self):
        threads = []
        logging.info("🚀 Initializing Global OCI Hunter Mode...")
        for ad in self.ads:
            if ad:
                t = Thread(target=self.create_instance, args=(ad,))
                t.start()
                threads.append(t)
        
        for t in threads:
            t.join()

if __name__ == "__main__":
    required_vars = ["OCI_COMPARTMENT_ID", "OCI_SUBNET_ID", "OCI_IMAGE_ID"]
    if all(os.getenv(var) for var in required_vars):
        hunter = OCIHunter()
        hunter.start_hunt()
    else:
        logging.error("Missing Environment Variables. Check your Runbook.")
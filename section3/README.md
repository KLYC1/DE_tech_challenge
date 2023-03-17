## Section 3

**Assumptions:**

1. The company decided on using Kafka instead of google pub/sub service to stream images, assuming it is already implemented and hosted on the cloud, assuming cloud provider is google cloud.
2. The image processing code is already written and can be deployed to a Compute Engine virtual machine.
3. The company has a database administrator who can manage the database and enforce the data retention policy on google cloud storage.
4. The BI resource is already implemented and hosted on BigQuery.

**Description of the Architecture:**

The architecture consists of several components to process images uploaded by users through the web application API and the Kafka stream.

1. User uploads (first image source): Users can upload images to the web application through an API. The uploaded images and metadata are then stored in Cloud Storage bucket for processing.

2. Kafka stream (second image source): The Kafka stream is responsible for uploading images to the cloud environment. The Kafka brokers component is responsible for managing the stream and forwarding the images. The uploaded images and metadata are then stored in Cloud Storage bucket for processing.

3. Image processing: The compute engine will host the codes written by the company's software engineer and responsible for processing the images that are stored in the Cloud Storage bucket. The output of the processing is then stored in a Cloud Storage bucket. 

4. Metadata storage: The processed images and their metadata are stored in a Cloud Spanner database / Cloud storage for archival purposes.

5. Data retention policy: The data retention policy component in google cloud storage / cloud spanner is responsible for enforcing the company's policy to purge the images and metadata from the database after 7 days. Placing a retention policy on a bucket ensures that all current and future objects in the bucket cannot be deleted or replaced until they reach the age you define in the retention policy.

6. Business Intelligence (BI) resources is hosted on BigQuery, providing access to the data for analysts to perform analytical computations, which can directly query the data stored in Cloud Spanner / storage.

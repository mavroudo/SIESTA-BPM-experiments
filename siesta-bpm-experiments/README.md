#### Deployment
The complete infrastructure of our solution, which includes the preprocessing component, query processor, database layer, and an intuitive user interface, can be easily deployed by following these steps:

1. Clone the repository of SIESTA-demo:
    ```bash
    git clone https://github.com/siesta-tool/siesta-demo
    ```
2. Navigate inside the directory:
    ```bash
    cd siesta-demo
    ```
3. Deploy the entire infrastructure using Docker. Ensure that both Docker and Docker Compose are installed:
    ```bash
    docker compose up 
    ```
   Note that this will deploy Minio (an open-source implementation of S3) as a database. If you need to change it, comment out both **minio** and **createbuckets** services, and uncomment the **cassandra** service.

   Once the infrastructure is up and running, you can access it through _localhost_.

#### Preprocessing
The next step is to index a dataset. The currently supported extensions are _.xes_ and _.withTimestamp_ (testing datasets). However, any new extensions can be employed by extending the preprocessing component.

1. Click on **Preprocessing** (left panel) and then click **Add**. This will open a new window to guide you through the indexing process.
2. Choose the event log that you want to index and click **Next**.
3. Define the database (S3 or Cassandra). The default parameters are correctly set to work with Docker Compose, but if you want to deploy the database externally, you can set the parameters here.
4. Choose the name of the index (logname). If the name does not exist, it will open two additional parameters (lookback and split every days). Set the lookback parameter equal to the duration of the longest-running trace to avoid missing any event-pair. The remaining parameters can be left at their default values. However, if the event log has more than 10,000 events, you might need to allocate additional memory to Spark. You can do this by adding the parameter `--driver-memory 10g` to the **Spark Parameters**.
5. The final step will present an overview of the indexing process. If everything looks good, click **Submit**.

Depending on the event log size and available resources, the process can take from a few seconds to several minutes. Use the refresh button to update the status of the process. When the status changes to **finished**, click the refresh button in the left panel and wait for the logname to appear under the indexes.

#### Accessing SIESTA's functionalities
By clicking a logname from the **Indexes** list, you can access the various functionalities of SIESTA:
1. Basic Statistics
2. Pattern Detection
3. Pattern Continuation
4. Mining DECLARE Constraints

In the Mining Constraints section, you can choose a subset or all the DECLARE constraints and click **Submit**. The query will be executed and the results will appear below. You can also choose to download the results in a CSV file (from the blue arrow).

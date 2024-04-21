=================================
API Documentation for Tech Challenge
=================================

Welcome to the Tech Challenge API documentation. This guide provides a comprehensive overview of the installation process, API functionalities, and usage instructions to get you started.

Installation
------------

To install the necessary components for the API, navigate to the `sh` directory and execute the installation scripts in the following order:

1. **Initial Setup**

   .. code-block:: bash

       sh 00-install.sh

2. **Build Docker Containers**

   .. code-block:: bash

       sh 90-build-container.sh

3. **Run Application**

   .. code-block:: bash

       sh 01-run.sh

API Documentation
-----------------

This section details each of the available API functions within the `api.py` file located in `src/tech_challenge_001`.

1. **Root Endpoint**
   - **Endpoint**: `/`
   - **Method**: GET
   - **Description**: Automatically redirects the user to the interactive API documentation (Swagger UI).
   - **Example Call**:

     .. code-block:: bash

         curl http://localhost:8000/

2. **Update Data Endpoint**
   - **Endpoint**: `/update_data`
   - **Method**: GET
   - **Description**: Triggers a comprehensive update of all datasets used by the API, ensuring the most up-to-date analysis capabilities.
   - **Example Call**:

     .. code-block:: bash

         curl http://localhost:8000/update_data

3. **Query Endpoint**
   - **Endpoint**: `/query`
   - **Method**: GET
   - **Authentication**: Required (API key via OAuth2).
   - **Description**: Offers direct database interaction for executing custom SQL queries.
   - **Example Call**:

     .. code-block:: bash

         curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8000/query?sql=YOUR_SQL_QUERY

4. **Processamento Data Endpoint**
   - **Endpoint**: `/processamento`
   - **Method**: GET
   - **Authentication**: Required (API key via OAuth2).
   - **Description**: Provides access to grape processing data with options for detailed filtering.
   - **Example Call**:

     .. code-block:: bash

         curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8000/processamento?id=1&control=organic&cultivar=variety&ano=2020

5. **Comércio Data Endpoint**
   - **Endpoint**: `/comercio`
   - **Method**: GET
   - **Authentication**: Required (API key via OAuth2).
   - **Description**: Fetches trade data with options for detailed filtering.
   - **Example Call**:

     .. code-block:: bash

         curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8000/comercio?id=2&produto=wine&detalhe_produto=red_wine&ano=2021

Building and Running with Docker
--------------------------------

To build and run the API in a Docker container, execute the following scripts:

.. code-block:: bash

    sh 90-build-container.sh
    sh 91-run-container.sh

Kubernetes Deployment
---------------------

**Creating Kubernetes Secrets for API Keys:**

To create a Kubernetes secret for storing API keys:

.. code-block:: bash

    kubectl create secret generic api-keys --from-file=keys/api_keys_list.txt

**Deploying to Kubernetes:**

To deploy the application to a Kubernetes cluster:

.. code-block:: bash

    kubectl apply -f sh/tech-challenge-dpl.yaml

**Port Forwarding for Local Access:**

To access the Kubernetes-deployed service locally:

.. code-block:: bash

    sh 94-port-forward.sh

Usage
-----

To use this API, start the server by running:

.. code-block:: bash

    sh 01-run.sh

Once the server is running, you can interact with the API via the defined endpoints using tools like curl or Postman.

Testing
-------

To run the automated tests for this project, execute:

.. code-block:: bash

    sh 99-test.sh

Contributing
------------

Contributions are welcome! Please refer to `docs/contributing.rst` for guidelines on how to contribute to this project.

License
-------

This project is licensed under the MIT License. For more details, see `docs/license.rst`.

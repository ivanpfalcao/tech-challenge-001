=================================
API Documentation for Tech Challenge
=================================

Welcome to the Tech Challenge API documentation. This guide provides a comprehensive overview of the installation process, API functionalities, and usage instructions to get you started.

Building and Running with Docker
--------------------------------

To build and run the API in a Docker container, execute the following scripts:

.. code-block:: bash

    bash 90-build-container.sh
    bash 91-run-container.sh

Kubernetes Deployment
---------------------

**Creating Kubernetes Secrets for API Keys:**

To create a Kubernetes secret for storing API keys (you can run multiple times to add multiple keys):

.. code-block:: bash

    bash sh/92-generate-api-key-file.sh "{API_KEY}"

**Deploying to Kubernetes:**

To deploy the application to a Kubernetes cluster:

.. code-block:: bash

    kubectl -n "${NAMESPACE}" apply -f sh/tech-challenge-dpl.yaml

**Port Forwarding for Local Access:**

To access the Kubernetes-deployed service locally:

.. code-block:: bash

    bash sh/94-port-forward.sh

API Documentation
-----------------

This section details each of the available API functions within the `api.py` file located in `src/tech_challenge_001`.

1. **Root Endpoint**
   - **Endpoint**: `/`
   - **Method**: GET
   - **Description**: Automatically redirects the user to the interactive API documentation (Swagger UI).
   - **Example Call**:

     .. code-block:: bash

         curl -i -v http://localhost:8000/

2. **Update Data Endpoint**
   - **Endpoint**: `/update_data`
   - **Method**: GET
   - **Description**: Triggers a comprehensive update of all datasets used by the API, ensuring the most up-to-date analysis capabilities.
   - **Example Call**:

     .. code-block:: bash

         curl -i -v http://localhost:8000/update_data

3. **Query Endpoint**
   - **Endpoint**: `/query`
   - **Method**: GET
   - **Authentication**: Required (API key via OAuth2).
   - **Description**: Offers direct database interaction for executing custom SQL queries.
   - **Example Call**:

     .. code-block:: bash

         curl -i -v -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8000/query?sql=YOUR_SQL_QUERY

4. **Processamento Data Endpoint**
   - **Endpoint**: `/processamento`
   - **Method**: GET
   - **Authentication**: Required (API key via OAuth2).
   - **Description**: Provides access to grape processing data with options for detailed filtering.
   - **Example Call**:

     .. code-block:: bash

         curl -i -v -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8000/processamento?id=1&control=organic&cultivar=variety&ano=2020

5. **Comércio Data Endpoint**
   - **Endpoint**: `/comercio`
   - **Method**: GET
   - **Authentication**: Required (API key via OAuth2).
   - **Description**: Fetches trade data with options for detailed filtering.
   - **Example Call**:

     .. code-block:: bash

         curl -i -v -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8000/comercio?id=2&produto=wine&detalhe_produto=red_wine&ano=2021


License
-------

This project is licensed under the MIT License. For more details, see `docs/license.rst`.

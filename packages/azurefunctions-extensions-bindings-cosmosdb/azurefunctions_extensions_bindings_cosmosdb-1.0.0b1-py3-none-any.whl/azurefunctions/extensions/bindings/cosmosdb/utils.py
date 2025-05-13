#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License.
import os
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient as CosmosClientSdk


def get_connection_string(connection_string: str) -> str:
    """
    Validates and returns the Cosmos DB connection string or endpoint URI.
    Supports both App Settings and managed identity-based configurations.

    Expected formats:
    1. Not using managed identity: the environment variable exists as is.
    2. Using managed identity: __accountEndpoint must be appended.
    3. None of these cases existed, so the connection variable is invalid.
    """
    if connection_string is None:
        raise ValueError(
            "Cosmos DB connection string cannot be None. "
            "Please provide a connection string or account endpoint."
        )
    elif connection_string in os.environ:
        return os.getenv(connection_string)
    elif connection_string + "__accountEndpoint" in os.environ:
        return os.getenv(connection_string + "__accountEndpoint")
    else:
        raise ValueError(
            f"Cosmos DB connection string {connection_string} does not exist. "
            f"Please make sure that it is a defined App Setting."
        )


def using_managed_identity(connection_name: str) -> bool:
    """
    Determines if managed identity is being used for Cosmos DB access
    by checking for a __accountEndpoint suffix.
    """
    return os.getenv(connection_name + "__accountEndpoint") is not None


def get_cosmos_client(using_managed_identity: bool,
                      connection: str, preferred_locations: str) -> CosmosClientSdk:
    pl = []
    if preferred_locations:
        pl = [location.strip() for location in preferred_locations.split(",")]

    cosmos_client = (
        CosmosClientSdk(
            url=connection, credential=DefaultAzureCredential(),
            preferred_locations=pl
        )
        if using_managed_identity
        else CosmosClientSdk.from_connection_string(connection, preferred_locations=pl)
    )

    return cosmos_client

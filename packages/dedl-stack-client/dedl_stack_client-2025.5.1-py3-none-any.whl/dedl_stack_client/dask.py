"""
Copyright 2024 EODC GmbH

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from dask_gateway import Gateway
from distributed import Client
from contextlib import contextmanager
import requests


class DaskMultiCluster:
    gateway_registry = {}
    gateway = {}
    cluster = {}
    client = {}

    bridges_url = \
        "https://destination-earth.github.io/DestinE_EUMETSAT_DEDL_Stack_Client/bridges.json"

    def __init__(self, auth):
        # load bridge configurations
        bridges_config = requests.get(self.bridges_url)
        if bridges_config.status_code != 200:
            bridges_config.raise_for_status()
        bridges = bridges_config.json()

        # set authenticator
        self.authenticator = auth

        # init Dask Gateways per bridge
        for site in bridges:
            # connect to gateway
            try:
                gw = Gateway(
                    address=bridges[site]["address"],
                    proxy_address=bridges[site]["proxy_address"],
                    auth=self.authenticator,
                )
                # check availability of gateway
                gw.get_versions()
            except Exception as e:
                print(f"Error connecting to {bridges[site]['name']}")
                continue
            else:
                self.gateway_registry[site] = bridges[site]
                self.gateway[site] = gw
                

    def print_registry(self):
        print(self.gateway_registry)

    def get_gateways(self) -> None:
        for site in self.gateway_registry:
            print(f"{site}: {self.gateway_registry[site]}")

    def new_cluster(self, *args, **kwargs) -> None:
        for site in self.gateway_registry:
            # get new cluster object
            print(f"Create new cluster for {self.gateway_registry[site]['name']}")
            self.cluster[site] = self.gateway[site].new_cluster(*args, **kwargs)
            self.cluster[site].adapt(
                minimum=self.gateway_registry[site]["default_config"]["min"],
                maximum=self.gateway_registry[site]["default_config"]["max"],
            )
            self.client[site] = self.cluster[site].get_client(set_as_default=False)

    def compute(self, data, location_key: str = "location", **kwargs):
        return self.client[data.attrs[location_key]].compute(data, **kwargs)

    @contextmanager
    def as_current(self, location: str = "central") -> Client:
        yield self.client[location]

    def get_cluster_url(self):
        for site in self.gateway_registry:
            print(self.cluster[site].dashboard_link)

    def shutdown(self):
        for site in self.gateway_registry:
            self.cluster[site].close()

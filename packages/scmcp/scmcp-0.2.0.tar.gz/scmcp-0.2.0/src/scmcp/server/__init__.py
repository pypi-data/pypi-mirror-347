
import asyncio
from fastmcp import FastMCP
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any


import scanpy_mcp.server as sc_server
import liana_mcp.server as li_server
import cellrank_mcp.server as cr_server
import decoupler_mcp.server as dc_server



class AdataState:
    def __init__(self):
        self.adata_dic ={"exp": {}, "splicing": {}, "activity": {}}
        self.active_id = None
        self.metadata = {}
        self.cr_kernel = {}
        self.cr_estimator = {}

    def get_adata(self, sampleid=None, dtype="exp"):
        try:
            if self.active_id is None:
                return None
            sampleid = sampleid or self.active_id
            return self.adata_dic[dtype][sampleid]
        except KeyError as e:
            raise KeyError(f"Key {e} not found in adata_dic[{dtype}]. check sampleid or dtype are right")
        except Exception as e:
            raise Exception(f"Error: {e}")
    
    def set_adata(self, adata, sampleid=None, sdtype="exp"):
        sampleid = sampleid or self.active_id
        self.adata_dic[sdtype][sampleid] = adata


ads = AdataState()

@asynccontextmanager
async def adata_lifespan(server: FastMCP) -> AsyncIterator[Any]:
    yield ads


sc_mcp = FastMCP("SC-MCP-Server", lifespan=adata_lifespan)

asyncio.run(sc_server.setup())
asyncio.run(li_server.setup(modules=["ccc", "pl"]))
asyncio.run(cr_server.setup(modules=["pp", "kernel", "estimator", "pl"]))
asyncio.run(dc_server.setup(modules=["if", "pl"]))


async def setup(modules=None):
    mcp_dic = {
        "sc": sc_server.scanpy_mcp, 
        "li": li_server.liana_mcp, 
        "cr": cr_server.cellrank_mcp, 
        "dc": dc_server.decoupler_mcp
        }
    if modules is None or modules == "all":
        modules = ["sc", "li", "cr", "dc"]
    for module in modules:
        await sc_mcp.import_server(module, mcp_dic[module])

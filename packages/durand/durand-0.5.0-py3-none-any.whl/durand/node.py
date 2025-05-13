from typing import List
from dataclasses import dataclass

from .network import NetworkABC
from .object_dictionary import ObjectDictionary
from .services.sdo import SDOServer
from .services.pdo import TPDO, RPDO
from .eds import EDS
from .services.nmt import NMTSlave, StateEnum
from .services.lss import LSSSlave
from .services.sync import SyncConsumer
from .services.emcy import EMCYProducer
from .services.heartbeat import HeartbeatProducer
from .object_dictionary import Variable, Record
from .datatypes import DatatypeEnum as DT


SDO_SERVERS = 127


@dataclass(frozen=True)
class NodeCapabilities:
    sdo_servers: int = 128
    rpdos: int = 512
    tpdos: int = 512


class Node:
    def __init__(
        self,
        network: NetworkABC,
        node_id: int,
        od: ObjectDictionary = None,
        capabilities: NodeCapabilities = NodeCapabilities(),
    ):

        self.network = network
        self.node_id = node_id
        od = ObjectDictionary() if od is None else od
        self.object_dictionary = od
        self.eds = EDS(self)

        self.nmt = NMTSlave(self)
        self.sync = SyncConsumer(self)

        self.tpdo = [TPDO(self, i) for i in range(capabilities.tpdos)]
        self.rpdo = [RPDO(self, i) for i in range(capabilities.rpdos)]

        self.eds.device_info.NrOfRXPDO = capabilities.rpdos
        self.eds.device_info.NrOfTXPDO = capabilities.tpdos

        self.sdo_servers: List[SDOServer] = []

        assert (
            1 <= SDO_SERVERS <= 128
        ), "Number of SDO servers has to be between 1 and 128"

        for index in range(capabilities.sdo_servers):
            self.sdo_servers.append(SDOServer(self, index))

        self.heartbeat_producer = HeartbeatProducer(self)
        self.lss = LSSSlave(self)
        self.emcy = EMCYProducer(self)

        od[0x1000] = Variable(DT.UNSIGNED32, "ro", 0, name="Device Type")

        od[0x1008] = Variable(
            DT.VISIBLE_STRING, "ro", b"", name="Manufacturer Device Name"
        )
        od[0x1009] = Variable(
            DT.VISIBLE_STRING, "ro", b"", name="Manufacturer Hardware Version"
        )
        od[0x100A] = Variable(
            DT.VISIBLE_STRING, "ro", b"", name="Manufacturer Software Version"
        )

        # Identity object
        identity_record = Record(name="Identity Object")
        identity_record[1] = Variable(DT.UNSIGNED32, "ro", 0, name="Vendor-ID")
        identity_record[2] = Variable(DT.UNSIGNED32, "ro", 0, name="Product Code")
        identity_record[3] = Variable(DT.UNSIGNED32, "ro", 0, name="Revision Number")
        identity_record[4] = Variable(DT.UNSIGNED32, "ro", 0, name="Serial Number")

        od[0x1018] = identity_record
        self.nmt.set_state(StateEnum.PRE_OPERATIONAL)

        # EDS provider
        od[0x1021] = Variable(DT.DOMAIN, "ro", name="Store EDS")
        od[0x1022] = Variable(DT.UNSIGNED8, "ro", value=0, name="Store Format")
        od.set_read_callback(0x1021, 0, lambda: self.eds.content.encode())


MinimalNodeCapabilities = NodeCapabilities(sdo_servers=1, rpdos=4, tpdos=4)


class MinimalNode(Node):
    def __init__(self, network: NetworkABC, node_id: int, od: ObjectDictionary = None):
        Node.__init__(self, network, node_id, od, MinimalNodeCapabilities)

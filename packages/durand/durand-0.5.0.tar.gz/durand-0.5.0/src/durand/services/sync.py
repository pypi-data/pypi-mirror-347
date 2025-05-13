from typing import TYPE_CHECKING

from durand.object_dictionary import Variable
from durand.datatypes import DatatypeEnum as DT
from durand.callback_handler import CallbackHandler


if TYPE_CHECKING:
    from durand.node import Node


class SyncConsumer:
    """This service is listening on a specified COB ID for sync messages

    Other services can register callbacks to sync messages via Sync.callbacks (CallbackHandler)
    """

    def __init__(self, node: "Node"):
        self._node = node
        self._cob_id = 0x80

        self.callbacks = CallbackHandler()

        node.object_dictionary[0x1005] = Variable(
            DT.UNSIGNED32, "rw", self._cob_id, name="COB-ID SYNC"
        )
        node.object_dictionary.update_callbacks[(0x1005, 0)].add(self._update_cob_id)

        node.network.add_subscription(cob_id=self._cob_id, callback=self._receive_sync)

    @property
    def cob_id(self):
        return self._cob_id

    @cob_id.setter
    def cob_id(self, cob: int):
        self._node.object_dictionary.write(0x1005, 0, cob)  # triggers _update_cob_id

    def _update_cob_id(self, value):
        self._node.network.remove_subscription(
            cob_id=self._cob_id, callback=self._receive_sync
        )
        self._cob_id = value & 0x1FFF_FFFF
        self._node.network.add_subscription(
            cob_id=self._cob_id, callback=self._receive_sync
        )

    def _receive_sync(self, _cob_id: int, _msg: bytes):
        self.callbacks.call()

# Automatically generated by pb2py
import protobuf as p


class TxOutputBinType(p.MessageType):
    FIELDS = {
        1: ('amount', p.UVarintType, 0),  # required
        2: ('script_pubkey', p.BytesType, 0),  # required
        3: ('decred_script_version', p.UVarintType, 0),
    }

    def __init__(
        self,
        amount: int = None,
        script_pubkey: bytes = None,
        decred_script_version: int = None,
        **kwargs,
    ):
        self.amount = amount
        self.script_pubkey = script_pubkey
        self.decred_script_version = decred_script_version
        p.MessageType.__init__(self, **kwargs)

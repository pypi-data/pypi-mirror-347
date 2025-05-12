from __future__ import annotations

from typing import Union

from pytoniq_core import Address, Cell, StateInit, begin_cell

from ...royalty_params import RoyaltyParams
from ....client import Client
from ....contract import Contract


class Collection(Contract):

    @classmethod
    async def get_royalty_params(
            cls,
            client: Client,
            collection_address: Union[Address, str],
    ) -> RoyaltyParams:
        """
        Gets the royalty parameters of the collection.

        :param client: The client instance.
        :param collection_address: The address of the collection.
        :return: The royalty parameters of the collection.
        """
        if isinstance(collection_address, str):
            collection_address = Address(collection_address)

        method_result = await client.run_get_method(
            address=collection_address.to_str(),
            method_name="royalty_params",
        )
        base = method_result[0]
        factor = method_result[1]
        royalty_address = method_result[2]

        return RoyaltyParams(base, factor, royalty_address)

    @classmethod
    async def get_nft_address_by_index(
            cls,
            client: Client,
            index: int,
            collection_address: Union[Address, str],
    ) -> Address:
        if isinstance(collection_address, Address):
            collection_address = collection_address.to_str()

        method_result = await client.run_get_method(
            address=collection_address,
            method_name="get_nft_address_by_index",
            stack=[index],
        )

        return method_result[0]

    @classmethod
    def calculate_nft_item_address(
            cls,
            index: int,
            nft_item_code: str,
            collection_address: Union[Address, str],
            index_len: int = 64,
    ) -> Address:
        if isinstance(collection_address, Address):
            collection_address = collection_address.to_str()

        code = Cell.one_from_boc(nft_item_code)
        data = begin_cell().store_uint(index, index_len).store_address(collection_address).end_cell()
        state_init = StateInit(code=code, data=data)

        return Address((0, state_init.serialize().hash))

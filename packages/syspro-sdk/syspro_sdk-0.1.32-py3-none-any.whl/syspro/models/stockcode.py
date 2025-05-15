import xml.etree.ElementTree as ET
from .base import SysproBaseModel
from ..utils import append_custom_columns_and_values

class StockCodeModel(SysproBaseModel):

    def get(self, id, multi_media_image_type:str = None, include_history="N",
            include_bins="N", include_lots="N", include_serials="Y", include_move="Y",
            move_date_sequence="A", move_start_date=None, max_number_move="100",
            include_custom_forms="Y", include_move_issues="N", include_move_transfers="N",
            include_move_receipts="N", include_move_physical="N", include_move_adjustments="N",
            include_move_costchange = "N", include_move_costmods = "N", include_ecc = "N",
            include_approvedmanuf = "N", include_narrations = "N", narrations_in_block = "N"):
        
        xmlin = {
            "@attributes": {
                "xmlns:xsd": "http://www.w3.org/2001/XMLSchema-instance",
                "xsd:noNamespaceSchemaLocation": "INVQRY.XSD"
            },
            "Key": {
                "StockCode": id
            },
            "Option": {
                "MultiMediaImageType": multi_media_image_type,
                "IncludeHistory": include_history,
                "IncludeBins": include_bins,
                "IncludeLots": include_lots,
                "IncludeSerials": include_serials,
                "IncludeMovements": include_move,
                "MovementDateSequence": move_date_sequence,
                "MovementStartDate": move_start_date,
                "MaxNumberMovements": max_number_move,
                "IncludeCustomForms": include_custom_forms,
                "IncludeMovementIssues": include_move_issues,
                "IncludeMovementTransfers": include_move_transfers,
                "IncludeMovementReceipts": include_move_receipts,
                "IncludeMovementPhysical": include_move_physical,
                "IncludeMovementAdjustments": include_move_adjustments,
                "IncludeMovementCostChanges": include_move_costchange,
                "IncludeMovementCostMods": include_move_costmods,
                "IncludeEcc": include_ecc,
                "IncludeApprovedManuf": include_approvedmanuf,
                "IncludeNarrations": include_narrations,
                "ReturnNarrationsinBlock": narrations_in_block,
                "XslStylesheet": None
            }
        }
        
        self.get_items(bo="INVQRY", id=id, xmlin=xmlin)

        if include_custom_forms == "Y":
            self.data["InvQuery"]["StockItem"] = append_custom_columns_and_values(self.data.get("InvQuery").get("StockItem"))
            del self.data["InvQuery"]["StockItem"]["CustomForm"]

        return self

    def find(self, id, columns: list = ["StockCode"]):
        where = {
            "Expression": {
                "OpenBracket": "(",
                "Column": "StockCode",
                "Condition": "EQ",
                "Value": id,
                "CloseBracket": ")"
            }
        }
        order_by = {
            "Column": "StockCode"
        }

        return self._find(id=id, table_name="StockMaster", columns=columns, where=where, order_by=order_by)

        
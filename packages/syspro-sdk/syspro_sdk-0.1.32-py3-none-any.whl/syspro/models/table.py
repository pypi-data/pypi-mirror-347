import xml.etree.ElementTree as ET
from .base import SysproBaseModel
from ..utils import find_operator


class TableModel(SysproBaseModel):
    def list(self, table_name: str, columns: list, num_rows: int = 1000,
                  wheres: list = None, order_by: list[str] = None):

        columns_expr = {
            "Column": columns
        }
        where_expr = None
        
        if wheres:
            where_expr = []
            for i, where in enumerate(wheres):
                where_expr.append({
                    "Expression": {
                        "OpenBracket": "(",
                        "Column": where[0],
                        "Condition": find_operator(where[1]),
                        "Value": where[2],
                        "CloseBracket": ")"
                    }
                })
        if order_by:
            order_by = {
                "Column": order_by
            }

        xmlin = {
            "@attributes": {
                "xmlns:xsd": "http://www.w3.org/2001/XMLSchema-instance",
                "xsd:noNamespaceSchemaLocation": "COMFND.XSD"
            },
            "TableName": table_name,
            "ReturnRows" : num_rows,
            "Columns": columns_expr,
            "Where": where_expr,
            "OrderBy": order_by
        }

        self.get_items(bo="COMFND", xmlin=xmlin)
        return self
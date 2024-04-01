from enum import Enum


class ExportType(Enum):
    ReportViewing = 1, 'Reporting / viewing'
    EditingImporting = 2, ' Editing / importing'


class ExportFields(Enum):
    ItemID = 1, 'Item ID'
    Statuses = 6, 'Status(es)'
    Name = 7, 'Name'


class InventorySearchRequest():
    exportType: ExportType = ExportType.ReportViewing
    exportFields: list[ExportFields] = list()

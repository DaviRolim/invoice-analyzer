import json
import boto3
from trp import trp2_expense
import base64

# Forked from https://github.com/aws-samples/amazon-textract-textractor/blob/master/prettyprinter/textractprettyprinter/t_pretty_print_expense.py
def convert_expenselineitemgroup_to_list(trp_table: trp2_expense.TLineItemGroup):
    rows_list = list()
    for _, row in enumerate(trp_table.lineitems):
        one_row = dict()
        for _, cell in enumerate(row.lineitem_expensefields):
            if cell.ftype and cell.ftype.text == 'EXPENSE_ROW':
                continue
            key = cell.ftype.text.lower()
            # TODO map quantity to int, price to float
            one_row[key] = cell.valuedetection.text

        if 'item' in one_row and one_row['item'] != "":
            rows_list.append(one_row)
    return rows_list


def get_expenselineitemgroups_json_list(textract_json: dict):
    doc = trp2_expense.TAnalyzeExpenseDocumentSchema().load(textract_json)
    items = []
    for document in doc.expenses_documents:
        for table in document.lineitemgroups:
            table_list = convert_expenselineitemgroup_to_list(
                table)
            items.append(table_list)
    return items


def main(event, context):
    print(event)
    print(event['body'])
    image_bytes = base64.b64decode(event['body'])
    client = boto3.client(
        service_name='textract',
        region_name='us-east-1',
        endpoint_url='https://textract.us-east-1.amazonaws.com',
        )

    response = client.analyze_expense(Document={'Bytes': image_bytes})
    allgroupeditems = get_expenselineitemgroups_json_list(response)
    print(allgroupeditems[0])
    body = allgroupeditems
    return {"statusCode": 200, "body": json.dumps(body)}

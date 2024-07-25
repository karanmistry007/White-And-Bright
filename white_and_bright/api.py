from erpnext.controllers.taxes_and_totals import (
    get_itemised_tax,
)
import frappe


@frappe.whitelist()
def item_wise_tax_sales_invoice(docname):
    # ? FINAL DATA SET
    final_data = {}

    try:
        # ? IF THE DOC EXISTS
        if frappe.db.exists("Sales Invoice", docname):
            # ? GET THE DOC AND DEFINE VARIABLES
            sales_invoice = frappe.get_doc("Sales Invoice", docname)
            item_table = sales_invoice.items
            taxes_table = sales_invoice.taxes

            # ? ADD EACH ITEMS INTO FINAL OBJECT AS DICT
            for item in item_table:
                # ! TEMP CODE WILL DO IT IN FUTURE FOR INCREASING EFFICIENCY
                # item_schemas = {
                #     "item_code": item.item_code,
                #     "item_name": item.item_name,
                #     "customer_item_code": item.customer_item_code,
                #     "description": item.description,
                #     "item_group": item.item_group,
                #     "brand": item.brand,
                #     "image": item.image,
                #     "qty": item.qty,
                #     "stock_uom": item.stock_uom,
                #     "uom": item.uom,
                #     "conversion_factor": item.conversion_factor,
                #     "stock_qty": item.stock_qty,
                #     "price_list_rate": item.price_list_rate,
                #     "base_price_list_rate": item.base_price_list_rate,
                # }
                #! END OF TEMP CODE

                final_data[item.item_code] = item.__dict__

            # ? GET THE ITEM WISE TAXES
            item_wise_taxes = get_itemised_tax(taxes_table)

            # ? CALCULATE TAX FOR EACH ITEM
            for item in item_wise_taxes:
                # ? SET THE BASE DATA
                tax_rate = 0
                tax_amount = 0

                # ? IF THE ITEM WITH SAME NAME EXISTS IN FINAL DATA
                if item in final_data:

                    # ? FOR MULTIPLE TAXES PER ITEM
                    for taxes in item_wise_taxes[item]:

                        # ? SET THE RATE AND AMOUNT
                        tax_rate += item_wise_taxes[item][taxes]["tax_rate"]
                        tax_amount += item_wise_taxes[item][taxes]["tax_amount"]

                    # ? APPEND THE RATE AND AMOUNT IN FINAL DATA
                    final_data[item]["tax_rate"] = tax_rate
                    final_data[item]["tax_amount"] = tax_amount

        # ? IF THE DOC DOES NOT EXISTS
        else:
            frappe.throw(f"Sales Invoice {docname} Not Found!")

    except Exception as e:
        frappe.throw(f"Unexpected Error: {str(e)}")

    else:
        return final_data

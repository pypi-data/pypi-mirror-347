from eBonsParser.stores import Rewe

pdf_file_path = "/home/oraies/Desktop/Projects/eBonsParser/examples/rewe/rewe_card.pdf"

rewe = Rewe()

receipt = rewe.parse_ebon(pdf_file_path)
print(receipt.model_dump_json(indent=4))
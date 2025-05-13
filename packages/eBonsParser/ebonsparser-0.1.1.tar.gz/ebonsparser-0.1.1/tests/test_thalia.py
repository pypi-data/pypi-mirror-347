from eBonsParser.stores import Thalia

pdf_file_path = "/home/oraies/Desktop/Projects/eBonsParser/examples/thalia/thalia_card.pdf"

thalia = Thalia()

receipt = thalia.parse_ebon(pdf_file_path)
print(receipt.model_dump_json(indent=4))
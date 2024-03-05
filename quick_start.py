from src.main import process_paper, find_peudo_code

# How to use
path_to_paper = "../test/pseudocode2.pdf"

count, pseudo_codes_list = find_peudo_code(path_to_paper, 0.6) #put your path and the confidence level for YOLO

print(f"A nomber of pseudocode: {count}")

for i, pseudo_code in enumerate(pseudo_codes_list):
    print(f"\n\n\nPseudocode {i+1}:")
    print(pseudo_code)

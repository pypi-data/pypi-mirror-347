import argparse

def get_parse() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="WinRAR ripoff made by HaxoTF")
    parser_sub = parser.add_subparsers(dest="command", required=True)

    parser_sub_pack = parser_sub.add_parser("pack")
    parser_sub_pack.add_argument("-i", "--input",    dest="input",    type=str, help="Directory path")
    parser_sub_pack.add_argument("-o", "--output",   dest="output",   type=str, help="PXD path")
    parser_sub_pack.add_argument("-p", "--password", dest="password", type=str, help="Encrypt PXD using password")

    parser_sub_free = parser_sub.add_parser("free")
    parser_sub_free.add_argument("-i", "--input",    dest="input",    type=str, help="PXD path")
    parser_sub_free.add_argument("-o", "--output",   dest="output",   type=str, help="Where to free?")
    parser_sub_free.add_argument("-p", "--password", dest="password", type=str, help="Decrypt PXD using password")

    
    return parser.parse_args()
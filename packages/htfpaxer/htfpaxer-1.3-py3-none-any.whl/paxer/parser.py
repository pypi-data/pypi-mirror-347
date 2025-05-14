import argparse

def get_parse() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="WinRAR ripoff made by HaxoTF")
    parser_sub = parser.add_subparsers(dest="command", required=True)

    parser_sub_pack = parser_sub.add_parser("pack")
    parser_sub_pack.add_argument("-i", "--input",    dest="input",    type=str, default=None, help="Directory path")
    parser_sub_pack.add_argument("-o", "--output",   dest="output",   type=str, default=None, help="Where to save the PXD?")
    parser_sub_pack.add_argument("-p", "--password", dest="password", type=str, default=None, help="Encrypt PXD using password")

    parser_sub_free = parser_sub.add_parser("free")
    parser_sub_free.add_argument("-i", "--input",    dest="input",    type=str, default=None, help="Where is PXD?")
    parser_sub_free.add_argument("-o", "--output",   dest="output",   type=str, default=None, help="Where to free?")
    parser_sub_free.add_argument("-p", "--password", dest="password", type=str, default=None, help="Decrypt PXD using password")

    parser_sub_count = parser_sub.add_parser("count")
    parser_sub_count.add_argument("-i", "--input",    dest="input",   type=str, default=None, help="Where is PXD?")

    parser_sub_list = parser_sub.add_parser("list")
    parser_sub_list.add_argument("-i", "--input",      dest="input",  type=str, default=None,  help="Where is PXD?")
    parser_sub_list.add_argument("-p", "--parent",     dest="parent", type=str, default=None,  help="List only from this parent")
    parser_sub_list.add_argument("-d", "--depth",      dest="depth",  type=int, default=-1,    help="How deep the list should be?")
    parser_sub_list.add_argument("-D", "--only-dirs",  dest="only_dirs",  action="store_true", help="List directories only")
    parser_sub_list.add_argument("-F", "--only-files", dest="only_files", action="store_true", help="List files only")
    
    return parser.parse_args()
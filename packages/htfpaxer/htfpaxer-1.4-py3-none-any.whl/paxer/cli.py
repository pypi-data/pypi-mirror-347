from . import core
from . import parser, stage
from colorama import Fore, Back, Style
import os, sys
import htfbox as hbox
from tkinter import filedialog

def main():

    # Arguments
    args = parser.get_parse()

    # Command
    cmd :str = args.command
    match cmd:

        # PACK
        case "pack":
            
            # I/O
            inp :str = args.input
            out :str = args.output
            
            # Password
            password = args.password
            if password: password = core.packer.Password(args.password)

            # Dialog
            if not inp: inp = filedialog.askdirectory(title="What to pack?")
            if not inp: stage.quick_error("Cancelled")
            if not out: out = filedialog.asksaveasfilename(title="Where to save PXD?", filetypes=[("Paxed File", "*.pxd")])
            if not out: stage.quick_error("Cancelled")
            out = os.path.splitext(out)[0] + ".pxd"

            # Calculating
            hbox.term.rewrite_line("Calculating...")
            total = hbox.dirs.count_items(inp)
            term_width = os.get_terminal_size().columns

            # Packing
            now = 0
            for rel, etype in core.packer.pack_all(inp, out, password):
                now += 1
                percent = f"{round(now/total*100, 1)} %"
                tracker = f"{hbox.toys.bar(now, total, 50, percent)} {rel}"
                tracker = tracker[:term_width]
                hbox.term.rewrite_line(tracker)
            
            # Finish
            hbox.term.rewrite_line("Done")
        
        # FREE
        case "free":
            
            # I/O
            inp :str = args.input
            out :str = args.output
            
            # Password
            password = args.password
            if password: password = core.packer.Password(args.password)

            # Dialog
            if not inp: inp = filedialog.askopenfilename(title="Where is PXD?", filetypes=[("Paxed File", "*.pxd")])
            if not inp: stage.quick_error("Cancelled")
            if not out: out = filedialog.askdirectory(title="Where to Free?")
            if not out: stage.quick_error("Cancelled")

            # Calculating
            hbox.term.rewrite_line("Calculating...")
            d, f = core.packer.count_entries(inp); total = d + f
            term_width = os.get_terminal_size().columns

            # Freeing
            now = 0
            for rel, etype in core.packer.free_all(inp, out, password):
                now += 1
                percent = f"{round(now/total*100, 1)} %"
                tracker = f"{hbox.toys.bar(now, total, 50, percent)} {rel}"
                tracker = tracker[:term_width]
                hbox.term.rewrite_line(tracker)

            # Finish
            hbox.term.rewrite_line("Done")
        
        # COUNT
        case "count":
            
            # I/O
            inp :str = args.input

            # Dialog
            if not inp: inp = filedialog.askopenfilename(title="Where is PXD?", filetypes=[("Paxed File", "*.pxd")])
            if not inp: stage.quick_error("Cancelled")

            # Calculating
            d, f = core.packer.count_entries(inp); total = d + f

            # Finish
            print(f"Dirs  : {d}")
            print(f"Files : {f}")
            print(f"Total : {total}")
        
        # LIST
        case "list":

            # I/O
            inp :str = args.input
            par :str = args.parent
            dep :int = args.depth
            count_dirs = True
            count_files = True

            if args.only_dirs: count_files = False
            if args.only_files: count_dirs = False

            # Dialog
            if not inp: inp = filedialog.askopenfilename(title="Where is PXD?", filetypes=[("Paxed File", "*.pxd")])
            if not inp: stage.quick_error("Cancelled")

            # Print
            if par: par = os.path.normpath(par)
            for rel, etype, size in core.packer.get_all_in_depth(inp, par, dep):
                match etype:
                    case "dir":
                        if not count_dirs: continue
                        print(Fore.YELLOW + rel + Fore.RESET)
                    
                    case "file":
                        if not count_files: continue
                        parent, filename = os.path.split(rel)
                        print(Fore.LIGHTBLACK_EX + parent + os.sep + Fore.RESET + filename)

        # BROWSE
        case "browse":

            # I/O
            inp :str = args.input

            # Dialog
            if not inp: inp = filedialog.askopenfilename(title="Where is PXD?", filetypes=[("Paxed File", "*.pxd")])
            if not inp: stage.quick_error("Cancelled")

            # Cache
            parent = ""
            entries_inside = list(core.packer.get_all_in_depth(inp, parent, 1))
            parent = entries_inside[0][0]
            entries_inside = entries_inside[1:]

            selected = 0
            while True:
                

                # Display
                hbox.term.clear(); hbox.term.place_cursor(0, 0)
                print(Fore.CYAN+parent+"\n"+Fore.RESET)
                term_width = os.get_terminal_size().lines
                a = int(term_width/2) - 3

                for i in range(selected-a, selected+a):

                    if i < 0: print(); continue
                    if i >= len(entries_inside): print("\n"*(selected+a-i)); break

                    path, etype, size = entries_inside[i]
                    name = os.path.split(path)[1]

                    line = ""
                    if i!=selected: line += Style.DIM
                    match etype:
                        case "dir": line += Fore.YELLOW + name + Fore.RESET
                        case "file": line += name
                    if i!=selected: line += Style.RESET_ALL
                    
                    print(line)
                print("\nArrows: Navigate // [Q] = Quit")


                key = stage.get_key()
                match key:
                    case "q":
                        hbox.term.clear(); hbox.term.place_cursor(0, 0)
                        sys.exit(0)
                    
                    case "up":
                        selected = max(0, min(selected-1, len(entries_inside)))
                    
                    case "down":
                        selected = max(0, min(selected+1, len(entries_inside)))
                    
                    case "right":
                        path, etype, size = entries_inside[selected]
                        if etype == "dir":
                            parent = path
                        entries_inside = list(core.packer.get_all_in_depth(inp, parent, 1))[1:]
                        selected = 0
                    
                    case "left":
                        np = os.path.split(parent)[0]
                        if np:
                            parent = np
                        entries_inside = list(core.packer.get_all_in_depth(inp, parent, 1))[1:]
                        selected = 0
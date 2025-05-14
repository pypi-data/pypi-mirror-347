from . import core
from . import parser, stage
from colorama import Fore
import os
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
            for rel, etype in core.packer.free_all(inp, "", None, True):
                
                # Info
                rel = os.path.normpath(rel)
                parent = os.path.normpath(os.path.split(rel)[0])
                depth = len(rel.split(os.sep)) -1

                # Parent
                if par:
                    if not parent.startswith(par): continue
                    depth -= len(par.split(os.sep)) -1
                
                # Depth
                if dep!=-1:
                    if depth>dep:
                        continue
                
                # Display
                match etype:
                    case "dir":
                        if not count_dirs: continue
                        print(Fore.YELLOW + rel + Fore.RESET)
                    
                    case "file":
                        if not count_files: continue
                        parent, filename = os.path.split(rel)
                        print(Fore.LIGHTBLACK_EX + parent + os.sep + Fore.RESET + filename)
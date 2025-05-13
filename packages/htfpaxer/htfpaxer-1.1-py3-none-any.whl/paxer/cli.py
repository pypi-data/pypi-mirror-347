from . import core
from . import parser, stage
import os
import htfbox as hbox
from tkinter import filedialog

def main():

    # Arguments
    args = parser.get_parse()
    cmd :str = args.command
    inp :str = args.input
    out :str = args.output

    # Password
    password :str = args.password
    if password: password = core.packer.Password(password)
    else: password = None

    # Command
    match cmd:

        # PACK
        case "pack":

            if not inp: inp = filedialog.askdirectory(title="Select Directory")
            if not inp: stage.quick_error("Cancelled")
            if not out: out = filedialog.asksaveasfilename(title="Save As", filetypes=[("Paxed File", "*.pxd")])
            if not out: stage.quick_error("Cancelled")
            out = os.path.splitext(out)[0] + ".pxd"

            hbox.term.rewrite_line("Calculating...")
            total = hbox.dirs.count_items(inp)
            term_width = os.get_terminal_size().columns

            now = 0
            for rel, etype in core.packer.pack_all(inp, out, password):
                now += 1
                percent = f"{round(now/total*100, 1)} %"
                tracker = f"{hbox.toys.bar(now, total, 50, percent)} {rel}"
                tracker = tracker[:term_width]
                hbox.term.rewrite_line(tracker)
            
            hbox.term.rewrite_line("Done")
        
        # FREE
        case "free":

            if not inp: inp = filedialog.askopenfilename(title="Select Paxed File")
            if not inp: stage.quick_error("Cancelled")
            if not out: out = filedialog.askdirectory(title="Where to Free?")
            if not out: stage.quick_error("Cancelled")

            hbox.term.rewrite_line("Calculating...")
            total = core.packer.count_entries(inp)
            term_width = os.get_terminal_size().columns

            now = 0
            for rel, etype in core.packer.free_all(inp, out, password):
                now += 1
                percent = f"{round(now/total*100, 1)} %"
                tracker = f"{hbox.toys.bar(now, total, 50, percent)} {rel}"
                tracker = tracker[:term_width]
                hbox.term.rewrite_line(tracker)

            hbox.term.rewrite_line("Done")
"""Report all time units"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from logging import debug

from timetracker.cmd.common import get_cfg
from timetracker.cmd.common import get_fcsv
from timetracker.utils import yellow
from timetracker.csvfile import CsvFile
from timetracker.docx import WordDoc
from timetracker.epoch.text import get_data_formatted
from timetracker.csvrun import chk_n_convert
from timetracker.report import Report


def cli_run_report(fnamecfg, args):
    """Report all time units"""
    if args.input is None:
        run_report(fnamecfg, args.name, pnum=args.product)
    elif len(args.input) == 1:
        _run_io(args.input[0], args.output, pnum=args.product)
    else:
        raise RuntimeError('TIME TO IMPLEMENT')
    ##if args.input and exists(args.input):
    ##    print(args.input)
    ##if args.input and args.output and exists(args.input):
    ##    _run_io(args.input, args.output)
    ##    return
    ##run_report(
    ##    fnamecfg,
    ##    args.name,
    ##    fin=args.input,
    ##    fout=args.output,
    ##)

def run_report(fnamecfg, uname, pnum=None, dirhome=None):
    """Report all time units"""
    debug(yellow('RUNNING COMMAND REPORT'))
    cfg = get_cfg(fnamecfg)
    fcsv = get_fcsv(cfg, uname, dirhome)
    return _run_io(fcsv, None, pnum) if fcsv is not None else None

def _run_io(fcsv, fout_docx, pnum):
    """Run input output"""
    chk_n_convert(fcsv)
    ocsv = CsvFile(fcsv)
    timedata, errs = ocsv.get_ntdata()
    #for e in sorted(timedata, key=lambda nt: nt.start_datetime):
    #    print(e)  # TimeData namedtuple
    timefmtd = get_data_formatted(timedata, pnum)
    if timefmtd:
        Report(timefmtd).prt_basic()
        if fout_docx:
            doc = WordDoc(timefmtd)
            doc.write_doc(fout_docx)
    if errs:
        for err in errs:
            print(err)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.

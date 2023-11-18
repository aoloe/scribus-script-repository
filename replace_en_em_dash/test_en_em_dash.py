#!/usr/bin/env python3
import sys
import subprocess

def main():
    try:
        import scribus
        run_script()
    except ImportError:
        run_scribus()

def run_scribus():
    # if len(sys.argv) < 2:
    #     print(f'Usage: python3 {sys.argv[0]} filename')
    #     return

    call_args = ['scribus', '-g', '-py', sys.argv[0]]
    # call_args += ['--', sys.argv[1]]
    subprocess.call(call_args)

def run_script() :
    scribus.newDocument(scribus.PAPER_A4_MM, (10, 10, 10, 10), scribus.PORTRAIT, 1, scribus.UNIT_MILLIMETERS, scribus.PAGE_1, 0, 1)
    test_text = [
        ('some text -- well -- more text', 'some text – well – more text'),
        ('-- can we start with it? -- more text', '– can we start with it? – more text'),
        ('some text -- or end with it? --', 'some text – or end with it? –'),
        ('a three dashes ---','a three dashes —'),
        ('some dashes 3 --- 2 -- 3 --- 4 ---- 2 -- 5 -----', 'some dashes 3 — 2 – 3 — 4 ---- 2 – 5 -----'),
        ('even in--the--middle--of--a--word','even in–the–middle–of–a–word'),
        ('leave-my-single-dashes-alone -- is it ok?', 'leave-my-single-dashes-alone – is it ok?'),
    ]
    for i, text in enumerate(test_text):
        frame = 'test-' + str(i)
        scribus.createText(10, 10 + 15 * i, 80, 15, frame)
        scribus.insertText(text[0], 0, frame)

    # scribus.saveDocAs('test_en_em_dash.sla') # enable for starting manual testing

    import replace_en_em_dash as reed
    reed.main()
    for i, text in enumerate(test_text):
        # print('>>>', i, scribus.getAllText('test-' + str(i)))
        assert scribus.getAllText('test-' + str(i)) == text[1]

if __name__ == "__main__":
    main()

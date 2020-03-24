# import argparse
from os import path
from tqdm import tqdm

ssa_file_path = None


def main():
    global ssa_file_path
    srt_file_path = input('Enter SubRip [.srt] subtitle file name:')

    if(srt_file_path.endswith('.srt')):
        ssa_file_path = srt_file_path.replace('.srt', '.ssa')
    else:
        print('Error: Incorrect file format.')
        exit(-1)

    if(path.exists(srt_file_path) == False):
        print('Error: File {0} not exists.'.format(srt_file_path))
        exit(-1)

    write_ssa_script_info(srt_file_path.replace('.srt', ''))
    write_ssa_styles()
    write_ssa_events_header()

    with tqdm(total=path.getsize(srt_file_path), bar_format='{l_bar}{bar:50}{r_bar}{bar:-10b}') as pbar:
        with open(srt_file_path) as file_reader:
            current_line = file_reader.readline()
            progress = len(current_line)
            #previous_line = None
            dialog_lines = []
            timestamps = []
            while current_line:
                if(not current_line.strip()):
                    pbar.update(progress)
                    write_ssa_dialogue(timestamps[0].strip(), timestamps[1].strip(), *dialog_lines)
                    progress = 0
                    dialog_lines = []

                if(len(timestamps) == 2 and current_line.strip()):
                    dialog_lines.append(current_line)
                else:
                    timestamps = current_line.split('-->')

                #previous_line = current_line.strip()
                current_line = file_reader.readline()
                progress = progress + len(current_line)
        pbar.update(pbar.total - pbar.n)


def write_ssa_script_info(title):
    info = [
        '[Script Info]\n',
        '; This is a Sub Station Alpha v4 script.\n',
        '; For Sub Station Alpha info and downloads,\n',
        '; go to http://www.eswat.demon.co.uk/\n'
    ]
    print(ssa_file_path)
    with open(ssa_file_path, 'w') as file_writer:
        file_writer.writelines(info)
        file_writer.write('Title: {0}\n'.format(title))
        file_writer.write('ScriptType: v4.00\n')
        file_writer.write('Collisions: Normal\n')
        file_writer.write('Timer: 100,0000\n')


def write_ssa_styles():
    header_columns = [
        'Name',
        'Fontname',
        'Fontsize',
        'PrimaryColour',
        'SecondaryColour',
        'TertiaryColour',
        'BackColour',
        'Bold',
        'Italic',
        'BorderStyle',
        'Outline',
        'Shadow',
        'Alignment',
        'MarginL',
        'MarginR',
        'MarginV',
        'AlphaLevel',
        'Encoding'
    ]

    default_values = [
        'Default',
        'Arial',
        '28',
        '11861244',
        '11861244',
        '11861244',
        '-2147483640',
        '-1',
        '0',
        '1',
        '1',
        '2',
        '2',
        '30',
        '30',
        '30',
        '0',
        '0'
    ]

    with open(ssa_file_path, 'a') as file_writer:
        file_writer.write('[V4 Styles]\n')
        file_writer.write('Format: ')
        file_writer.write(', '.join(header_columns))
        file_writer.write('\n')
        file_writer.write('Style: ')
        file_writer.write(', '.join(default_values))
        file_writer.write('\n')


def write_ssa_events_header():
    header_columns = [
        'Marked',
        'Start',
        'End',
        'Style',
        'Name',
        'MarginL',
        'MarginR',
        'MarginV',
        'Effect',
        'Text'
    ]

    with open(ssa_file_path, 'a') as file_writer:
        file_writer.write('[Events]\n')
        file_writer.write('Format: ')
        file_writer.write(', '.join(header_columns))
        file_writer.write('\n')


def write_ssa_dialogue(start, end, *dialogues):
    dialogue_line = 'Dialogue: Marked=0,{0},{1},Default,NTP,0000,00 00,0020,!Effect,'.format(
        start, end)

    if(len(dialogues) > 1):
        for dialog in dialogues:
            dialogue_line = dialogue_line + dialog.strip() + '\\N'
        dialogue_line = dialogue_line.rstrip('\\N')
    else:
        dialogue_line = dialogue_line + dialogues[0].strip()

    with open(ssa_file_path, 'a') as file_writer:
        file_writer.write(dialogue_line + '\n')


if __name__ == "__main__":
    main()

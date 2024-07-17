from argparse import ArgumentParser, Namespace

import fileindexer


class FileIndexerCLI(ArgumentParser):
    """ Basic CLI to interact with `fileindexer`. """
    def __init__(self) -> None:
        super().__init__(description='File Indexer and searcher')
        self._prepare()
        
    def _prepare(self) -> None:
        """ Preparing the arguments for the cli """
       
        self.add_argument(
            '-ft',
            '--file_type',
            metavar='ft',
            type=str,
            default='py',
            help='The file type you want to look for'
        )
        
        self.add_argument(
            '-w',
            '--writer',
            metavar='w',
            type=str,
            help='Writes details about all files in the .csv file'
        )
        
        self.add_argument(
            '-rf'
            '--record_file',
            metavar='rf',
            type=str,
            help='The .csv file where you want to store the records'
        )
        
        self.add_argument(
            '-f',
            '--find',
            metavar='f',
            type=str,
            help='Finds the file and returns the details about it'
        )
        
        self.add_argument(
            '-r',
            '--recent',
            metavar='r',
            type=int,
            help='Shows details of the recent files'
        )
        
        self.add_argument(
            '-o',
            '--open',
            metavar='o',
            type=bool,
            default=False,
            help='Opens the file and shows its contents'
        )
        
    @staticmethod
    def show_results(args: Namespace) -> None:
        """ Showing the results of the arguments """
        finder = fileindexer.Finder(
            args.writer,
            args.rf__record_file,
            call_type='cli',
            file_type=args.file_type
        )
        finder.write()
        
        if args.find is not None:
            print(*finder.find(args.find), sep='='*100)
        
        if args.recent is not None:
            print(*finder.indexed_files[:args.recent], sep='='*100)
            
        if args.open:
            print('='*100)
            recent_file = finder.recent_file
            if recent_file is None:
                print('File not found!')
                return
            with open(recent_file.file_path, encoding='utf-8') as file:
                print(file.read())

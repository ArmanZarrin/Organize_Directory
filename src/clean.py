import json
from pathlib import Path

import shutil
from loguru import logger

from src.data import Data_DIR


class Organizefiles:

      """
    It takes a directory path and oraganize tha containing files in specific destinations
    """
      def __init__(self , Dir_Path):
          self.path=Path(Dir_Path);
          if not self.path.exists():
                raise FileNotFoundError("The path is not valid");
          self.extensions_dest={};
          with open(Data_DIR/'extensions.json') as f:
                ext_dirs=json.load(f);
                for Dir_name,extensions in ext_dirs.items():
                      for extension in extensions:
                            self.extensions_dest[extension]=Dir_name;
          #print(self.extensions)
      def __call__(self):
            logger.info(f"Organizing files in {self.path}...");
            """
            organizes the files in the directory by moving them to their respective directories
            """
            file_extensions=[]
            for file_path in self.path.iterdir():
                #ignore_directories
                if file_path.is_dir():
                    continue
                #ignore_hidden_file
                if file_path.name.startswith('.'):
                    continue
                file_extensions.append(file_path.suffix)
                if file_path.suffix not in self.extensions_dest:
                    Dest_Dir=self.path/'other'
                else:
                    Dest_Dir=self.path/self.extensions_dest[file_path.suffix]
                Dest_Dir.mkdir(exist_ok=True)
                shutil.move(str(file_path),str(Dest_Dir))
                logger.info(f'{file_path} moved to {Dest_Dir}')

if __name__ == "__main__":
  org_files=Organizefiles('/home/arman/Downloads');
  org_files();
  logger.info("Done!");
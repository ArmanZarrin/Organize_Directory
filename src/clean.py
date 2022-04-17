import json
import shutil
import sys
from pathlib import Path

from loguru import logger

from src.data import Data_DIR


class Organizefiles:

      """
    It takes a directory path and oraganize tha containing files in specific destinations
    """
      def __init__(self):
          self.extensions_dest={};
          with open(Data_DIR/'extensions.json') as f:
                ext_dirs=json.load(f);
                for Dir_name,extensions in ext_dirs.items():
                      for extension in extensions:
                            self.extensions_dest[extension]=Dir_name;
          #print(self.extensions)
      def __call__(self, Dir_Path):
            Dir_Path=Path(Dir_Path);
            if not Dir_Path.exists():
                    raise FileNotFoundError("The path is not valid");
            logger.info(f"Organizing files in {Dir_Path}...");
            """
            organizes the files in the directory by moving them to their respective directories
            """
            file_extensions=[]
            for file_path in Dir_Path.iterdir():
                #ignore_directories
                if file_path.is_dir():
                    continue
                #ignore_hidden_file
                if file_path.name.startswith('.'):
                    continue
                file_extensions.append(file_path.suffix)
                if file_path.suffix not in self.extensions_dest:
                    Dest_Dir=Dir_Path/'other'
                else:
                    Dest_Dir=Dir_Path/self.extensions_dest[file_path.suffix]
                Dest_Dir.mkdir(exist_ok=True)
                shutil.move(str(file_path),str(Dest_Dir))
                logger.info(f'{file_path} moved to {Dest_Dir}')

if __name__ == "__main__":
    logger.info(f"your Input Directory is: {sys.argv[1]}");
    org_files=Organizefiles();
    org_files(sys.argv[1]);
    logger.info("Done!");

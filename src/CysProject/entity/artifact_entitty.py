from dataclasses import dataclass
from src.CysProject.constants import training_pipeline


@dataclass
class DataIngestionArtifact:
    trained_file_path: str 
    test_file_path: str
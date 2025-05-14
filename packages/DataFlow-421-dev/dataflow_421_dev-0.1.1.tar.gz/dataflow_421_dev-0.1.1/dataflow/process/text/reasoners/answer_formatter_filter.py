from dataflow.core import TextFilter, ReasonerFilter
import numpy as np
from dataflow.utils.registry import PROCESSOR_REGISTRY
import re
from dataflow.utils.utils import get_logger

@PROCESSOR_REGISTRY.register()
class AnswerFormatterFilter(ReasonerFilter):
    def __init__(self, args_dict: dict):
        super().__init__(args_dict)
        self.filter_name = 'AnswerFormatterFilter'
        self.logger = get_logger()
        
    def is_valid_answer(answer: str) -> bool:
        # check final answer in \boxed{} or not 
        if not re.search(r'\\boxed{.*}', answer):
            return False
        
        return True 
    
    def filter_func(self, dataset):
        indexes =  np.zeros(len(dataset)).astype(int)

        for i, item in enumerate(dataset):
            answer = item[self.keys]
            if AnswerFormatterFilter.is_valid_answer(answer):
                indexes[i] = 1

        return indexes
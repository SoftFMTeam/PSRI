from ccft.core.constant import ENode, ERelation, EExpand


class InstructionConverter:
    @staticmethod
    def get_action(instruction) -> str:
        pass

    @staticmethod
    def get_id(instruction) -> int:
        pass

    @staticmethod
    def reply(cmd_id, status, message=None, **params) -> str:
        pass

    @staticmethod
    def exit() -> str:
        pass

    @staticmethod
    def parse_sourcecode_instruction(instruction) -> tuple[str, str, str, str]:
        pass

    @staticmethod
    def parse_cpg_instruction(instruction) -> tuple[str, str]:
        pass

    @staticmethod
    def load_model_instruction(instruction) -> tuple[str, str]:
        pass

    @staticmethod
    def cut_parse_model_instruction(instruction) -> tuple[str, str, list[int], list[ENode], list[ERelation], EExpand]:
        pass

    @staticmethod
    def demo_instruction(instruction):
        pass

    @staticmethod
    def gen_analysis_instruction(instruction) -> tuple[str, str, dict, bool]:
        pass

    @staticmethod
    def get_path_instruction(instruction) -> tuple[str, str, str, int, int, int]:
        pass

    @staticmethod
    def get_tree_instruction(instruction) -> tuple[str, str, int, int, int]:
        pass

    @staticmethod
    def get_subgraph_instruction(instruction) -> tuple[str, str, list, list, EExpand, int]:
        pass

    @staticmethod
    def get_path_return(cmd_id, status, paths):
        pass
